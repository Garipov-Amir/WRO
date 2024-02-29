import json
from paho.mqtt import client as mqtt
from cv2 import *
import telebot
import pytesseract
from PIL import Image
import math
import numpy
import re
from time import sleep
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
detected = False
start_scaning = False
def on_message(client, userdata, message):
    message_from_bot = message.payload.decode()
    global start_scaning
    global message_bot
    global last_message
    global bot_message
    print(message_from_bot)
    if message_from_bot == 'start':
        start_scaning = True
        last_message = message_from_bot
        print(start_scaning)


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
client.subscribe("techbkirill/start_scanning")
client.on_message = on_message

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


key = 1
cap = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

client.loop_start()
while key != 32:
    isRead, image = cap.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plates = cascade.detectMultiScale(gray)
    if start_scaning == False:
        for plate in plates:
            x, y, w, h = plate
            # value, mask = cv2.threshold(crop, 100, 255, cv2.THRESH_BINARY_INV)
            # cv2.imshow('window_mask', mask)
            imwrite('image.jpg', image)
            print("detected")
            detected = True
        if detected == True:
            bot.send_photo(591060853, photo=open('image.jpg', 'rb'))
            detected = False
            sleep(8)
        cv2.imshow('window', image)
        key = cv2.waitKey(10)
    start_scaning = False

client.loop_stop()