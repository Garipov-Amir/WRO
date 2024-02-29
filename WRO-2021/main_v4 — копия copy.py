# import libraries
import cv2
import numpy as np
import math
from paho.mqtt import client as mqtt
from PIL import Image

# calculate centre coordinates
def coordinate_centre(countour):
    rect = cv2.minAreaRect(countour)
    x_centre, y_centre = rect[0]

    return x_centre, y_centre


# variable for color points
red_y = 0
red_x = 0
green_y = 0
green_x = 0
blue_y = 0
blue_x = 0
yellow_x = 0
yellow_y = 0
violet_y = 0
violet_x = 0


# bool var for bot and pos
bot_ready = False
on_centre = False
on_point = False
on_point_2 = False
on_point_3 = False
on_point_4 = False
on_point_5 = False

carnum = ''
# check messafe func
def on_message(client, userdata, message):
    global bot_ready
    global carnum
    # if message.topic == 'techbkirill/from_bot_to_cam':
    bot_message = message.payload.decode()
    print(bot_message)
    if bot_message == "ok":
        bot_ready = True
    print(bot_ready)
    # if message.topic == 'techbkirill/carnum':
    #     carnum = message.payload.decode()
    #     print(carnum)


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
last_point_angle_5 = ''
last_dist_point_5 = ''
last_point_angle_6 = ''
last_dist_point_6 = ''

y_crop = 200
x_crop = 20
h_crop = 980
w_crop = 1400

# frame variables
frame_width_half = 630
frame_height_half = 360
frame_width_half = int(frame_width_half)
frame_height_half = int(frame_height_half)


# points coordinates
points1_x = 820
points1_y = 600

points2_x = 623
points2_y = 460

points3_x = 440
points3_y = 500

points4_x = 623
points4_y = 270

points5_x = 623
points5_y = 140

points6_x = 840
points6_y = 280 

crop_y1 = 80
crop_y2 = 660
crop_x1 = 340
crop_x2 = 910

# loop until 'space' is not clicked
while key != 8:
    # subprocess.run('python3 plate_reader.p', shell=True)
    isRead, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedPoints = cv2.aruco.detectMarkers(gray, dictionary)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    crop = rgb[crop_y1:crop_y2, crop_x1:crop_x2]
    # crop = image[crop_y1:crop_y2, crop_x1:crop_x2]

    
    # define range of colors in RGB
    lower_blue = np.array([125, 119, 0])
    upper_blue = np.array([148, 255, 255])

    lower_green = np.array([59, 160, 0])
    upper_green = np.array([113, 255, 255])

    lower_red = np.array([231, 125, 0])
    upper_red = np.array([255, 255, 255])

    lower_violet = np.array([24, 0, 148])  # 160, 26, 83
    upper_violet = np.array([255, 130, 25])  # 255, 255, 255

    lower_yellow = np.array([30, 154, 184])
    upper_yellow = np.array([47, 255, 255])

    # masks
    green_mask = cv2.inRange(crop, lower_green, upper_green)  
    blue_mask = cv2.inRange(crop, lower_blue, upper_blue)
    red_mask = cv2.inRange(crop, lower_red, upper_red)
    violet_mask = cv2.inRange(crop, lower_violet, upper_violet)
    yellow_mask = cv2.inRange(crop, lower_yellow, upper_yellow)
    mask = blue_mask + green_mask + red_mask + violet_mask + yellow_mask

    # Bitwise-AND mask and original image
    res_red = cv2.bitwise_and(crop, crop, mask=red_mask)
    res_green = cv2.bitwise_and(crop, crop, mask=green_mask)
    res_blue = cv2.bitwise_and(crop, crop, mask=blue_mask)
    res_violet = cv2.bitwise_and(crop, crop, mask=violet_mask)
    res_yellow = cv2.bitwise_and(crop, crop, mask=yellow_mask)


    #contours
    contours_red, h_red = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours_green, h_green = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours_blue, h_blue = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours_violet, h_violet = cv2.findContours(violet_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours_yellow, h_yellow = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    all_contours, h_all = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


    # red contours
    for contour_rd in contours_red:
        points_rd = len(contour_rd)
        x_rd, y_rd, w_rd, h_rd = cv2.boundingRect(contour_rd)
        b_rd = w_rd * h_rd
        rect_rd = cv2.minAreaRect(contour_rd)
        box_rd = cv2.boxPoints(rect_rd)
        box_rd = np.int0(box_rd)
        area_rd = int(rect_rd[1][0] * rect_rd[1][1])
        if area_rd > 1750:
            cv2.circle(crop, (w_rd // 2 + x_rd, h_rd // 2 + y_rd), 7, (0, 255, 0), -1)
            cv2.drawContours(crop, [box_rd], 0, (255, 255, 255), 4)
        if points_rd > 50:
            red_x, red_y = coordinate_centre(contour_rd)

        red_x = int(red_x)
        red_y = int(red_y)

    # green contours
    for contour_gr in contours_green:
        points_gr = len(contour_gr)
        x_gr, y_gr, w_gr, h_gr = cv2.boundingRect(contour_gr)
        b_gr = w_gr * h_gr
        rect_gr = cv2.minAreaRect(contour_gr)
        box_gr = cv2.boxPoints(rect_gr)
        box_gr = np.int0(box_gr)
        area_gr = int(rect_gr[1][0] * rect_gr[1][1])
        if area_gr > 1750:
            cv2.circle(crop, (w_gr // 2 + x_gr, h_gr // 2 + y_gr), 7, (0, 255, 0), -1)
            cv2.drawContours(crop, [box_gr], 0, (255, 255, 255), 4)

        if points_gr > 50:
            green_x, green_y = coordinate_centre(contour_gr)
        green_x = int(green_x)
        green_y = int(green_y)

    # blue contours
    for contour_bl in contours_blue:
        points_bl = len(contour_bl)
        x_bl, y_bl, w_bl, h_bl = cv2.boundingRect(contour_bl)
        b = w_bl * h_bl
        rect_bl = cv2.minAreaRect(contour_bl)
        box_bl = cv2.boxPoints(rect_bl)
        box_bl = np.int0(box_bl)
        area_bl = int(rect_bl[1][0] * rect_bl[1][1])
        if area_bl > 1750:
            cv2.circle(crop, (w_bl // 2 + x_bl, h_bl // 2 + y_bl), 7, (0, 255, 0), -1)
            cv2.drawContours(crop, [box_bl], 0, (255, 255, 255), 4)

        if points_bl > 50:
            blue_x, blue_y = coordinate_centre(contour_bl)
        blue_x = int(blue_x)
        blue_y = int(blue_y)

    # violet contours
    for contour_vl in contours_violet:
        points_vl = len(contour_vl)
        x_vl, y_vl, w_vl, h_vl = cv2.boundingRect(contour_vl)
        b = w_vl * h_vl
        rect_vl = cv2.minAreaRect(contour_vl)
        box_vl = cv2.boxPoints(rect_vl)
        box_vl = np.int0(box_vl)
        area_vl = int(rect_vl[1][0] * rect_vl[1][1])
        if area_vl > 1750:
            cv2.circle(crop, (w_vl // 2 + x_vl, h_vl // 2 + y_vl), 7, (0, 255, 0), -1)
            cv2.drawContours(crop, [box_vl], 0, (255, 255, 255), 4)

        if points_vl > 50:
            violet_x, violet_y = coordinate_centre(contour_vl)
        violet_x = int(violet_x)
        violet_y = int(violet_y)
    # yellow contour
    for contour_yl in contours_yellow:
        points_yl = len(contour_yl)
        x_yl, y_yl, w_yl, h_yl = cv2.boundingRect(contour_yl)
        b_yl = w_yl * h_yl
        rect_yl = cv2.minAreaRect(contour_yl)
        box_yl = cv2.boxPoints(rect_yl)
        box_yl = np.int0(box_yl)
        area_yl = int(rect_yl[1][0] * rect_yl[1][1])
        if area_yl > 1750:
            cv2.circle(crop, (w_yl // 2 + x_yl, h_yl // 2 + y_yl), 7, (0, 255, 0), -1)
            cv2.drawContours(crop, [box_yl], 0, (255, 255, 255), 4)

        if points_yl > 50:
            yellow_x, yellow_y = coordinate_centre(contour_yl)
        yellow_x = int(yellow_x)
        yellow_y = int(yellow_y)

    red_y = int(red_y)
    blue_y = int(blue_y)
    green_y = int(green_y)
    violet_y = int(violet_y)
    yellow_y = int(yellow_y)

    red_x = int(red_x)
    blue_x = int(blue_x)
    green_x = int(green_x)
    violet_x = int(violet_x)
    yellow_x = int(yellow_x)

    cv2.line(crop, (green_x, green_y), (yellow_x, yellow_y), (200, 0, 0), 2)
    cv2.line(crop, (yellow_x, yellow_y),(blue_x, blue_y), (200, 0, 0), 2)
    cv2.line(crop, (violet_y, violet_y), (red_x, red_y), (200, 0, 0), 2)

    distance_yl_to_gr = int(math.sqrt((yellow_x - green_x) ** 2 + (yellow_y - green_y) ** 2))
    distance_gr_to_bl = int(math.sqrt((yellow_x - green_x) ** 2 + (yellow_y - green_y) ** 2))
    distance_vl_to_rd = int(math.sqrt((yellow_x - green_x) ** 2 + (yellow_y - green_y) ** 2))
    cv2.putText(crop, str(distance_yl_to_gr), (100,40), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 1)



    # if carnum == 'k656mc':
    #     if distance_vl_to_rd <= 160:
    #         client.publish('techbkirill/status', 'Зарядка невозможна')
    #     else: 
    #         client.publish('techbkirill/status', 'Начинается процесс зарядки')
    # elif carnum == 'e542pm':
    #     if distance_gr_to_bl <= 220: 
    #         client.publish('techbkirill/status', 'Зарядка невозможна')
    #     else: 
    #         client.publish('techbkirill/status', 'Начинается процесс зарядки')
    # elif carnum == 'k752cx' or carnum == 'm910cc':
    #     if distance_vl_to_rd <= 220: 
    #         client.publish('techbkirill/status', 'Зарядка невозможна')
    #     else: 
    #         client.publish('techbkirill/status', 'Начинается процесс зарядки')
    #     # image = image[x_crop:w_crop, y_crop:h_crop]

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

        grid_x1 = x1 - 30
        grid_y1 = y1 - 50

        grid_x2 = x2 + 30
        grid_y2 = y2 - 50

        grid_x3 = x3 + 30
        grid_y3 = y3 + 50

        grid_x4 = x4 - 30
        grid_y4 = y4 + 50

        grid_x1 = int(grid_x1)
        grid_y1 = int(grid_y1)

        grid_x2 = int(grid_x2)
        grid_y2 = int(grid_y2)

        grid_x3 = int(grid_x3)
        grid_y3 = int(grid_y3)

        grid_x4 = int(grid_x4)
        grid_y4 = int(grid_y4)

        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0))
        cv2.line(image, (x2, y2), (x3, y3), (0, 255, 0))
        cv2.line(image, (x3, y3), (x4, y4), (0, 255, 0))
        cv2.line(image, (x4, y4), (x1, y1), (0, 255, 0))

        centrey_1 = y1 + ((y4 - y1) / 2) 
        centrey_2 = y2 + ((y3 - y2) / 2)

        centrey_1 = int(centrey_1)
        centrey_2 = int(centrey_2)


        cv2.circle(image, (x1, y2), 3, (255, 0 ,0 ) , -1)

        # calculating centre of aruco marker coordinates
        centreX = int((x1 + x3) / 2)
        centreY = int((y1 + y3) / 2)



        

        # calculating angle for local angle
        cv2.line(image, (x1, y1), (x4, y4), (255, 255, 0), 2)
        cv2.line(image, (x4, y4), (x4, y1), (0, 255, 255), 2)
        hip = math.sqrt((x4 - x1) ** 2 + (y4 - y1) ** 2)
        kat = math.sqrt((x4 - x4) ** 2 + (y4 - y1) ** 2)
        cos = kat / hip
        angle = np.arccos(cos)
        angle_degrees = np.degrees(angle)
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
            angle_global = np.arccos(cos_global)
            angle_degrees_global = np.degrees(angle_global)
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
        cv2.circle(image, (points6_x, points6_y), 10, (255, 0, 0), -1)


        # calculating point 1 angle
        cv2.line(image, (centreX, centreY), (points1_x, points1_y), (255, 255, 0), 2)
        cv2.line(image, (centreX, centreY), (points1_x, points1_y), (0, 255, 255), 2)
        hip_point = math.sqrt((centreX - points1_x) ** 2 + (centreY - points1_y) ** 2)
        kat_point = math.sqrt((centreX - centreX) ** 2 + (centreY - points1_y) ** 2)
        if hip_point == 0:
            angle_degrees_point = 0
        else:
            cos_point = kat_point / hip_point
            angle_point = np.arccos(cos_point)
            angle_degrees_point = np.degrees(angle_point)
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
            angle_point_2 = np.arccos(cos_point_2)
            angle_degrees_point_2 = np.degrees(angle_point_2)
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
            angle_point_3 = np.arccos(cos_point_3)
            angle_degrees_point_3 = np.degrees(angle_point_3)
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
            angle_point_4 = np.arccos(cos_point_4)
            angle_degrees_point_4 = np.degrees(angle_point_4)
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
            angle_point_5 = np.arccos(cos_point_5)
            angle_degrees_point_5 = np.degrees(angle_point_5)
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


# calculating point 6 angle
        cv2.line(image, (centreX, centreY), (points6_x, points6_y), (255, 255, 0), 2)
        cv2.line(image, (centreX, centreY), (points6_x, points6_y), (0, 255, 255), 2)
        hip_point_6 = math.sqrt((centreX - points6_x) ** 2 + (centreY - points6_y) ** 2)
        kat_point_6 = math.sqrt((centreX - centreX) ** 2 + (centreY - points6_y) ** 2)
        if hip_point_6 == 0:
            angle_degrees_point_6 = 0
        else:
            cos_point_6 = kat_point_6 / hip_point_6
            angle_point_6 = np.arccos(cos_point_6)
            angle_degrees_point_6 = np.degrees(angle_point_6)
            angle_degrees_point_6 = int(angle_degrees_point_6)

            # statement for checking full clock degree for point 6
            if centreX > points6_x and centreY > points6_y:
                angle_degrees_point_6 = 180 - angle_degrees_point_6
            elif centreX < points6_x and centreY > points6_y:
                angle_degrees_point_6 = 180 + angle_degrees_point_3
            elif centreX < points6_x and centreY < points3_y:
                angle_degrees_point_6 = 360 - angle_degrees_point_6
        cv2.putText(image, 'Angle over point 6: ' + str(angle_degrees_point_6), (0, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # dist for point 6
        distance_point_6 = int(math.sqrt((centreX - points6_x) ** 2 + (centreY - points6_y) ** 2))
        cv2.putText(image, 'Distance to point 6: ' + str(distance_point_6), (0, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

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

            if angle_degrees_point_6 != last_point_angle_6: 
                client.publish("techbkirill/angle_point_6", angle_degrees_point_6)
                last_point_angle_6 = angle_degrees_point_6
                print("Angle point 6 Sent")
            if distance_point_6 != last_dist_point_6:
                client.publish("techbkirill/dist_point_6", distance_point_6)
                last_dist_point_6 = distance_point_6
                print("dist point 6 sent")
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
    # cv2.imshow('crop', crop)
    cv2.imshow("original", image)
    key = cv2.waitKey(1)

# stop loop for mqtt
client.loop_stop()