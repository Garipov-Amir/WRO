import telebot
import config
import cv2

bot = telebot.TeleBot(config.TOKEN_myBot)

@bot.message_handler(content_types=['video'])
def photo(message):
    fileID = message.video.file_id
    file_info = bot.get_file(fileID)
    print(file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.mp4", 'wb') as new_file:
        new_file.write(downloaded_file)
    new_file.close()
    bot.send_message(message.chat.id, 'receive')
    cap = cv2.VideoCapture("image.mp4")
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    key = -1
    for c in range(count):
        isRead, image = cap.read()
        cv2.imshow('window', image)
        key = cv2.waitKey(20)
        if key != -1:
            break
    cv2.destroyAllWindows()
    bot.send_message(message.chat.id, 'receive')
bot.polling()
