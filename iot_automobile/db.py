# Python Script for reading and storing data from Arduino Uno
import MySQLdb
import time
import serial

device = '/dev/ttyUSB0'
arduino = serial.Serial(device,9600)
arduino.flush()

previous = ""

while True:
    cur_data = arduino.readline()
    print(cur_data)
    if(cur_data != previous):
        previous = cur_data
        print(previous)
        dbConn = MySQLdb.connect("localhost","pi","","car_db") or die("Could not connect to database")
        
        print (dbConn)
        a_list = cur_data.split()
        print(a_list)
        if(len(a_list) ==2):
            map_object = map(int, a_list)
            values = list(map_object)
            print (values)
            ult_val = values[0]
            ldr_val = values[1]
            with dbConn:
                cursor = dbConn.cursor()
                cursor.execute("INSERT INTO sensorLog (ult_val,ldr_val) VALUES (%d,%d)" % (ult_val,ldr_val))
                dbConn.commit()
                cursor.close()