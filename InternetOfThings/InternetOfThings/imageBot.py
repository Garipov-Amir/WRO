import telebot
import config
import cv2

bot = telebot.TeleBot(config.TOKEN_myBot)

@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("../InternetOfThings/image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    new_file.close()
    bot.send_message(message.chat.id, 'receive')

    image = cv2.imread("image.jpg")

    bot.send_message(message.chat.id, str(image[0,0]))
bot.polling()