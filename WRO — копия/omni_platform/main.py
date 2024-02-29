#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import math
import time
import os
from umqtt.robust import MQTTClient


def turn_conterclockwise(angle, motor_left,motor_right, motor_center):
    '''
    1500 градусов - полный оборот робота
    '''
    motor_left.run_angle(100,angle,Stop.BRAKE,False)
    motor_right.run_angle(100,angle,Stop.BRAKE,False)
    motor_center.run_angle(100,angle,Stop.BRAKE,True)


def turn_clockwise(angle, motor_left,motor_right, motor_center):
    '''
    1500 градусов - полный оборот робота
    '''
    motor_left.run_angle(-100,angle,Stop.BRAKE,False)
    motor_right.run_angle(-100,angle,Stop.BRAKE,False)
    motor_center.run_angle(-100,angle,Stop.BRAKE,True)

def run_forward(motor_left,motor_right,motor_center):
    power = 50
    ac = [[0.58, -0.33, 0.33], [-0.58, -0.33, 0.33], [0, 0.67, 0.33]]
    # n = [-x, y, 0]
    n = [1, 0, 0]
    c = [0, 0, 0]
    c[0] = round((ac[0][0] * n[0] + ac[0][1] * n[1] + ac[0][2] * n[2]) * power, 2)
    c[1] = round((ac[1][0] * n[0] + ac[1][1] * n[1] + ac[1][2] * n[2]) * power, 2)
    c[2] = round((ac[2][0] * n[0] + ac[2][1] * n[1] + ac[2][2] * n[2]) * power, 2)
    c[0] = c[0] * 10
    c[1] = c[1] * 10
    c[2] = c[2] * 10
    s=2
    print(c)

    motor_center.run(int(c[2]))
    motor_left.run(int(c[1]))
    motor_right.run(int(c[0]))
    # motor_center.run(0)
    # motor_left.run(-300)
    # motor_right.run(300)
    time.sleep(2)


def run_back(motor_left,motor_right,motor_center):
    power = 50
    ac = [[0.58, -0.33, 0.33], [-0.58, -0.33, 0.33], [0, 0.67, 0.33]]
    # n = [-x, y, 0]
    n = [-1, 0, 0]
    c = [0, 0, 0]
    c[0] = round((ac[0][0] * n[0] + ac[0][1] * n[1] + ac[0][2] * n[2]) * power, 2)
    c[1] = round((ac[1][0] * n[0] + ac[1][1] * n[1] + ac[1][2] * n[2]) * power, 2)
    c[2] = round((ac[2][0] * n[0] + ac[2][1] * n[1] + ac[2][2] * n[2]) * power, 2)
    c[0] = c[0] * 10
    c[1] = c[1] * 10
    c[2] = c[2] * 10
    s=2
    while s>1:
        motor_center.run(int(c[2]))
        motor_left.run(int(c[1]))
        motor_right.run(int(c[0]))
        time.sleep(2)
        s=s-1


def run_left(motor_left,motor_right,motor_center):
    power = 50
    ac = [[0.58, -0.33, 0.33], [-0.58, -0.33, 0.33], [0, 0.67, 0.33]]
    # n = [-x, y, 0]
    n = [0, 1, 0]
    c = [0, 0, 0]
    c[0] = round((ac[0][0] * n[0] + ac[0][1] * n[1] + ac[0][2] * n[2]) * power, 2)
    c[1] = round((ac[1][0] * n[0] + ac[1][1] * n[1] + ac[1][2] * n[2]) * power, 2)
    c[2] = round((ac[2][0] * n[0] + ac[2][1] * n[1] + ac[2][2] * n[2]) * power, 2)
    c[0] = c[0] * 10
    c[1] = c[1] * 10
    c[2] = c[2] * 10
    s=2
    while s>1:
        motor_center.run(int(c[2]))
        motor_left.run(int(c[1]))
        motor_right.run(int(c[0]))
        time.sleep(2.2)
        s=s-1

def run_right(motor_left,motor_right,motor_center):
    power = 50
    ac = [[0.58, -0.33, 0.33], [-0.58, -0.33, 0.33], [0, 0.67, 0.33]]
    # n = [-x, y, 0]
    n = [0, -1, 0]
    c = [0, 0, 0]
    c[0] = round((ac[0][0] * n[0] + ac[0][1] * n[1] + ac[0][2] * n[2]) * power, 2)
    c[1] = round((ac[1][0] * n[0] + ac[1][1] * n[1] + ac[1][2] * n[2]) * power, 2)
    c[2] = round((ac[2][0] * n[0] + ac[2][1] * n[1] + ac[2][2] * n[2]) * power, 2)
    c[0] = c[0] * 10
    c[1] = c[1] * 10
    c[2] = c[2] * 10
    s=2
    while s>1:
        motor_center.run(int(c[2]))
        motor_left.run(int(c[1]))
        motor_right.run(int(c[0]))
        time.sleep(2.2)
        s=s-1

def run_omni_angle(angle, motor_left,motor_right,motor_center):
    angle=(angle+90)*(-1)
    power = 50
    a_r=math.radians(angle)
    y=round(math.cos(a_r),2)
    x=round(math.sin(a_r),2)
    ac = [[0.58, -0.33, 0.33], [-0.58, -0.33, 0.33], [0, 0.67, 0.33]]
    n = [x, -y, 0]
    c = [0, 0, 0]
    c[0] = round((ac[0][0] * n[0] + ac[0][1] * n[1] + ac[0][2] * n[2]) * power, 2)
    c[1] = round((ac[1][0] * n[0] + ac[1][1] * n[1] + ac[1][2] * n[2]) * power, 2)
    c[2] = round((ac[2][0] * n[0] + ac[2][1] * n[1] + ac[2][2] * n[2]) * power, 2)
    c[0] = c[0] * 10
    c[1] = c[1] * 10
    c[2] = c[2] * 10
    motor_center.run(int(c[2]))
    motor_left.run(int(c[1]))
    motor_right.run(int(c[0]))
    time.sleep(1)
    motor_center.stop()
    motor_left.stop()
    motor_right.stop()
    time.sleep(0.2)

def getmessages(topic, msg):
    message = str(msg.decode())
    brick.display.text(message)
    if message == 'f':
        run_omni_angle(180, Mleft,Mright,Mcenter)
    if message == 'l':
        run_omni_angle(90, Mleft,Mright,Mcenter)
    if message == 'b':
        run_omni_angle(0, Mleft,Mright,Mcenter)
    if message == 'r':
        run_omni_angle(270, Mleft,Mright,Mcenter)
    if message == 'q':
        run_omni_angle(135, Mleft,Mright,Mcenter)
    if message == 'e':
        run_omni_angle(225, Mleft,Mright,Mcenter)
    if message == 'z':
        run_omni_angle(45, Mleft,Mright,Mcenter)
    if message == 'c':
        run_omni_angle(315, Mleft,Mright,Mcenter)
    if message == 'x':
        client.publish(topic, "x")



os.system('hostname > /dev/shm/hostname.txt')
file = open('/dev/shm/hostname.txt', 'r')
MQTT_ClientID = file.readline().rstrip('\n')
file.close()
os.system('rm /dev/shm/hostname.txt')

client=MQTTClient(MQTT_ClientID,"mqtt.pi40.ru", user='techbkirill', password='madshark')
client.connect()

client.publish("techbkirill/test1", 'Start...')
client.set_callback(getmessages)
client.subscribe("techbkirill/angle_bot")
client.subscribe("techbkirill/is_zero")

Mcenter=Motor(Port.A)
Mright=Motor(Port.B)
Mleft=Motor(Port.C)
run_omni_angle(45, Mleft,Mright,Mcenter)
# run_omni_angle(90, Mleft,Mright,Mcenter)
# run_omni_angle(270, Mleft,Mright,Mcenter)


while True:
    client.check_msg()
    time.sleep(0.1)