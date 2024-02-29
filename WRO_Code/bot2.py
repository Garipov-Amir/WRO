import telebot
import paho.mqtt as mqtt
from time import *
import pytesseract
from paho.mqtt import client as mqtt
import socket
import cv2
from PIL import Image
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib

HOST=''
PORT=8485

result = ''
start_charge = False
stop_charge = False
last_coordinateX = 0
last_coordinateY = 0
# bot connect
token = '1770481977:AAGBsilOymdPUhlWnON-Mf2hLro7kRhWizs'
bot = telebot.TeleBot(token)

# mqtt connect
hostname = "mqtt.pi40.ru"
port = 1883
username = "techbkirill"
password = "madshark"
clientID = "nvjrfhruhnv"
client = mqtt.Client('techbkirill')
client.subscribe('techbkirill/carpic')
client.username_pw_set(username, password)
client.connect(hostname, port)

cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')


# start of the bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     f'Добро пожаловать на Enegry Parking! \nВведите пожалуйста номер своей машины латинскими буквами, {message.from_user.first_name}')


@bot.message_handler(content_types=['text'])
def send_reply(message):
    global plates
    if message.text.lower() != '' and len(message.text.lower()) >= 6:
        bot.send_message(message.from_user.id,
        'Спасибо, в скором времени начнется зарядка вашего эллектромобиля \nМы оповестим вас о завершении загрузки.')
        # here will be photo logic
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Bind port:
            s.bind(("127.0.1.1", 9999))
            print("bind udp on 9999 ...")
            # Receive data:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Socket created')

            s.bind((HOST, PORT))
            print('Socket bind complete')
            s.listen(10)
            print('Socket now listening')

            conn, addr = s.accept()

            data = b""
            payload_size = struct.calcsize(">L")
            print("payload_size: {}".format(payload_size))
            while len(data) < payload_size:
                print("Recv: {}".format(len(data)))
                data += conn.recv(4096)
            print("Done Recv: {}".format(len(data)))
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            print("msg_size: {}".format(msg_size))
            while len(data) < msg_size:
                data += conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            gray = cv2.imread(frame, cv2.COLOR_BGR2GRAY)
            gray = Image.fromarray(gray)
            plates = cascade.detectMultiScale(gray)
            for plate in plates:
                x, y, w, h = plate
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 10)
                crop = gray[y:y + 50 + h, x:x + 50 + w]
                centreX = int((x + (x + w)) / 2)
                centreY = int((y + (y + h)) / 2)
                value, mask = cv2.threshold(crop, 100, 255, cv2.THRESH_BINARY_INV)
                cv2.imshow('window_mask', mask)
                text2 = pytesseract.image_to_string(mask, lang='eng')
                if len(text2) >= 6 and text2 != '':
                    print("readed")
                    getVals = list([val for val in text2
                                    if val.isalpha() or val.isnumeric()])

                    text2 = "".join(getVals)
                    text2 = text2.lower()
                    text2 = text2[0:6]
                    if text2 == message.text.lower()[0:6] and len(text2) >= 6:
                        start_charge = True
                        client.publish('techbkirill/start_work', start_charge)
                        start_charge = False
                        sleep(2)
                        stop_charge = True
                        client.publish('techbkirill/stop_charge', stop_charge)
                        stop_charge = False
                        if centreX != last_x_coordinate:
                            client.publish("techbkirill/centreX_plate", centreX)
                            last_x_coordinate = centreX
                            print("Angle carnum Sent")
                        if centreY != last_y_coordinate:
                            client.publish("techbkirill/centreY_plate", centreY)
                            last_y_coordinate = centreY
                            print("dist carnume sent")
        bot.send_message(message.from_user.id, 'Зарядка была успешно произведена!\nХорошего вам дня!')
    else:
        bot.send_message(message.from_user.id, 'Простите, но номер машины должен иметь минимум из 6 символов.')
    print(message.chat.id,
          message.text)


@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    print(file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    new_file.close()
    bot.send_message(message.chat.id, 'receive')
    image = cv2.imread("image.jpg")
    key = -1
    while key == -1:
        cv2.imshow('window', image)
        key = cv2.waitKey()
    cv2.destroyAllWindows()
    bot.send_message(message.chat.id, 'receive')


print('До свидания!')
bot.polling(none_stop=True)
client.loop_forever()
