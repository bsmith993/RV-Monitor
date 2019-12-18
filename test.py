import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import math


#Set up ADS1115 board for reading voltages.
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan0 = AnalogIn(ads, ADS.P0, ADS.P1)
#chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)
shuntR = .00075
shuntR2 = .0025
adcvalues = [0,0,0,0,0,0,0,0,0,0]
ads.data_rate=8
Battery_Calibrate = -0.03
Shunt1_Calibrate = 0.00009

while True:
    print('----------------------------------------')
    # BATTERY
    # Read Battery voltage. This is a 12v battery so running through a 0-25v voltage divider. I've found 4.95 more accurate than 5 as a divider.
    ads.gain = 1
    for i in range(10):
        adcvalues[i] = (chan3.voltage * 1220/220) + Battery_Calibrate
        #print(chan3.voltage)
    voltage = sum(adcvalues) / len(adcvalues)
    print('BATTERY Volts: ' + f'{voltage:.2f}')

    # DISCHARGE
    ads.gain = 16
    ads.data_rate=8
    for i in range(10):
        adcvalues[i] = chan0.voltage + Shunt1_Calibrate
        print(f'{adcvalues[i]:.7f}')
    value = sum(adcvalues) / len(adcvalues)
    amps = value / shuntR
    mvolts = value * 1000
    print('DISCHARGE Value: ' + f'{value:.5f}' + ' -- mVolts: ' + f'{mvolts:.2f}' + ' -- Amps: ' + f'{amps:.2f}')


    # CHARGE
    ads.gain = 16
    for i in range(10):
        adcvalues[i] = (chan2.voltage + .002615) * -1 *.9
        #print(adcvalues[i])
    value = sum(adcvalues) / len(adcvalues)
    amps = value / shuntR2
    mvolts = value * 1000
    print('CHARGE Value: ' + f'{value:.5f}' + ' -- mVolts: ' + f'{mvolts:.2f}' + ' -- Amps: ' + f'{amps:.2f}')


    time.sleep(1)

