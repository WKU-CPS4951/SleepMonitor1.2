import MySQLdb
from mpu6050 import mpu6050
import time
conn = MySQLdb.Connect(host = '127.0.0.1',
                       port = 3306,
                       user = 'root',
                       passwd = '12345',
                       db = 'sleep_monitor',
                       charset='utf8')

sql = "CREATE TABLE mpu6050(id varchar(10),time varchar(30),accel_x varchar(30),accel_y varchar(30),accel_z varchar(30),gyro_x varchar(30),gyro_y varchar(30),gyro_z varchar(30),temp varchar(30))"

cur = conn.cursor()
cur.execute(sql)
conn.commit()

id=0
maxRecord=60*24/2
while True:
    if id<maxRecord:
        try:
            sensor = mpu6050(0x68)
            accelerometer_data = sensor.get_all_data()
            accel_x=accelerometer_data[0]['x']
            accel_y=accelerometer_data[0]['y']
            accel_z=accelerometer_data[0]['z']
            gyro_x=accelerometer_data[1]['x']
            gyro_y=accelerometer_data[1]['y']
            gyro_z=accelerometer_data[1]['z']
            temp=accelerometer_data[2]
            print(accelerometer_data)
            cur = conn.cursor()
            nowTime=time.time()
            into = "INSERT INTO mpu6050(id,time,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (id, nowTime,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp)
            cur.execute(into, values)
            conn.commit()
            id=id+1
        except:
            into = "INSERT INTO mpu6050(id,time,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # values = ('id','time',accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp)
            values = (id, nowTime, None, None, None, None, None, None, None)
            cur.execute(into, values)
            conn.commit()
            id = id + 1
    if id>=maxRecord:
        try:
            sensor = mpu6050(0x68)
            accelerometer_data = sensor.get_all_data()
            sql = "DELETE FROM mpu6050 WHERE id='%d'" % (id - maxRecord)
            cur.execute(sql)
            conn.commit()
            accel_x = accelerometer_data[0]['x']
            accel_y = accelerometer_data[0]['y']
            accel_z = accelerometer_data[0]['z']
            gyro_x = accelerometer_data[1]['x']
            gyro_y = accelerometer_data[1]['y']
            gyro_z = accelerometer_data[1]['z']
            temp = accelerometer_data[2]
            print(accelerometer_data)
            cur = conn.cursor()
            nowTime = time.time()
            into = "INSERT INTO mpu6050(id,time,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (id, nowTime, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, temp)
            cur.execute(into, values)
            conn.commit()
            id = id + 1
        except:
            conn.rollback()
            into = "INSERT INTO mpu6050(id,time,accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # values = ('id','time',accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,temp)
            values = (id, nowTime, None, None, None, None, None, None, None)
            cur.execute(into, values)
            conn.commit()
            id = id + 1
    time.sleep(30)
