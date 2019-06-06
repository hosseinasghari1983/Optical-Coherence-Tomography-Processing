import serial

ard= serial.Serial('COM5', 115200)
ard.write(1)

