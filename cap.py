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

amps = 1
voltage = 12.4

#Calculate battery capacity off of load index
for i in range(9):
    if amps > Batt_Capacity[i][1] and amps <= Batt_Capacity[i][2]:
        print('Battery Load: ' + str(Batt_Capacity[i][0]))
        for j in range(3,14):
            if voltage >= Batt_Capacity[i][j] and voltage < Batt_Capacity[i][j+1]:
                print(Batt_Capacity[i][j])
                print('Battery Capacity: ' + str((j-3)*10))
