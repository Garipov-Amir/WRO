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
import _thread

gl_msg_angle_bot = 0
gl_msg_angle = 0
gl_msg_distance = 0


def getmessages(topic, msg):
    global gl_msg_angle_bot, gl_msg_angle, gl_msg_distance    
    message = msg.decode()
    topic =  topic.decode()
    brick.display.text(str(message))
    print("my topic", topic)
    if topic == "techbkirill/angle_bot": 
        gl_msg_angle_bot = int(message)
        print('angle_bot: ', gl_msg_angle_bot)
        turn_robot(gl_msg_angle_bot,Mleft, Mright, Mcenter)       
    if topic == "techbkirill/angle":
        gl_msg_angle = int(message)
        print('angle: ', gl_msg_angle) 
    if topic == "techbkirill/distance":
        gl_msg_distance = int(message)
        print('distance: ', gl_msg_distance) 


def turn_robot(angle, motor_left,motor_right, motor_center):
    '''
    1500 градусов - полный оборот робота
    '''
    k = -4.17
    motor_left.run_angle(200,int(angle*k),Stop.BRAKE,False)
    motor_right.run_angle(200,int(angle*k),Stop.BRAKE,False)
    motor_center.run_angle(200, int (angle*k),Stop.BRAKE,True)
    client.publish("techbkirill/ready", 'ok')
    gl_msg_angle_bot = ''
    

def run_omni_angle(angle, distance, motor_left,motor_right,motor_center):
    k = 1
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
    time.sleep(distance*k)
    motor_center.stop()
    motor_left.stop()
    motor_right.stop()
    time.sleep(0.2)
    client.publish("techbkirill/ready", 'ok')

ev3 = EV3Brick()
client=MQTTClient("robot1","mqtt.pi40.ru", user='techbkirill', password='madshark')
client.connect()
client.publish("techbkirill/ready", 'ok')
client.set_callback(getmessages)
client.subscribe("techbkirill/angle_bot")
client.subscribe("techbkirill/angle")
client.subscribe("techbkirill/distance")

Mcenter=Motor(Port.A)
Mright=Motor(Port.B)
Mleft=Motor(Port.C)


# turn_robot(-90, Mleft, Mright, Mcenter)
while True:
    client.check_msg()
    # if gl_msg_distance != 0 and gl_msg_angle != 0:
    #     print("!!!")
    #     run_omni_angle(gl_msg_angle, gl_msg_distance, Mleft, Mright, Mcenter)



