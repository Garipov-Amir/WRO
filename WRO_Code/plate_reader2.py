from paho.mqtt import client as mqtt
import cv2
import pytesseract
import numpy
import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import socket

message_bot = ''
is_ready = False
on_point_4 = False
start_charge = False
last_message = ''
bot_message = ''
last_x_coordinate = 0
last_y_coordinate = 0


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
while key != 32:
    isRead, image = cap.read()


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plates = cascade.detectMultiScale(gray)
    cv2.circle(image, (320, 240), 5, (0, 255, 0), -1)
    for plate in plates:
        x, y, w, h = plate
        centreX = int((x + (x+w)) / 2)
        centreY = int((y + (y+h)) / 2)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 10)
        crop = gray[y:y+50 + h, x:x+50 + w]
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect('127.0.0.1', 8485)
        connection = client_socket.makefile('wb')
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, frame = cv2.imencode('.jpg', image, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)        # send data:
        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1
        # Receive data:
        s.close()
        img_counter = 0




    cv2.imshow("original", image)
    key = cv2.waitKey(10)

client.loop_stop()