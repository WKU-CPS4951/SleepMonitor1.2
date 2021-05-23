import os
import serial
import subprocess
import time
import signal

p = subprocess.Popen("sudo rfcomm connect /dev/rfcomm0 00:20:12:08:25:66 1",shell=True)
(stderr,stdout) = p.communicate()
print('stderr: [%s]' % stderr)
print('stdout: [%s]' % stdout)

print("cnm1")
ser = serial.Serial("/dev/rfcomm0",9600)
time.sleep(5)
if(ser.isOpen()):
    print(-1)
    time.sleep(5)
print(ser.inWaiting())
while (ser.inWaiting() >0):
    buffer = ser.readline(ser.in_waiting)
    print(type(buffer))
    print(len(buffer))
    print(buffer)
    temp = buffer.decode('gb18030')
    print(temp)
    AccX = str(temp).strip().split(":")[0]
    AccY = str(temp).strip().split(":")[1]
    AccZ = str(temp).strip().split(":")[2]
    GyroX = str(temp).strip().split(":")[3]
    GyroY = str(temp).strip().split(":")[4]
    GyroZ = str(temp).strip().split(":")[5]
    Temp = str(temp).strip().split(":")[6]
    print(AccX)
    print(AccY)
    print(AccZ)
    print(GyroX)
    print(GyroY)
    print(GyroZ)
    print(Temp)
    