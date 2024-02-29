#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
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

def getmessages(topic, msg):
    message = msg.decode()
    brick.display.text(str(message))
    if topic == "tehbkiril/angle_bot": 
        #message = str(msg.decode())
        if abs(message) > 5:
            turn_clockwise(int(message),Mleft, Mright, Mcenter)
# def getmessages(topic, msg):
#     ev3.speaker.beep()
#     ev3.screen.clear()
#     message = str(msg.decode())
#     ev3.screen.print(message)
ev3 = EV3Brick()
client=MQTTClient("robot1","mqtt.pi40.ru", user='techbkirill', password='madshark')
client.connect()
client.publish("techbkirill/test1", 'Start...')
client.set_callback(getmessages)
client.subscribe("techbkirill/angle_bot")
client.subscribe("techbkirill/is_zero")

def turn_conterclockwise(angle, motor_left,motor_right, motor_center):
    '''
    1500 градусов - полный оборот робота
    '''
    k = 3
    motor_left.run_angle(100,angle*3,Stop.BRAKE,False)
    motor_right.run_angle(100,angle*3,Stop.BRAKE,False)
    motor_center.run_angle(100,angle*3,Stop.BRAKE,True)


def turn_clockwise(angle, motor_left,motor_right, motor_center):
    '''
    1500 градусов - полный оборот робота
    '''
    motor_left.run_angle(-100,angle,Stop.BRAKE,False)
    motor_right.run_angle(-100,angle,Stop.BRAKE,False)
    motor_center.run_angle(-100,angle,Stop.BRAKE,True)

def turn_robot(angle, motor_left,motor_right, motor_center):
    '''
    1500 градусов - полный оборот робота
    '''
    k = 4.17
    motor_left.run_angle(100,int(angle*k),Stop.BRAKE,False)
    motor_right.run_angle(100,int(angle*k),Stop.BRAKE,False)
    motor_center.run_angle(100, int (angle*k),Stop.BRAKE,True)
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



    # run_omni_angle(180, Mleft,Mright,Mcenter)
    # run_omni_angle(90, Mleft,Mright,Mcenter)
    # run_omni_angle(270, Mleft,Mright,Mcenter)

    # Our program starts here
Mcenter=Motor(Port.A)
Mright=Motor(Port.B)
Mleft=Motor(Port.C)
turn_robot(180,Mleft, Mright, Mcenter)

# run_omni_angle(0,Mleft, Mright, Mcenter)
# turn_conterclockwise(180,Mleft, Mright, Mcenter)
# while True:
#     client.check_msg()
# if "techbkirill/is_zero" != True and "tehbkiril/angle_bot" < 0:
#     turn_conterclockwise(angle_bot, Mleft, Mright, Mcenter)
# elif "techbkirill/is_zero" != True and "techbkirill/angle_bot" > 0:
#     turn_clockwise(angle_bot, Mleft, Mright, Mcenter)


