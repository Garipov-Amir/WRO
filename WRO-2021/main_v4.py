# import libraries
import cv2
import numpy
import math
from paho.mqtt import client as mqtt
from PIL import Image
# bool var for bot and pos
bot_ready = False
on_centre = False
on_point = False
on_point_2 = False
on_point_3 = False
on_point_4 = False
on_point_5 = False

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
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# start loop for mqtt connection
client.loop_start()

#var for calculations
last_angle = '0['
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
last_point_angle_5 = ''
last_dist_point_5 = ''

y_crop = 200
x_crop = 20
h_crop = 980
w_crop = 1400


frame_width_half = 630
frame_height_half = 360
frame_width_half = int(frame_width_half)
frame_height_half = int(frame_height_half)

points1_x = 820
points1_y = 580

points2_x = 623
points2_y = 460

points3_x = 420
points3_y = 450

points4_x = 623
points4_y = 270

points5_x = 623
points5_y = 120

# loop until 'space' is not clicked
while key != 8:
    # subprocess.run('python3 plate_reader.p', shell=True)
    isRead, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedPoints = cv2.aruco.detectMarkers(gray, dictionary)
    
    # image = image[x_crop:w_crop, y_crop:h_crop]

# detection of aruco
    if corners != []:
        marker = corners[0][0]
        x1, y1 = marker[0]
        x2, y2 = marker[1]
        x3, y3 = marker[2]
        x4, y4 = marker[3]

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        x3 = int(x3)
        y3 = int(y3)
        x4 = int(x4)
        y4 = int(y4)


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
        cv2.putText(image, 'Local angle: ' + str(angle_degrees), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # calculating distance
        distance = int(math.sqrt((centreX - frame_width_half) ** 2 + (centreY - frame_height_half) ** 2))
        cv2.putText(image, 'Distance to the middle of field: ' + str(distance), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # calculating global angle
        cv2.line(image, (centreX, centreY), (frame_width_half, frame_height_half), (255, 255, 0), 2)
        cv2.line(image, (centreX, centreY), (frame_width_half, frame_height_half), (0, 255, 255), 2)
        hip_global = math.sqrt((centreX - frame_width_half) ** 2 + (centreY - frame_height_half) ** 2)
        kat_global = math.sqrt((centreX - centreX) ** 2 + (centreY - frame_height_half) ** 2)
        if hip_global == 0:
            angle_degrees_global = 0
        else:
            cos_global = kat_global / hip_global
            angle_global = numpy.arccos(cos_global)
            angle_degrees_global = numpy.degrees(angle_global)
            angle_degrees_global = int(angle_degrees_global)

            # statement for checking full clock degree
            if centreX > frame_width_half and centreY > frame_height_half:
                angle_degrees_global = 180 - angle_degrees_global
            elif centreX < frame_width_half and centreY > frame_height_half:
                angle_degrees_global = 180 + angle_degrees_global
            elif centreX < frame_width_half and centreY < frame_height_half:
                angle_degrees_global = 360 - angle_degrees_global
        cv2.putText(image, 'Global angle over middle point ' + str(angle_degrees_global), (0, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # creating point and calculating distance and angle
        cv2.circle(image, (points1_x, points1_y), 10, (255, 0, 0), -1)
        cv2.circle(image, (points2_x, points2_y), 10, (255, 0, 0), -1)
        cv2.circle(image, (points3_x, points3_y), 10, (255, 0, 0), -1)
        cv2.circle(image, (points4_x, points4_y), 10, (255, 0, 0), -1)
        cv2.circle(image, (points5_x, points5_y), 10, (255, 0, 0), -1)

        # calculating point 1 angle
        cv2.line(image, (centreX, centreY), (points1_x, points1_y), (255, 255, 0), 2)
        cv2.line(image, (centreX, centreY), (points1_x, points1_y), (0, 255, 255), 2)
        hip_point = math.sqrt((centreX - points1_x) ** 2 + (centreY - points1_y) ** 2)
        kat_point = math.sqrt((centreX - centreX) ** 2 + (centreY - points1_y) ** 2)
        if hip_point == 0:
            angle_degrees_point = 0
        else:
            cos_point = kat_point / hip_point
            angle_point = numpy.arccos(cos_point)
            angle_degrees_point = numpy.degrees(angle_point)
            angle_degrees_point = int(angle_degrees_point)

        # statement for checking full clock degree for point 1
            if centreX > points1_x and centreY > points1_y:
                angle_degrees_point = 180 - angle_degrees_point
            elif centreX < points1_x and centreY > points1_y:
                angle_degrees_point = 180 + angle_degrees_point
            elif centreX < points1_x and centreY < points1_y:
                angle_degrees_point = 360 - angle_degrees_point
        cv2.putText(image, 'Angle over point 1: ' + str(angle_degrees_point), (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # calc dist for point 1
        distance_point = int(math.sqrt((centreX - points1_x) ** 2 + (centreY - points1_y) ** 2))
        cv2.putText(image, 'Distance to point 1: ' + str(distance_point), (0, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # calculating point 2 angle
        cv2.line(image, (centreX, centreY), (points2_x, points2_y), (255, 255, 0), 2)
        cv2.line(image, (centreX, centreY), (points2_x, points2_y), (0, 255, 255), 2)
        hip_point_2 = math.sqrt((centreX - points2_x) ** 2 + (centreY - points2_y) ** 2)
        kat_point_2 = math.sqrt((centreX - centreX) ** 2 + (centreY - points2_y) ** 2)
        if hip_point_2 == 0:
            angle_degrees_point_2 = 0
        else:
            cos_point_2 = kat_point_2 / hip_point_2
            angle_point_2 = numpy.arccos(cos_point_2)
            angle_degrees_point_2 = numpy.degrees(angle_point_2)
            angle_degrees_point_2 = int(angle_degrees_point_2)

        # statement for checking full clock degree for point 2
            if centreX > points2_x and centreY > points2_y:
                angle_degrees_point_2 = 180 - angle_degrees_point_2
            elif centreX < points2_x and centreY > points2_y:
                angle_degrees_point_2 = 180 + angle_degrees_point_2
            elif centreX < points2_x and centreY < points2_y:
                angle_degrees_point_2 = 360 - angle_degrees_point_2
        cv2.putText(image, 'Angle over point 2: ' + str(angle_degrees_point_2), (0, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # dist for point 2
        distance_point_2 = int(math.sqrt((centreX - points2_x) ** 2 + (centreY - points2_y) ** 2))
        cv2.putText(image, 'Distance to point 2: ' + str(distance_point_2), (0, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # calculating point 3 angle
        cv2.line(image, (centreX, centreY), (points3_x, points3_y), (255, 255, 0), 2)
        cv2.line(image, (centreX, centreY), (points3_x, points3_y), (0, 255, 255), 2)
        hip_point_3 = math.sqrt((centreX - points3_x) ** 2 + (centreY - points3_y) ** 2)
        kat_point_3 = math.sqrt((centreX - centreX) ** 2 + (centreY - points3_y) ** 2)
        if hip_point_3 == 0:
            angle_degrees_point_3 = 0
        else:
            cos_point_3 = kat_point_3 / hip_point_3
            angle_point_3 = numpy.arccos(cos_point_3)
            angle_degrees_point_3 = numpy.degrees(angle_point_3)
            angle_degrees_point_3 = int(angle_degrees_point_3)

            # statement for checking full clock degree for point 3
            if centreX > points3_x and centreY > points3_y:
                angle_degrees_point_3 = 180 - angle_degrees_point_3
            elif centreX < points3_x and centreY > points3_y:
                angle_degrees_point_3 = 180 + angle_degrees_point_3
            elif centreX < points3_x and centreY < points3_y:
                angle_degrees_point_3 = 360 - angle_degrees_point_3
        cv2.putText(image, 'Angle over point 3: ' + str(angle_degrees_point_3), (0, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # dist for point 3
        distance_point_3 = int(math.sqrt((centreX - points3_x) ** 2 + (centreY - points3_y) ** 2))
        cv2.putText(image, 'Distance to point 3: ' + str(distance_point_3), (0, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # calculating point 4 angle
        cv2.line(image, (centreX, centreY), (points4_x, points4_y), (255, 255, 0), 2)
        cv2.line(image, (centreX, centreY), (points4_x, points4_y), (0, 255, 255), 2)
        hip_point_4 = math.sqrt((centreX - points4_x) ** 2 + (centreY - points4_y) ** 2)
        kat_point_4 = math.sqrt((centreX - centreX) ** 2 + (centreY - points4_y) ** 2)
        if hip_point_4 == 0:
            angle_degrees_point_4 = 0
        else:
            cos_point_4 = kat_point_4 / hip_point_4
            angle_point_4 = numpy.arccos(cos_point_4)
            angle_degrees_point_4 = numpy.degrees(angle_point_4)
            angle_degrees_point_4 = int(angle_degrees_point_4)

            # statement for checking full clock degree for point 4
            if centreX > points4_x and centreY > points4_y:
                angle_degrees_point_4 = 180 - angle_degrees_point_4
            elif centreX < points4_x and centreY > points4_y:
                angle_degrees_point_4 = 180 + angle_degrees_point_4
            elif centreX < points4_x and centreY < points4_y:
                angle_degrees_point_4 = 360 - angle_degrees_point_4
        cv2.putText(image, 'Angle over point 4: ' + str(angle_degrees_point_4), (0, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # dist for point 4
        distance_point_4 = int(math.sqrt((centreX - points4_x) ** 2 + (centreY - points4_y) ** 2))
        cv2.putText(image, 'Distance to point 4: ' + str(distance_point_4), (0, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


         # calculating point 5 angle
        cv2.line(image, (centreX, centreY), (points5_x, points5_y), (255, 255, 0), 2)
        cv2.line(image, (centreX, centreY), (points5_x, points5_y), (0, 255, 255), 2)
        hip_point_5 = math.sqrt((centreX - points5_x) ** 2 + (centreY - points5_y) ** 2)
        kat_point_5 = math.sqrt((centreX - centreX) ** 2 + (centreY - points5_y) ** 2)
        if hip_point_5 == 0:
            angle_degrees_point_5 = 0
        else:
            cos_point_5 = kat_point_5 / hip_point_5
            angle_point_5 = numpy.arccos(cos_point_5)
            angle_degrees_point_5 = numpy.degrees(angle_point_5)
            angle_degrees_point_5 = int(angle_degrees_point_5)

            # statement for checking full clock degree for point 5
            if centreX > points5_x and centreY > points5_y:
                angle_degrees_point_5 = 180 - angle_degrees_point_5
            elif centreX < points5_x and centreY > points5_y:
                angle_degrees_point_5 = 180 + angle_degrees_point_5
            elif centreX < points5_x and centreY < points5_y:
                angle_degrees_point_5 = 360 - angle_degrees_point_5
        cv2.putText(image, 'Angle over point 5: ' + str(angle_degrees_point_5), (0, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # dist for point 5
        distance_point_5 = int(math.sqrt((centreX - points5_x) ** 2 + (centreY - points5_y) ** 2))
        cv2.putText(image, 'Distance to point 5: ' + str(distance_point_5), (0, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)



        # sending data about point
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

            # point 3
            if angle_degrees_point_3 != last_point_angle_3:
                client.publish("techbkirill/angle_point_3", angle_degrees_point_3)
                last_point_angle_3 = angle_degrees_point_3
                print("Angle point 3 Sent")
            if distance_point_3 != last_dist_point_3:
                client.publish("techbkirill/dist_point_3", distance_point_3)
                last_dist_point_3 = distance_point_3
                print("dist point 3 sent")

            # point 4
            if angle_degrees_point_4 != last_point_angle_4: 
                client.publish("techbkirill/angle_point_4", angle_degrees_point_4)
                last_point_angle_4 = angle_degrees_point_4
                print("Angle point 4 Sent")
            if distance_point_4 != last_dist_point_4:
                client.publish("techbkirill/dist_point_4", distance_point_4)
                last_dist_point_4 = distance_point_4
                print("dist point 4 sent")
            bot_ready = False

            if angle_degrees_point_5 != last_point_angle_5: 
                client.publish("techbkirill/angle_point_5", angle_degrees_point_5)
                last_point_angle_5 = angle_degrees_point_5
                print("Angle point 5 Sent")
            if distance_point_5 != last_dist_point_5:
                client.publish("techbkirill/dist_point_5", distance_point_5)
                last_dist_point_5 = distance_point_5
                print("dist point 5 sent")
            bot_ready = False

        # checking is marker in centre
        if centreX == frame_width_half and centreY == frame_height_half:
            on_centre = True
            client.publish("techbkirill/on_centre", on_centre)
            on_centre = False
        else:
            on_centre = False

        # sending that bot is on point 1
        if centreX == points1_x and centreY == points1_y:
            on_point = True
            client.publish("techbkirill/on_point", on_point)
            on_point = False
        else:
            on_point = False

        # on point 2
        if centreX == points2_x and centreY == points2_y:
            on_point_2 = True
            client.publish("techbkirill/on_point_2", on_point_2)
            on_point_2 = False
        else:
            on_point_2 = False

        #on point 3
        if centreX == points3_x and centreY == points3_y:
            on_point_3 = True
            client.publish("techbkirill/on_point_3", on_point_3)
            on_point_3 = False
        else:
            on_point_3 = False

        # on point 4
        if centreX == points4_x and centreY == points4_y:
            on_point_4 = True
            client.publish("techbkirill/on_point_4", on_point_4)
            on_point_4 = False
        else:
            on_point_4 = False

        if centreX == points5_x and centreY == points5_y:
            on_point_5 = True
            client.publish("techbkirill/on_point_5", on_point_5)
            on_point_5 = False
        else:
            on_point_5 = False

    # showing image
    cv2.imshow("original", image)
    key = cv2.waitKey(1)

# stop loop for mqtt
client.loop_stop()