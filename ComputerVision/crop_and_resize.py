import cv2

capture = cv2.VideoCapture('smart_car.mp4')

for number in range(300):
    isRead, image = capture.read()
    image[50, 550:750] = [0,255,255]
    image[50:250, 550] = [0, 255, 255]
    image[250, 550:750] = [0, 255, 255]
    image[50:250, 750] = [0, 255, 255]
    crop = image[50:250, 550:750]
    #cv2.imshow('window', image)
    crop_resize = cv2.resize(crop, (200*2, 200*2))
    #cv2.imshow('window_crop_resize', crop_resize)

    zone1 = image[0:360, 0:640]
    cv2.imshow('window_zone1', zone1)
    zone2 = image[0:360, 640:1280]
    cv2.imshow('window_zone2', zone2)

    zone3 = image[360:720, 0:640]
    cv2.imshow('window_zone3', zone3)
    zone4 = image[360:720, 640:1280]
    cv2.imshow('window_zone4', zone4)

    cv2.waitKey(30)
capture.release()