# RV-Monitor
RV Monitor

This is B. Smitty's RV Monitor.

This python script will monitor the status of a 12v battery, 3 shunt resistors for the purposes of determining amperage in and out
of the battery and charging system, a DHT humidity and temperature sensor, and has one LED output for blinking a status.

The circuit utilizes 2 ADS1115 preassembled boards on a 10 pin, single row header to allow a total of 8 channels
Differential voltage readings are taken on ADS1115_1 A0/A1, ADS1115_1 A2/A3, and ADS1115_2 A0/A1, all at a gain of 16  to read the
current passing through the shunts. Variables allow configuration of shunt resistance. (.00075 = a shunt that allows 75 mV for 100 amps)
Due to the high gain, line voltage loss, and other noise factors, a calibration variable is also required for each shunt reading. Use a 
quality, standalone multimeter to adjust this variable until the ADS readings match actuals.


