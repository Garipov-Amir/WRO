import cv2

cap = cv2.VideoCapture(0)

key_stop = 32
key = 0

while key != key_stop:
    isRead, image = cap.read()
    cv2.line(image, (320, 0), (320, 480), (0, 255, 0), 3)
    cv2.line(image, (0, 240), (640, 240), (0, 255, 0), 3)

    pixelRightTop = image[120, 480]
    blueRT, greenRT, redRT = pixelRightTop
    print(pixelRightTop)
    pixelRightBottom = image[360, 480]
    blueRB, greenRB, redRB = pixelRightBottom

    pixelLeftBottom = image[360, 160]
    blueLB, greenLB, redLB = pixelLeftBottom

    pixelLeftTop = image[160, 120]
    blueLT, greenLT, redLT = pixelLeftTop

    if blueRT < 60 and greenRT < 60 and redRT < 60:
        cv2.putText(image, ' zone 1 ', (320, 50), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255,0), 2)

    if blueRB < 60 and greenRB < 60 and redRB < 60:
        cv2.putText(image, ' zone 2 ', (320, 430), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255,0), 2)

    if blueLB < 60 and greenLB < 60 and redLB < 60:
        cv2.putText(image, ' zone 3 ', (0, 430), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255,0), 2)

    if blueLT < 60 and greenLT < 60 and redLT < 60:
        cv2.putText(image, ' zone 4 ', (0, 50), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255,0), 2)


    cv2.circle(image, (480, 120), 50, (int(blueRT), int(greenRT), int(redRT)), -1) #rightTop
    cv2.circle(image, (480, 360), 50, (int(blueRB), int(greenRB), int(redRB)), -1) #rightBottom
    cv2.circle(image, (160, 360), 50, (int(blueLB), int(greenLB), int(redLB)), -1) #leftBottom
    cv2.circle(image, (160, 120), 50, (int(blueLT), int(greenLT), int(redLT)), -1) #leftTop

    cv2.imshow('window', image)
    key = cv2.waitKey(30)
cap.release()