import telebot
import config
import cv2
import numpy

def read_values(filename):
    f = open(filename, 'r')
    data = f.read()
    HSV_split = data.split(', ')
    for i in range(6):
        HSV_split[i] = int(HSV_split[i])
    f.close()
    return HSV_split

def proceed_image(imagename, filename):
    contourFound = False
    counter = 0
    h_up, h_down, s_up, s_down, v_up, v_down = read_values(filename)
    HSV_down = numpy.array([h_down, s_down, v_down])
    HSV_up = numpy.array([h_up, s_up, v_up])
    image_hsv = cv2.cvtColor(imagename, cv2.COLOR_BGR2HSV_FULL)
    mask = cv2.inRange(image_hsv, HSV_down, HSV_up)
    contours, service = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        if(len(c) >= 250):
            counter += 1

    return counter


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

    result = proceed_image(image, "../Color_Detection/HSV_yellow.txt")

    bot.send_message(message.chat.id, str(result) + " Yellow Objects Found")
bot.polling()