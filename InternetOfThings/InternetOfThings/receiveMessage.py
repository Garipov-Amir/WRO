import telebot
import config
from paho.mqtt import publish

username_mqtt = 'client18'
password = 'akxhc7vtry'
hostName = 'mqtt.pi40.ru'
port = 1883

bot = telebot.TeleBot(config.TOKEN_myBot)

@bot.message_handler(content_types=['text'])
def send(message):
    print(message.chat.id, message.text)
    publish.single('client18/test',
                    hostname = hostName,
                    port = 1883,
                    client_id="10983647899013830",
                    auth={'username': username_mqtt, 'password': password})

bot.polling(none_stop=True)