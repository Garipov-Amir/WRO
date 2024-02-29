import socket
import cv2
import numpy as np
import telebot
s=socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
#Bind port:
s.bind (("127.0.0.1", 9999))
print ("bind udp on 9999 ...")
while True:
 #Receive data:
   data, addr=s.recvfrom (400000)
   nparr = np.fromstring(data, np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

   cv2.imshow ("result", img)
   cv2.waitKey(200)
