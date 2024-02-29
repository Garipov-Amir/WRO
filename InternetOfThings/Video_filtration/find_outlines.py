import cv2

cap = cv2.VideoCapture(0)

key = 0
keyStop = 32

while key != keyStop:
    isRead, image = cap.read()
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    value_threshold, image_threshold = cv2.threshold(image_gray, 180, 255, cv2.THRESH_BINARY)
    cv2.imshow("Gray", image_threshold)

    image_gray_blur = cv2.medianBlur(image_threshold, 9)
    cv2.imshow("Blurred Image", image_gray_blur)

    contours, service = cv2.findContours(image_gray_blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print(contours)
    contours2, service2 = cv2.findContours(image_gray_blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, (0,0,255), 1)
    cv2.drawContours(image, contours2, -1, (255,0,0), 1)
    cv2.imshow("Original", image)
    key = cv2.waitKey(20)
cap.release()