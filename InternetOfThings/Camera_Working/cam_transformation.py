import cv2

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 20)
cap.set(cv2.CAP_PROP_SATURATION, 100)
cap.set(cv2.CAP_PROP_SETTINGS, 0)

key_stop = 32
key = 0

while key != key_stop:
    isRead, image = cap.read()
    cv2.imshow('window', image)
    key = cv2.waitKey(30)
cap.release()