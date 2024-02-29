# import libraries
import cv2
import numpy
import math
from paho.mqtt import client as mqtt
import subprocess
# bool var for bot and pos
bot_ready = False
on_centre = False
on_point = False
on_point_2 = False
on_point_3 = False
on_point_4 = False

# check messafe func
def on_message(client, userdata, message):
    global bot_ready
    bot_message = message.payload.decode()
    print(bot_message)
    if bot_message == "ok":
        bot_ready = True
    print(bot_ready)

#connect to mqtt
username_mqtt = 'techbkirill'
password = 'madshark'
hostName = 'mqtt.pi40.ru'
port = 1883
clientID = "hfrhif"
client = mqtt.Client(clientID)
client.username_pw_set(username_mqtt, password)
client.connect(hostName, port)
client.subscribe("techbkirill/from_bot_to_cam")
client.on_message = on_message

# start cam
key = 1
cap = cv2.VideoCapture(1)
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)

# start loop for mqtt connection
client.loop_start()

#var for calculations
last_angle = '0'
last_distane = '0'
last_global = '0'

last_point_angle = ''
last_dist_point = ''
last_point_angle_2 = ''
last_dist_point_2 = ''
last_point_angle_3 = ''
last_dist_point_3 = ''
last_point_angle_4 = ''
last_dist_point_4 = ''

# loop until 'space' is not clicked
while key != 8:
    # subprocess.run('python3 plate_reader.p', shell=True)
    isRead, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedPoints = cv2.aruco.detectMarkers(gray, dictionary)
# detection of aruco
    if corners != []:
        marker = corners[0][0]
        x1, y1 = marker[0]
        x2, y2 = marker[1]
        x3, y3 = marker[2]
        x4, y4 = marker[3]

        # calculating centre of aruco marker coordinates
        centreX = int((x1 + x3) / 2)
        centreY = int((y1 + y3) / 2)

        # calculating angle for local angle
        cv2.line(image, (x1, y1), (x4, y4), (255, 255, 0), 2)
        cv2.line(image, (x4, y4), (x4, y1), (0, 255, 255), 2)
        hip = math.sqrt((x4 - x1) ** 2 + (y4 - y1) ** 2)
        kat = math.sqrt((x4 - x4) ** 2 + (y4 - y1) ** 2)
        cos = kat / hip
        angle = numpy.arccos(cos)
        angle_degrees = numpy.degrees(angle)
        angle_degrees = int(angle_degrees)

        # statement for clockwise retation on negative and pos
        if y1 > y4:
            angle_degrees = 180 - angle_degrees
        if x4 > x1:
            angle_degrees = -angle_degrees
        cv2.putText(image, str(angle_degrees), (x4, y4), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)

        # calculating distance
        distance = int(math.sqrt((centreX - 320) ** 2 + (centreY - 240) ** 2))
        cv2.putText(image, str(distance), (100, 40), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

        # calculating global angle
        cv2.line(image, (centreX, centreY), (320, 240), (255, 255, 0), 2)
        cv2.line(image, (centreX, centreY), (320, 240), (0, 255, 255), 2)
        hip_global = math.sqrt((centreX - 320) ** 2 + (centreY - 240) ** 2)
        kat_global = math.sqrt((centreX - centreX) ** 2 + (centreY - 240) ** 2)
        if hip_global == 0:
            angle_degrees_global = 0
        else:
            cos_global = kat_global / hip_global
            angle_global = numpy.arccos(cos_global)
            angle_degrees_global = numpy.degrees(angle_global)
            angle_degrees_global = int(angle_degrees_global)

            # statement for checking full clock degree
            if centreX > 320 and centreY > 240:
                angle_degrees_global = 180 - angle_degrees_global
            elif centreX < 320 and centreY > 240:
                angle_degrees_global = 180 + angle_degrees_global
            elif centreX < 320 and centreY < 240:
                angle_degrees_global = 360 - angle_degrees_global
        cv2.putText(image, str(angle_degrees_global), (320, 240), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0, 255, 0), 2)

        # creating point and calculating distance and angle
        cv2.circle(image, (350, 390), 10, (255, 0, 0), -1)
        cv2.circle(image, (350, 100), 10, (255, 0, 0), -1)
        # cv2.circle(image, (100, 160), 10, (255, 0, 0), -1)
        # cv2.circle(image, (100, 350), 10, (255, 0, 0), -1)

        # calculating point 1 angle
        cv2.line(image, (centreX, centreY), (350, 390), (255, 255, 0), 2)
        cv2.line(image, (centreX, centreY), (350, 390), (0, 255, 255), 2)
        hip_point = math.sqrt((centreX - 350) ** 2 + (centreY - 390) ** 2)
        kat_point = math.sqrt((centreX - centreX) ** 2 + (centreY - 390) ** 2)
        if hip_point == 0:
            angle_degrees_point = 0
        else:
            cos_point = kat_point / hip_point
            angle_point = numpy.arccos(cos_point)
            angle_degrees_point = numpy.degrees(angle_point)
            angle_degrees_point = int(angle_degrees_point)

        # statement for checking full clock degree for point 1
            if centreX > 350 and centreY > 390:
                angle_degrees_point = 180 - angle_degrees_point
            elif centreX < 350 and centreY > 390:
                angle_degrees_point = 180 + angle_degrees_point
            elif centreX < 350 and centreY < 390:
                angle_degrees_point = 360 - angle_degrees_point
        cv2.putText(image, str(angle_degrees_point), (540, 350), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0, 255, 0), 2)

        # calc dist for point 1
        distance_point = int(math.sqrt((centreX - 350) ** 2 + (centreY - 390) ** 2))
        cv2.putText(image, str(distance_point), (560, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

        # calculating point 2 angle
        cv2.line(image, (centreX, centreY), (350, 100), (255, 255, 0), 2)
        cv2.line(image, (centreX, centreY), (350, 100), (0, 255, 255), 2)
        hip_point_2 = math.sqrt((centreX - 350) ** 2 + (centreY - 100) ** 2)
        kat_point_2 = math.sqrt((centreX - centreX) ** 2 + (centreY - 100) ** 2)
        if hip_point_2 == 0:
            angle_degrees_point_2 = 0
        else:
            cos_point_2 = kat_point_2 / hip_point_2
            angle_point_2 = numpy.arccos(cos_point_2)
            angle_degrees_point_2 = numpy.degrees(angle_point_2)
            angle_degrees_point_2 = int(angle_degrees_point_2)

        # statement for checking full clock degree for point 2
            if centreX > 350 and centreY > 100:
                angle_degrees_point_2 = 180 - angle_degrees_point_2
            elif centreX < 350 and centreY > 100:
                angle_degrees_point_2 = 180 + angle_degrees_point_2
            elif centreX < 350 and centreY < 100:
                angle_degrees_point_2 = 360 - angle_degrees_point_2
        cv2.putText(image, str(angle_degrees_point_2), (500, 200), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0, 255, 0), 2)

        # dist for point 2
        distance_point_2 = int(math.sqrt((centreX - 350) ** 2 + (centreY - 100) ** 2))
        cv2.putText(image, str(distance_point_2), (560, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

        # # calculating point 3 angle
        # cv2.line(image, (centreX, centreY), (100, 160), (255, 255, 0), 2)
        # cv2.line(image, (centreX, centreY), (100, 160), (0, 255, 255), 2)
        # hip_point_3 = math.sqrt((centreX - 100) ** 2 + (centreY - 160) ** 2)
        # kat_point_3 = math.sqrt((centreX - centreX) ** 2 + (centreY - 160) ** 2)
        # if hip_point_3 == 0:
        #     angle_degrees_point_3 = 0
        # else:
        #     cos_point_3 = kat_point_3 / hip_point_3
        #     angle_point_3 = numpy.arccos(cos_point_3)
        #     angle_degrees_point_3 = numpy.degrees(angle_point_3)
        #     angle_degrees_point_3 = int(angle_degrees_point_3)
        #
        #     # statement for checking full clock degree for point 3
        #     if centreX > 100 and centreY > 160:
        #         angle_degrees_point_3 = 180 - angle_degrees_point_3
        #     elif centreX < 100 and centreY > 160:
        #         angle_degrees_point_3 = 180 + angle_degrees_point_3
        #     elif centreX < 100 and centreY < 160:
        #         angle_degrees_point_3 = 360 - angle_degrees_point_3
        # cv2.putText(image, str(angle_degrees_point_3), (80, 200), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0, 255, 0), 2)
        #
        # # dist for point 3
        # distance_point_3 = int(math.sqrt((centreX - 100) ** 2 + (centreY - 160) ** 2))
        # cv2.putText(image, str(distance_point_3), (80, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        #
        # # calculating point 4 angle
        # cv2.line(image, (centreX, centreY), (100, 350), (255, 255, 0), 2)
        # cv2.line(image, (centreX, centreY), (100, 350), (0, 255, 255), 2)
        # hip_point_4 = math.sqrt((centreX - 100) ** 2 + (centreY - 350) ** 2)
        # kat_point_4 = math.sqrt((centreX - centreX) ** 2 + (centreY - 350) ** 2)
        # if hip_point_4 == 0:
        #     angle_degrees_point_4 = 0
        # else:
        #     cos_point_4 = kat_point_4 / hip_point_4
        #     angle_point_4 = numpy.arccos(cos_point_4)
        #     angle_degrees_point_4 = numpy.degrees(angle_point_4)
        #     angle_degrees_point_4 = int(angle_degrees_point_4)
        #
        #     # statement for checking full clock degree for point 4
        #     if centreX > 100 and centreY > 350:
        #         angle_degrees_point_4 = 180 - angle_degrees_point_4
        #     elif centreX < 100 and centreY > 350:
        #         angle_degrees_point_4 = 180 + angle_degrees_point_4
        #     elif centreX < 100 and centreY < 350:
        #         angle_degrees_point_4 = 360 - angle_degrees_point_4
        # cv2.putText(image, str(angle_degrees_point_4), (80, 320), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0, 255, 0), 2)
        #
        # # dist for point 4
        # distance_point_4 = int(math.sqrt((centreX - 100) ** 2 + (centreY - 350) ** 2))
        # cv2.putText(image, str(distance_point_4), (80, 380), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        #
        # # sending data about point
        if bot_ready == True:

            # marker
            if angle_degrees != last_angle:
                client.publish("techbkirill/angle_bot", angle_degrees)
                last_angle = angle_degrees
                print("Angle Sent")

                # centre
            if angle_degrees_global != last_global:
                client.publish("techbkirill/angle_global", angle_degrees_global)
                last_global = angle_degrees_global
                print("Global Sent")
            if distance != last_distane:
                client.publish("techbkirill/dist", distance)
                last_distane = distance
                print("dist sent")

            # point 1
            if angle_degrees_point != last_point_angle:
                client.publish("techbkirill/angle_point", angle_degrees_point)
                last_point_angle = angle_degrees_point
                print("Angle point Sent")
            if distance_point != last_dist_point:
                client.publish("techbkirill/dist_point", distance_point)
                last_dist_point = distance_point
                print("dist point sent")

            # point 2
            if angle_degrees_point_2 != last_point_angle_2:
                client.publish("techbkirill/angle_point_2", angle_degrees_point_2)
                last_point_angle_2 = angle_degrees_point_2
                print("Angle point 2 Sent")
            if distance_point_2 != last_dist_point_2:
                client.publish("techbkirill/dist_point_2", distance_point_2)
                last_dist_point_2 = distance_point_2
                print("dist point 2 sent")
        #
        #     # point 3
        #     if angle_degrees_point_3 != last_point_angle_3:
        #         client.publish("techbkirill/angle_point_3", angle_degrees_point_3)
        #         last_point_angle_3 = angle_degrees_point_3
        #         print("Angle point 3 Sent")
        #     if distance_point_3 != last_dist_point_3:
        #         client.publish("techbkirill/dist_point_3", distance_point_3)
        #         last_dist_point_3 = distance_point_3
        #         print("dist point 3 sent")
        #
        #     # point 4
        #     if angle_degrees_point_4 != last_point_angle_4:
        #         client.publish("techbkirill/angle_point_4", angle_degrees_point_4)
        #         last_point_angle_4 = angle_degrees_point_4
        #         print("Angle point 4 Sent")
        #     if distance_point_4 != last_dist_point_4:
        #         client.publish("techbkirill/dist_point_4", distance_point_4)
        #         last_dist_point_4 = distance_point_4
        #         print("dist point 4 sent")
        #     bot_ready = False
        #
        # # checking is marker in centre
        # if centreX == 320 and centreY == 240:
        #     on_centre = True
        #     client.publish("techbkirill/on_centre", on_centre)
        #     on_centre = False
        # else:
        #     on_centre = False
        #
        # # sending that bot is on point 1
        # if centreX == 540 and centreY == 350:
        #     on_point = True
        #     client.publish("techbkirill/on_point", on_point)
        #     on_point = False
        # else:
        #     on_point = False
        #
        # # on point 2
        # if centreX == 540 and centreY == 160:
        #     on_point_2 = True
        #     client.publish("techbkirill/on_point_2", on_point_2)
        #     on_point_2 = False
        # else:
        #     on_point_2 = False
        #
        # #on point 3
        # if centreX == 100 and centreY == 160:
        #     on_point_3 = True
        #     client.publish("techbkirill/on_point_3", on_point_3)
        #     on_point_3 = False
        # else:
        #     on_point_3 = False
        #
        # # on point 4
        # if centreX == 100 and centreY == 350:
        #     on_point_4 = True
        #     client.publish("techbkirill/on_point_4", on_point_4)
        #     on_point_4 = False
        # else:
        #     on_point_4 = False

    # showing image
    cv2.imshow("original", image)
    key = cv2.waitKey(1)

# stop loop for mqtt
client.loop_stop()