import cv2

cap = cv2.VideoCapture(0)
key = 0
keyStop = 32

while key != keyStop:
    imRead, image = cap.read()
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    value, thresh = cv2.threshold(image_gray, 200, 255, cv2.THRESH_BINARY_INV)
    value2, thresh2 = cv2.threshold(image_gray, 230, 255, cv2.THRESH_BINARY)
    #cv2.imshow("window", image)
    print(image_gray)

    cv2.imshow("window_gray", image_gray)
    cv2.imshow("Binary Mask", thresh)
    cv2.imshow("Thresh 2", thresh2)
    key = cv2.waitKey(20)

