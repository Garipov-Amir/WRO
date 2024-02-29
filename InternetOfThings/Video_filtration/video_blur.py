import cv2

cap = cv2.VideoCapture(0)

key = 0
keyStop = 32

while key != keyStop:
    isRead, image = cap.read()

    #cv2.imshow("Original Video", image)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    value_threshold, image_threshold = cv2.threshold(image_gray, 60, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Binary Mask", image_threshold)

    image_gray_blur = cv2.blur(image_gray,(8,8))
    cv2.imshow("Blurred Image", image_gray_blur)

    image_gray_median_blur = cv2.medianBlur(image_gray, 9)
    cv2.imshow("Median Blur", image_gray_median_blur)

    value2, mask2 = cv2.threshold(image_gray_blur, 60, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Blurred Mask", mask2)
    key = cv2.waitKey(20)

cap.release()