import telebot

token = '1770481977:AAGBsilOymdPUhlWnON-Mf2hLro7kRhWizs'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, message.id)
    print(message.chat.id)

bot.polling(none_stop=True)

