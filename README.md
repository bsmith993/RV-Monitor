# RV-Monitor

This is B. Smitty's RV Monitor.

# Overall Design
This system will monitor the status of a 12v battery, 3 shunt resistors for the purposes of determining amperage in and out of the battery and charging system, a DHT humidity and temperature sensor, and has one LED output for blinking a status. Results are sent to an Influx database where it will then be used for monitoring with a Grafana Server.

# Current Readings

The circuit utilizes 2 ADS1115 chips on a custom PCB providing a total of 8 inputs.

Differential voltage readings are taken on ADS1115_1 A0/A1, ADS1115_1 A2/A3, and ADS1115_2 A0/A1, all at a gain of 16  to read the voltage differential across the shunts. Each line from A0/A1 go to each end of the shunt resistor measuring post. Using Ohm's Law, current(I) can be calculated by dividing the read voltage by the shunt resistor value. (.00075 = a shunt that allows 75 mV for 100 amps, or, .075 / 100 = .00075) Variables in the script allow configuration of shunt resistance. Due to the high gain, line voltage loss, and other noise factors, a calibration variable is also utilized for each shunt reading. Use a  quality, standalone multimeter to adjust this variable until the ADS readings match actuals. Multiple comparisons are best to find the proper calbiration.

# Voltage Reading

The Batt+ terminal accepts a positive 12v battery lead, which then runs through a simple divider circuit to drop the maximum voltage below the 3.3 ADS source voltage, and fed into the ADS1115. The reading is then multiplied back to original values in software. The Batt- terminal grounds the remaining ADS input channel and bridges the ground of both the Raspberry Pi and the 12v system.

# Battery Capacity

One of the challenges of battery monitoring is battery "capacity", and actually the only real data that one might really care about. Built in, simple battery monitors only show capacity based on a basic voltage scale. 12.76 = 100% capacity, 12.5V = 90%, etc.. As voltage drops, capacity is shown to drop. In practical usage this is not accurate as load on a battery also drops voltage but doesn't necessarilly indicate an equivalent "capacity" drop. For instance, a fullly topped off batter with a 10 amp load will drop to an indicated 12.1 volts, and slowly return back to 12.6 after the load removed. This script will calculate capacity more accurately by comparing voltage and amperage output to determine a more realistic capacity. In our example, 12.1 volts while at 10 amps load will still equal approximately 100% capacity.

# Monitoring and what to do with all this data

The intent of this system is to see at a glance the current voltage and capacity of the battery, the amperage load off of the battery, and the charging load into the battery from the AC converter and the solar charging controller. Additionally, a historical graph, and calculated amp hour usage statistics would be beneficial.

This scenario for monitoring includes a wifi connected Raspberry Pi running the monitoring script and also running a self contained Influx database and Grafana instance. The Influx database should be set with a very low retention policy to avoid data growth. The local Grafana instance will pull from the influx database and show a real-time, and recent history capture of all data. This local instance will allow functionality while "off grid" and unable to connect to a remote server. A web browser can view the grafana instance locally, or a mounted display could be made to view data in real time.

An extended scenario also sends data to an external Influx/Grafana system to allow remote monitoring, provided the wifi network has internet connectivity. This remote influx/grafana system can save date for longer periods and show more historical information. With sufficient solar charging, the system can run indefinitely with the Raspberry Pi running off a 12v - 5v buck converting power supply. 

# Hardware prototyping

After initial prototyping on a breadboard, a printed PCB was designed. This PCB is designed with the exact dimensions of the Raspberry Pi 3 model and will sit directly over the Raspberry Pi utilizing a GPIO extender and standoff mounts. I used EasyEDA.com and ordered PCB boards from JLBPCB.com including SMT building of the ADS chips, and all necessary resistors, capacitors, LEDs, and other components with outstanding results. (Highly Recommended!) Long term use of a breadboard is inadvisable as the poor contacts wreak havoc on the sensitive voltage calculations that must be able to accurately differentiate fractions of millivolts. I still included an onboard SHT humidity and temperature sensor but unsure of the value of this chip at this time. Since all components are I2C based, they coexist nicely.

The PCB includes the 2 ADS1115 sensors and the SHT21 sensor. A decoupler capacitor on the inbound side of the 3.3v power source is used to stabilize incoming power, then both power and ground connections go through a ferrite bead filter. Each sensor then gets its own decoupling capacitor as well. The SCL/ADS lines are bridged and each have a pull up resistor. 12v+ line goes through a voltage divider circuit, and a status LED is included for the script to provide a visual status.

# My most recent PCB design.
![Image of PCB photo](https://raw.githubusercontent.com/bsmith993/RV-Monitor/master/pcbphoto.png)

# Hardware Required
* PCB as designed
* 4x 2 post screw terminals or 8 post terminal
* 1 GPIO extension header
* Appropriate cable to extend from PCB terminals to shunt/battery endpoints
* 1 Raspberry Pi (Model 3 or better suggested)
* Raspberry Pi case with standoffs for mounting the PCB


