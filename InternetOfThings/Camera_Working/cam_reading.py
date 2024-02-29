import cv2

cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(1)
key_stop = 32
key = 0
while key != key_stop:
    isRead, image = cam1.read()
    isRead2, image2 = cam2.read()
    cv2.imshow('window', image)
    cv2.imshow('window1', image2)
    key = cv2.waitKey(25)
cam1.release()
cam2.release()