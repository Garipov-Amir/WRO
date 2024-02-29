import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_SETTINGS,0 )
key = 0
keyStop = 32

while key != keyStop:
    isRead, image = cap.read()

    cv2.imshow("Original", image)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    value_threshold, image_threshold = cv2.threshold(image_gray, 200, 255, cv2.THRESH_BINARY)
    cv2.imshow("Mask", image_threshold)

    value_thresholdInv, image_thresholdInv = cv2.threshold(image_gray, 25, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Inverse Mask", image_thresholdInv)

    value_thresholdZero, image_thresholdZero = cv2.threshold(image_gray, 60, 255, cv2.THRESH_TOZERO_INV)
    cv2.imshow("To Zero Mask", image_thresholdZero)

    key = cv2.waitKey(20)