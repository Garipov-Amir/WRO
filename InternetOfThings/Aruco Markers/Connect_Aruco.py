import cv2
from cv2 import aruco
import numpy

cap = cv2.VideoCapture(1)
dictionary = aruco.Dictionary_get(aruco.DICT_4X4_50)
key, keystop = 0, 32

while key != keystop:
    isRead,image = cap.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    markersCorners, ids, falsePoints = cv2.aruco.detectMarkers(gray, dictionary)

    number = 10
    if ids is not None and [number] in ids:
        print(ids)
        i = numpy.where(ids == number)
        corners = markersCorners[i[0][0]]

        x1, y1 = corners[0][0]
        x2, y2 = corners[0][1]
        x3, y3 = corners[0][2]
        x4, y4 = corners[0][3]
        x_center = int((x1 + x3) / 2)
        y_center = int((y1 + y3) / 2)
        hypotenuse = [x1 - x4, y1 - y4]
        len_hyp = numpy.linalg.norm(hypotenuse)
        cathet = [x4 - x4, y1 - y4]
        len_cat = numpy.linalg.norm(cathet)
        angle_cos = len_cat / len_hyp
        angle_rad = numpy.arccos(angle_cos)
        angle_degrees = int(numpy.degrees(angle_rad))
        cv2.putText(image, str(angle_degrees), (x_center, y_center), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 2)

    cv2.imshow("Original", image)
    cv2.imshow("Gray", gray)
    key = cv2.waitKey(20)
