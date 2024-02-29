import telebot
import paho.mqtt as mqtt
from time import *
import pytesseract
from paho.mqtt import client as mqtt
import socket
import cv2
import numpy
from PIL import Image
message_bot = ''
is_ready = False
on_point_4 = False
start_charge = False
last_message = ''
bot_message = ''
last_x_coordinate = 0
last_y_coordinate = 0

charge_stoped = False
def on_message(client, userdata, message):
    message_from_bot = message.payload.decode()
    global charge_stoped
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

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
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
client.subscribe('techbkirill/charge_stoped')
client.username_pw_set(username, password)
client.connect(hostname, port)

cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

user_message = ''
image = 0
gray = 0
plates = ''
text2 = ''
result = ''
x, y, w, h = 0, 0, 0, 0


# start of the bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     f'Добро пожаловать на Enegry Parking! \nВведите пожалуйста номер своей машины латинскими буквами, {message.from_user.first_name}')


@bot.message_handler(content_types=['photo'])
def recieve_photo(message_photo):
    global plates
    global gray
    photo_id = message_photo.photo[-1].file_id
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    image = cv2.imread('image.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plates = cascade.detectMultiScale(gray)

@bot.message_handler(content_types=['text'])
def send_reply(message):
    global start_charge
    global last_x_coordinate
    global last_y_coordinate
    if message.text.lower() != '' and len(message.text.lower()) >= 6:
        bot.send_message(message.from_user.id,
        'Спасибо, в скором времени начнется зарядка вашего эллектромобиля \nМы оповестим вас о завершении загрузки.')
        # user_message = str(message.text.lower())
        # for plate in plates:
        for plate in plates:
            global x, y, w, h
            x, y, w, h = plate
        centreX = int((x + (x + w)) / 2)
        centreY = int((y + (y + h)) / 2)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 10)
        crop = gray[y:y + h, x:x + w]
        # value, mask = cv2.threshold(crop, 100, 255, cv2.THRESH_BINARY_INV)
        # cv2.imshow('window_mask', mask)
        text2 = pytesseract.image_to_string(crop, lang='eng')
        print(text2)
        cv2.circle(image, (x, y), 5, (255, 0, 0), -1)
        cv2.circle(image, (x + w, y + h), 5, (255, 0, 0), -1)
        cv2.circle(image, (centreX, centreY), 5, (255, 0, 0), -1)
        if len(text2) >= 6 and text2 != '':
            getVals = list([val for val in text2
                            if val.isalpha() or val.isnumeric()])

            text2 = "".join(getVals)
            text2 = text2.lower()
            text2 = text2[0:6]
            print(text2)
            cv2.putText(image, text2, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)
            print('readed')
            if charge_stoped != False:
                bot.send_message(message.from_user.id, 'Зарядка была успешно произведена!\nХорошего вам дня!')
                if text2 == message.text.lower()[0:6] and len(text2) >= 6:
                    print("readed")
                    if centreX != last_x_coordinate:
                        client.publish("techbkirill/centreX_plate", centreX)
                        last_x_coordinate = centreX
                        print("Angle carnum Sent")
                    if centreY != last_y_coordinate:
                        client.publish("techbkirill/centreY_plate", centreY)
                        last_y_coordinate = centreY
                        print("dist carnume sent")
                    start_charge = True

                client.publish("techbkirill/start_charge", start_charge)
                start_charge = False
    else:
        bot.send_message(message.from_user.id, 'Простите, но номер машины должен иметь минимум из 6 символов.')
    print(message.text.lower()[0:6])


print('До свидания!')
bot.polling(none_stop=True)
client.loop_forever()
