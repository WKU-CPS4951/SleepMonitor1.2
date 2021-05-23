import MySQLdb
import os
import serial
import subprocess
import time
import signal
import time
conn = MySQLdb.Connect(host = '127.0.0.1',
                       port = 3306,
                       user = 'root',
                       passwd = '12345',
                       db = 'sleep_monitor',
                       charset='utf8')

sql = "CREATE TABLE newmpu6050(id varchar(10),time varchar(30),accel_x varchar(30),accel_y varchar(30),accel_z varchar(30),gyro_x varchar(30),gyro_y varchar(30),gyro_z varchar(30),temp varchar(30))"

cur = conn.cursor()
cur.execute(sql)
conn.commit()

id=0
maxRecord=60*24/2
p = subprocess.Popen("sudo rfcomm connect /dev/rfcomm0 00:20:12:08:25:66 1",shell=True)
ser = serial.Serial("/dev/rfcomm0",9600)
time.sleep(5)
print("cnm1")
while True:
    if id<maxRecord:
        try:
            buffer = ser.readline(ser.in_waiting)
            temp = buffer.decode('gb18030')
            Acc_X = str(temp).strip().split(":")[0]
            Acc_Y = str(temp).strip().split(":")[1]
            Acc_Z = str(temp).strip().split(":")[2]
            Gyro_X = str(temp).strip().split(":")[3]
            Gyro_Y = str(temp).strip().split(":")[4]
            Gyro_Z = str(temp).strip().split(":")[5]
            Temp = str(temp).strip().split(":")[6]
            cur = conn.cursor()
            nowTime=time.time()
            into = "INSERT INTO newmpu6050(id,time,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (id, nowTime,Acc_X,Acc_Y,Acc_Z,Gyro_X,Gyro_Y,Gyro_Z,Temp)
            cur.execute(into, values)
            conn.commit()
            id=id+1
        except:
            into = "INSERT INTO newmpu6050(id,time,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # values = ('id','time',accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp)
            values = (id, nowTime, None, None, None, None, None, None, None)
            cur.execute(into, values)
            conn.commit()
            id = id + 1
    if id>=maxRecord:
        try:
            sensor = mpu6050(0x68)
            accelerometer_data = sensor.get_all_data()
            sql = "DELETE FROM newmpu6050 WHERE id='%d'" % (id - maxRecord)
            cur.execute(sql)
            conn.commit()
            buffer = ser.readline(ser.in_waiting)
            temp = buffer.decode('gb18030')
            Acc_X = str(temp).strip().split(":")[0]
            Acc_Y = str(temp).strip().split(":")[1]
            Acc_Z = str(temp).strip().split(":")[2]
            Gyro_X = str(temp).strip().split(":")[3]
            Gyro_Y = str(temp).strip().split(":")[4]
            Gyro_Z = str(temp).strip().split(":")[5]
            Temp = str(temp).strip().split(":")[6]
            cur = conn.cursor()
            nowTime = time.time()
            into = "INSERT INTO newmpu6050(id,time,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (id, nowTime,Acc_X,Acc_Y,Acc_Z,Gyro_X,Gyro_Y,Gyro_Z,Temp)
            cur.execute(into, values)
            conn.commit()
            id = id + 1
        except:
            conn.rollback()
            into = "INSERT INTO newmpu6050(id,time,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # values = ('id','time',accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp)
            values = (id, nowTime, None, None, None, None, None, None, None)
            cur.execute(into, values)
            conn.commit()
            id = id + 1
    time.sleep(30)