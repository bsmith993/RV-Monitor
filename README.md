# RV-Monitor

This is B. Smitty's RV Monitor.

# Overall Design
This python script will monitor the status of a 12v battery, 3 shunt resistors for the purposes of determining amperage in and out of the battery and charging system, a DHT humidity and temperature sensor, and has one LED output for blinking a status. Results are sent to an Influx database where it will then be used for monitoring with a Grafana Server.

The circuit utilizes 2 ADS1115 preassembled boards on a 10 pin, single row header to allow a total of 8 channels

Differential voltage readings are taken on ADS1115_1 A0/A1, ADS1115_1 A2/A3, and ADS1115_2 A0/A1, all at a gain of 16  to read the voltage across the shunts. Each line from A0/A1 go to each end of the shunt resistor measuring post. Using Ohm's Law, current(I) can be calculated by dividing the read voltage by the shunt resistor value. (.00075 = a shunt that allows 75 mV for 100 amps, or, .075 / 100 = .00075) Variables allow configuration of shunt resistance. Due to the high gain, line voltage loss, and other noise factors, a calibration variable is also utilized for each shunt reading. Use a  quality, standalone multimeter to adjust this variable until the ADS readings match actuals. Multiple comparisons are best to find the proper calbiration.

The Batt+ terminal accepts a positive 12v battery lead, which then runs through a simple divider circuit to drop the maximum voltage below the 3.3 ADS source voltage. The reading is then multiplied back to original values in software. The Batt- terminal grounds the remaining ADS input channel and bridges the ground of both the Raspberry Pi and the 12v system.

One scenario for monitoring includes a Raspberry Pi running the monitoring script and also running a self contained Influx database and Grafana instance. The Influx database should be set with a very low retention policy to avoid data growth. The local Grafana instance will pull from the influx database and show a real-time, and recent history capture of all data. This local instance will allow functionality while "off grid" and unable to connect to a remote server.

An extended scenario also sends data to external Influx/Grafana system to allow remote monitoring. With sufficient solar charging, the system can run indefinitely with the Raspberry Pi running off a 12v - 5v buck converting power supply. 

After initial prototyping on a breadboard, a printed PCB was designed to house all circuits. This PCB is designed to sit directly over the Raspberry Pi utilizing a GPIO extender and standoff mounts. I used EasyEDA.com and ordered PCB boards from JLBPCB.com with outstanding results. (Highly Recommended!) Long term use of a breadboard is inadvisable as the poor contacts wreak havoc on the sensitive voltage calculations that must be able to accurately differentiate fractions of millivolts.

# My most recent PCB design.
![Image of PCB photo](https://raw.githubusercontent.com/bsmith993/RV-Monitor/master/BSRVMv2.01_PCB_photo.png)

# Hardware Required
* ADS: 2x pre-built ADS1115 boards with 10 pin header
* 1 each: 10kΩ, 1kΩ, 220Ω, and 100Ω resistors
* 2x .1uF Capacitors
* 1 DHT22 Sensor
* 1 LED bulb
* 4x 2 post screw terminals
* 1 GPIO extension header
* 1 PCB or breadboard for initial prototyping
* Appropriate cable to extend from PCB terminals to shunt/battery endpoints
* 1 Raspberry Pi 


