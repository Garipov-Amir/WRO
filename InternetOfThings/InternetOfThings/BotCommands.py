import telebot
import config

bot = telebot.TeleBot(config.TOKEN_myBot)
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('/start', '/info')
keyboard.row('/send', 'Hey')

@bot.message_handler(commands=['start'])
def start(message):
    print(message.chat.id, message.text)
    bot.send_message(message.chat.id, "Bot Launched", reply_markup= keyboard)

@bot.message_handler(commands=['info'])
def send(message):
    print(message.chat.id, message.text)
    inline = telebot.types.InlineKeyboardMarkup()
    item1 = telebot.types.InlineKeyboardButton(text='INFO1', callback_data='info1')
    item2 = telebot.types.InlineKeyboardButton(text='INFO2', callback_data='info2')

    inline.add(item1, item2)
    bot.send_message(message.chat.id, "I am a bot for IOT!", reply_markup=inline)

@bot.callback_query_handler(func= lambda call: True)
def answer(call):
    if call.data == 'info1':
        bot.send_message(call.message.chat.id, "My name is Bots")
    if call.data == 'info2':
        bot.send_message(call.message.chat.id, "I am a programm")
bot.polling(none_stop=True)
