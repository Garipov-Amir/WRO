import telebot
import config
from paho.mqtt import subscribe

username_mqtt = 'client18'
password = 'akxhc7vtry'
hostName = 'mqtt.pi40.ru'
port = 1883

message = subscribe.simple('client18/test',
                           hostname = hostName,
                           port = 1883,
                           client_id="10983647899013830",
                           auth={'username': username_mqtt, 'password': password})
print(message.payload.decode())
bot = telebot.TeleBot(config.TOKEN_myBot)
bot.send_message(config.BotRoboland2020_chatid, message.payload.decode())

bot.polling(none_stop=True)