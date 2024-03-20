import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
from machine import I2C, Pin
from math import sqrt, atan2, pi, copysign, sin, cos
from mpu9250 import MPU9250
from time import sleep
#adc related
from picozero import Pot # Pot is short for Potentiometer

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("mokka","21800000")
print("connecting in 10 sec")
time.sleep(2)
j=0
while not wlan.isconnected():
    print("connecting ", j)
    time.sleep(1)
    j+=1

sensor = Pin(16, Pin.IN)
#adc related pin configure
dial = Pot(0) # Connected to pin A0 (GP_26)
dialb = Pot(1)
flexs = Pot(2)


mqtt_server = 'broker.emqx.io'
client_id = f'raspberry-pub-{time.time_ns()}'
topic_pub = 'data'
user = "emqx"
password = "public"

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, 1883, user, password)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
while True:
    # addresses 
    MPU = 0x68
    id = 0
    sda = Pin(0)
    scl = Pin(1)

    # 
    # create the I2C
    i2c = I2C(id=id, scl=scl, sda=sda)

    # Scan the bus
    print(i2c.scan())
    m = MPU9250(i2c)
    x = m.acceleration[0]
    y = m.acceleration[1]
    z = m.acceleration[2]
    temp = m.temperature
    temp1 = str(temp)
    gyro_x = m.gyro[0]
    gyro_y = m.gyro[1]
    gyro_z = m.gyro[2]
    magnetometerx = m.magnetic[0]
    magnetometery= m.magnetic[1]
    magnetometerz = m.magnetic[2]
    acc_x = str(x)
    acc_y = str(y)
    acc_z = str(z)
    gyro_x1 = str(gyro_x)
    gyro_y2 = str(gyro_y)
    gyro_z2 = str(gyro_z)
    magnetox = str(magnetometerx)
    magnetoy = str(magnetometery)
    magnetoz = str(magnetometerz)
    values = ('x_axis: '  + acc_x + ';y_axis: '  + acc_y + ';z_axis: '  + acc_z  +
              ';gyro_x: ' + gyro_x1  + ';gyro_y: '  + gyro_y2  + ';gyro_z: '  + gyro_z2
               + ';temp: '  + temp1 + ';Magnetometer_x: ' + magnetox + ';Magnetometer_y: ' + magnetoy +
              ';Magnetometer_z: ' + magnetoz + ';Dial 1: '+ str(dial.value)+ ';Dial 2: '+ str(dialb.value)+';flexs: '+ str(flexs.value)+';')
    
    print(';x_axis: '  + acc_x + ';y_axis: '  + acc_y + ';z_axis: '  + acc_z )
    print(';gyro_x: ' + gyro_x1  + ';gyro_y: '  + gyro_y2  + ';gyro_z: '  + gyro_z2)
    print(';temp: '  + temp1)
    print(';Magnetometer_x: ' + magnetox + ';Magnetometer_y: ' + magnetoy +
              ';Magnetometer_z: ' + magnetoz)
    print(';Dial 1: '+ str(dial.value)+ ';Dial 2: '+ str(dialb.value)+';flexs: '+ str(flexs.value)+';')
    client.publish(topic_pub, values)
    time.sleep(0.4)
