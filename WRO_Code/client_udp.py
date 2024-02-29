import socket
import cv2
import numpy as np


s=socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
img=cv2.imread ("123.jpg")
img_encode = cv2.imencode(".jpg", img)[1]
data_encode=np.array (img_encode)
data=data_encode.tostring ()
#send data:
s.sendto (data, ("127.0.0.1", 9999))
#Receive data:
print (s.recv (1024) .decode ("utf-8"))
s.close ()

@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    print(file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    new_file.close()
    bot.send_message(message.chat.id, 'receive')
    image = cv2.imread("image.jpg")
    key = -1
    while key == -1:
        cv2.imshow('window', image)
        key = cv2.waitKey()
    cv2.destroyAllWindows()
    bot.send_message(message.chat.id, 'receive')