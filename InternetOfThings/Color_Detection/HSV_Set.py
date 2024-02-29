import cv2
import numpy

def create_window():
    cv2.namedWindow('Settings')
    cv2.resizeWindow('Settings', 400, 350)
    cv2.createTrackbar('H_down', 'Settings', 0, 255, print)
    cv2.createTrackbar('H_up', 'Settings', 255, 255, print)

    cv2.createTrackbar('S_down', 'Settings', 0, 255, print)
    cv2.createTrackbar('S_up', 'Settings', 255, 255, print)

    cv2.createTrackbar('V_down', 'Settings', 0, 255, print)
    cv2.createTrackbar('V_up', 'Settings', 255, 255, print)

def HSV():
    H_down = cv2.getTrackbarPos('H_down', 'Settings')
    H_up = cv2.getTrackbarPos('H_up', 'Settings')

    S_down = cv2.getTrackbarPos('S_down', 'Settings')
    S_up = cv2.getTrackbarPos('S_up', 'Settings')

    V_down = cv2.getTrackbarPos('V_down', 'Settings')
    V_up = cv2.getTrackbarPos('V_up', 'Settings')
    return H_down, H_up, S_down, S_up, V_down, V_up
cap = cv2.VideoCapture(1)

create_window()

key, keyStop = 0, 32

while key != keyStop:
    isRead, image = cap.read()
    cv2.imshow("window", image)

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    H_down, H_up, S_down, S_up, V_down, V_up = HSV()
    HSV_down = numpy.array([H_down, S_down, V_down])
    HSV_up = numpy.array([H_up, S_up, V_up])

    mask = cv2.inRange(image_hsv, HSV_down, HSV_up)
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    image_plus_mask = cv2.bitwise_and(mask_bgr, image)

    cv2.imshow("Mask", mask_bgr)

    key = cv2.waitKey(32)
f = open('HSV_green.txt', 'w')
f.write(str(H_up))
f.write(", ")
f.write(str(H_down))
f.write(", ")
f.write(str(S_up))
f.write(", ")
f.write(str(S_down))
f.write(", ")
f.write(str(V_up))
f.write(", ")
f.write(str(V_down))

f.close()