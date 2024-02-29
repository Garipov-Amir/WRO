#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from umqtt.robust import MQTTClient
def getmessages(topic, msg):
    ev3.speaker.beep()
    ev3.screen.clear()
    message = str(msg.decode())
    ev3.screen.print(message)
ev3 = EV3Brick()
client=MQTTClient("robot1","mqtt.pi40.ru", user='techbkirill', password='madshark')
client.connect()
client.publish("techbkirill/test1", 'Start...')
#client.set_callback(getmessages)
client.set_callback(getmessages)
client.subscribe("techbkirill/angle_bot")
client.subscribe("techbkirill/is_zero")
while True:
    client.check_msg()
