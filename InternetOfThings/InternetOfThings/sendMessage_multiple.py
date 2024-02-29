import telebot
import config
from paho.mqtt import client as mqtt

username_mqtt = 'client18'
password = 'akxhc7vtry'
hostName = 'mqtt.pi40.ru'
port = 1883
clientID = "0983647899013830"
client = mqtt.Client(clientID)
client.username_pw_set(username_mqtt, password)
client.connect(hostName, port)
bot = telebot.TeleBot(config.TOKEN_myBot)

def on_message_temp(client, userdata, msg):
    message = msg.payload.decode()
    bot.send_message(config.BotRoboland2020_chatid, message)

client.on_message = on_message_temp
client.subscribe('client18/test')
client.loop_forever()


