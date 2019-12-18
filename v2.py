import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import math
import requests
import Adafruit_DHT
import RPi.GPIO as GPIO

#Set up Status LED
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)

#Set up DHT22 humidity and temperature sensor
dht_pin = 4
dht_sensor = Adafruit_DHT.DHT22

#Set up ADS1115 board for reading voltages.
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan0 = AnalogIn(ads, ADS.P0, ADS.P1)
#chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)
shuntR1 = .00075
shuntR2 = .0025
adcvalues = [0,0,0,0,0,0,0,0,0,0]
chatter = 1  # chatter of 1 means to print output. Anything else will not print.
counter = 0

Battery_Calibrate = -0.03
Shunt1_Calibrate = 0.00009
Shunt2_Calibrate = 0
Shunt3_Calibrate = 0

#Set up url info for posting data to an influx database that Grafana will use as the source.
headers = {'Content-type': 'text/plain'}
urlstring_local = 'http://localhost:8086/write?db=VoltMeter'
urlstring_remote = 'http://www.bs911.us:8086/write?db=PowerMeter'

#  The following multi level list is used to calculate an estimated battery "capacity" based off of
#  battery voltage at the current battery load. This list is an estimate and may need tuned for your
#  specific battery bank. Each second level list represents load in amps, min, max, then percentages of
#  estimated voltage readings for the battery level at that load.

Batt_Capacity = [0,0,0,0,0,0,0,0,0]
Batt_Capacity[0] = [0,-99,1,11.2,11.3,11.6,11.8,11.9,12.1,12.2,12.3,12.4,12.5,12.6,99]
Batt_Capacity[1] = [2.5,1,3.75,11.0,11.1,11.4,11.6,11.8,11.9,12.0,12.2,12.3,12.4,12.5,99]
Batt_Capacity[2] = [5,3.75,6.25,10.9,11.0,11.2,11.5,11.6,11.8,11.9,12.0,12.1,12.2,12.3,99]
Batt_Capacity[3] = [7.5,6.25,8.75,10.7,10.8,11.1,11.3,11.5,11.6,11.7,11.9,12.0,12.1,12.2,99]
Batt_Capacity[4] = [10,8.75,11.25,10.5,10.6,10.9,11.2,11.4,11.5,11.6,11.8,11.9,12.0,12.1,99]
Batt_Capacity[5] = [12.5,11.25,13.75,10.4,10.5,10.8,11.1,11.3,11.4,11.6,11.7,11.8,11.9,12.0,99]
Batt_Capacity[6] = [15,13.75,16.25,10.3,10.4,10.7,11.0,11.2,11.3,11.5,11.6,11.7,11.8,11.9,99]
Batt_Capacity[7] = [17.5,16.25,18.75,10.2,10.3,10.6,10.9,11.1,11.3,11.4,11.6,11.7,11.8,11.9,99]
Batt_Capacity[8] = [20,18.75,99,10.1,10.2,10.5,10.7,11.0,11.2,11.3,11.5,11.6,11.7,11.8,99]


def write_influx(unit,probe,value):
    datastring = str(unit) + ',probe=' + str(probe) + ' value=' +str(value)
    try:
        r = requests.post(urlstring_local, data=datastring, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError as e:
        print(e)

    try:
        r = requests.post(urlstring_remote, data=datastring, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError as e:
        print(e)

def do_print(arg):
    if chatter == 1:
        print(arg)


while True:
    # COUNTER
    # Some checks only run when load is on or periodic
    counter += 1
    
    ##### ---------------  LOAD  ---------------------
    ##### Shunt 1 on a load leg
    # Read Shunt Voltage. This is in very small mV measurements so will need high gain.
    do_print('----------------------------------------')
    ads.gain = 16
    ads.data_rate=8
    for i in range(10):
        adcvalues[i] = chan0.voltage + Shunt1_Calibrate
    value = sum(adcvalues) / len(adcvalues)
    #if value < 20 and value > -20: value = 0
    amps = value / shuntR1
    mvolts = value * 1000
    do_print('LOAD Value:' + f'{value:.5f}' + ' -- mVolts: ' + f'{mvolts:.2f}' + ' -- Amps: ' + f'{amps:.2f}')
    write_influx('I','BatteryAmps',round(amps,2))

    ##### -------------  BATTERY  ---------------------
    if counter == 1 or amps > 0:
        ads.gain = 1
        for i in range(10):
            adcvalues[i] = (chan3.voltage * 1220/220) + Battery_Calibrate
        voltage = sum(adcvalues) / len(adcvalues)
        do_print('BATTERY Volts: ' + f'{voltage:.2f}')
        write_influx('V','Voltage1',round(voltage,2))

        # BATTERY CAPACITY - Must come immediately after LOAD and BATTERY
        # Calculate battery capacity off of load index
        for i in range(9):
            if amps > Batt_Capacity[i][1] and amps <= Batt_Capacity[i][2]:
                do_print('LOAD Range: ' + str(Batt_Capacity[i][0]))
                for j in range(3,14):
                    if voltage >= Batt_Capacity[i][j] and voltage < Batt_Capacity[i][j+1]:
                        Capacity = (j-3)*10
                        do_print('CAPACITY: ' + str(Capacity))
                        write_influx('%','BatteryCap',Capacity)

    ##### --------------- CHARGE 1 ------------------
    ##### Shunt 2 on charge leg 1 - This is from converter charger
    ads.gain = 16
    for i in range(10):
        adcvalues[i] = (chan2.voltage * -1) - Shunt2_Calibrate
        adcvalues[i] = 0
    value = sum(adcvalues) / len(adcvalues)
    amps = value / shuntR2
    mvolts = value * 1000
    do_print('Converter CHARGE Value: ' + str(value) + ' -- mVolts: ' + f'{mvolts:.2f}' + ' -- Amps: ' + f'{amps:.1f}')
    write_influx('I','ChargeAmps',round(amps,2))

    ##### ---------------- CHARGE 2 ----------------------
    ##### Placeholder for Shunt 3 on solar charge controller
    #ads.gain = 16
    for i in range(10):
        #adcvalues[i] = (chan2.voltage * -1) - Shunt3_Calibrate
        adcvalues[i] = 0
    value = sum(adcvalues) / len(adcvalues)
    amps = value / shuntR2
    mvolts = value * 1000
    do_print('Solar CHARGE Value: ' + str(value) + ' -- mVolts: ' + f'{mvolts:.2f}' + ' -- Amps: ' + f'{amps:.1f}')
    write_influx('I','SolarAmps',round(amps,2))





    #Read Humidity and Temperature
    if counter == 1:
        humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
        temperature = int((temperature * 9 / 5) + 32)
        write_influx('F','Temperature',temperature)
        write_influx('%','Humidity',round(humidity,1))
        do_print('Humidity: ' + str(round(humidity,1)) + ' -- Temperature: ' + str(temperature))

    if counter == 10:
        counter = 0

    GPIO.output(5, GPIO.HIGH)
    time.sleep(.1)
    GPIO.output(5, GPIO.LOW)

    time.sleep(1)
