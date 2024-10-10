#아두이노에서 가져온 시리얼데이터(센서값)를 파이썬으로 가져오는 코드입니다.
import serial
import os
import pandas

ser = serial.Serial('/dev/cu.usbmodem1101', 9600)

#print(ser) 시리얼 출력
line = ser.readlines().decode('utf-8').strip()
data = line.split(',')

if len(data) == 11:
    year = int(data[0])
    month = int(data[1])
    day = int(data[2])
    hour = int(data[3])
    minute = int(data[4])
    second = int(data[5])
    temperature_in = float(data[6])
    humidity_in = float(data[7])
    temperature_ex = float(data[8])
    humidity_ex = float(data[9])
    


