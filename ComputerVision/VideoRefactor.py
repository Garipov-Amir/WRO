import cv2

capture = cv2.VideoCapture('car.mp4')

for number in range(200):
    isRead, image = capture.read()
    cv2.imshow('window', image)
    cv2.waitKey(16)
capture.release()