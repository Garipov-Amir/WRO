import json
from paho.mqtt import client as mqtt
from cv2 import *
import pytesseract
import telebot
from PIL import Image
import math
import numpy
import re
import os
message_bot = ''
is_ready = False
on_point_4 = False
start_charge = False
last_message = ''
bot_message = ''
last_x_coordinate = 0
last_y_coordinate = 0

token = '1770481977:AAGBsilOymdPUhlWnON-Mf2hLro7kRhWizs'
bot = telebot.TeleBot(token)

def on_message(client, userdata, message):
    message_from_bot = message.payload.decode()
    global message_bot
    global is_ready
    global on_point_4
    global last_message
    global bot_message
    print(message_from_bot)
    if message_from_bot == 'ok':
        is_ready = True
        last_message = message_from_bot
        print(is_ready)
    if len(message_from_bot) >= 6:
        message_from_bot = message_from_bot.split('"')
        bot_message = message_from_bot[3]
        bot_message = bot_message.lower()
        print(bot_message)


#connect to mqtt
username_mqtt = 'techbkirill'
password = 'madshark'
hostName = 'mqtt.pi40.ru'
port = 1883
clientID = "vrergre"
client = mqtt.Client(clientID)
client.username_pw_set(username_mqtt, password)
client.connect(hostName, port)
client.subscribe("techbkirill/carnum")
client.subscribe("techbkirill/on_point_4")
client.subscribe("techbkirill/from_bot_to_cam")
client.on_message = on_message

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


key = 1
cap = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

client.loop_start()
while key != 81:
    isRead, image = cap.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plates = cascade.detectMultiScale(gray)
    cv2.circle(image, (320, 240), 5, (0, 255, 0), -1)
    for plate in plates:
        x, y, w, h = plate
        centreX = int((x + (x+w)) / 2)
        centreY = int((y + (y+h)) / 2)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 10)
        crop = gray[y:y+h, x:x+w]
        # value, mask = cv2.threshold(crop, 100, 255, cv2.THRESH_BINARY_INV)
        # cv2.imshow('window_mask', mask)
        text2 = pytesseract.image_to_string(crop, lang='eng')
        cv2.circle(image, (x, y), 5, (255, 0, 0), -1)
        cv2.circle(image, (x + w, y + h), 5, (255, 0, 0), -1)
        cv2.circle(image, (centreX, centreY), 5, (255,0,0),-1)
        if len(text2) >= 6 and text2 != '':
            getVals = list([val for val in text2
                            if val.isalpha() or val.isnumeric()])

            text2 = "".join(getVals)
            text2 = text2.lower()
            text2 = text2[0:6]
            cv2.putText(image, text2, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)


            if text2 == bot_message[0:6] and len(text2) >= 6:
                print("readed")
                start_charge = True
                if centreX != last_x_coordinate:
                    client.publish("techbkirill/centreX_plate", centreX)
                    last_x_coordinate = centreX
                    print("Angle carnum Sent")
                if centreY != last_y_coordinate:
                    client.publish("techbkirill/centreY_plate", centreY)
                    last_y_coordinate = centreY
                    print("dist carnume sent")
                client.publish("techbkirill/start_charge", start_charge)
                start_charge = False
                print("Charge started")
            else:
                start_charge = False

    cv2.imshow("original", image)
    key = cv2.waitKey(10)

client.loop_stop()