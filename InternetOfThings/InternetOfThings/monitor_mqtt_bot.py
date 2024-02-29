import telebot
import config
from paho.mqtt import client as mqtt

username_mqtt = 'techbkirill'
password = 'madshark'
hostName = 'mqtt.pi40.ru'
port = 1883
clientID = "0983647899013830"
client = mqtt.Client(clientID)
client.username_pw_set(username_mqtt, password)
client.connect(hostName, port)
bot = telebot.TeleBot(config.TOKEN_myBot)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    bot.send_message(config.chatid, message)
    print(message)

@bot.message_handler(content_types=['text'])
def send_mqtt(message):
    print(message.chat.id, message.text)
    client.publish('techbkirill/bot', message.text)

client.on_message = on_message
client.subscribe('techbkirill/bot')
client.loop_start()
bot.polling(none_stop=True)
