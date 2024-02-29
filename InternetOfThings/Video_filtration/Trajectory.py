import cv2
import numpy

def find_fit_rect(image, c):
    rect = cv2.minAreaRect(c)
    points = cv2.boxPoints(rect)
    int_points = numpy.int0(points)
    print(int_points)
    cv2.drawContours(image, [int_points], -1, (255,0, 255), 3)

def find_center(image, c):
    x, y, width, height = cv2.boundingRect(c)
    x_center = int(x + (width/2))
    y_center = int(y + (height/2))
    P = 2*width + 2*height
    if(P>=50):
        cv2.circle(image, (x_center, y_center), 3, (255, 0, 0), -1)
    return x_center, y_center, P

def read_values(filename):
    f = open(filename, 'r')
    data = f.read()
    HSV_split = data.split(', ')
    for i in range(6):
        HSV_split[i] = int(HSV_split[i])
    f.close()
    return HSV_split

cap = cv2.VideoCapture(1)
h_up, h_down, s_up, s_down, v_up, v_down = read_values('HSV_blue.txt')
hg_up, hg_down, sg_up, sg_down, vg_up, vg_down = read_values('HSV_green.txt')

HSV_b_down = numpy.array([h_down, s_down, v_down])
HSV_b_up = numpy.array([h_up, s_up, v_up])

HSV_g_down = numpy.array([hg_down, sg_down, vg_down])
HSV_g_up = numpy.array([hg_up, sg_up, vg_up])
key, keyStop = 0, 32

while key != keyStop:
    isRead, image = cap.read()
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask_b = cv2.inRange(image_hsv, HSV_b_down, HSV_b_up)
    mask_g = cv2.inRange(image_hsv,HSV_g_down, HSV_g_up)

    mask_blue = cv2.cvtColor(mask_b, cv2.COLOR_GRAY2BGR)
    mask_green = cv2.cvtColor(mask_g, cv2.COLOR_GRAY2BGR)
    image_plus_bluemask = cv2.bitwise_and(mask_blue, image)
    image_plus_greenmask = cv2.bitwise_and(mask_green, image)

    contours_blue, service_blue = cv2.findContours(mask_b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours_blue, -1, (0, 255, 255), 2)



    for c in contours_blue:
        x_center, y_center, P = find_center(image, c)
        find_fit_rect(image, c)
        if(P>= 75):
            cv2.putText(image, "Green", (x_center, y_center), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 1)

    cv2.imshow("Original", image)
    cv2.imshow("Blue Highlight", mask_blue)
    cv2.imshow("Green Mask", mask_green)
    key = cv2.waitKey(32)