import telebot
import config

bot = telebot.TeleBot(config.TOKEN_myBot)

@bot.message_handler(content_types=['text'])
def lalala(message):
    print(message.chat.id, message.text)
    bot.send_message(message.chat.id, message.text)

bot.polling(none_stop=True)