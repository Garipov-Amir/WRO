import paho.mqtt.client as mqtt
import math
import serial
import time
# This is the Subscriber

angle_bot = ""
angle_global_center = ""
dist_center = ""
dist_point1 = ""
angle_global_point1 = ""
dist_point2 = ""
angle_global_point2 = ""
dist_point3 = ""
angle_global_point3 = ""
dist_point4 = ""
angle_global_point4 = ""

move_angle = 0
move_time = ""
command = ""
turningBot = False
centering = ""
rotorDir= 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    
def monitorManipulator(client, userdata, msg):
    
    receive_message = msg.payload.decode()
    global rotorDir
    rotorDir = receive_message
    if int(rotorDir) > 0:
        sendRotor = str(rotorDir) + '>'
    else:
        sendRotor = str(abs(int(rotorDir))) + '<'
        
    sRotor = str.encode(sendRotor)
    #serH.write(sRotor)
    print("Rotating with the SHIM of: " + sendRotor)
#Функция отправки угла для подъема первого колена манипулятора

def monitorAngle(client, userdata, msg):
    receive_message = msg.payload.decode()
    global angle_bot
    angle_bot = receive_message
    print("Bot's Angle is: " + angle_bot)
# Функция приема угла робота относительно своей оси
 
def monitorGlobal(client, userdata, msg):
    receive_message = msg.payload.decode()
    global angle_global_center
    angle_global_center = receive_message
    print("Angle to Center is: " + angle_global_center)

def monitorDist(client, userdata, msg):
    receive_message = msg.payload.decode()
    global dist_center
    dist_center = receive_message
    print("Distance from Center is: " + dist_center)
    
#Две функции для определения координат относительно центра камеры

def monitorGlobalPoint1(client, userdata, msg):
    receive_message = msg.payload.decode()
    global angle_global_point1
    angle_global_point1 = receive_message
    print("Angle to Point 1 is: " + angle_global_point1)
    
def monitorDistPoint1(client, userdata, msg):
    receive_message = msg.payload.decode()
    global dist_point1
    dist_point1 = receive_message
    print("Distance from Point 1 is: " + dist_point1)
    
# Прием координат относительно первой точки (прав.нижн)

def monitorGlobalPoint2(client, userdata, msg):
    receive_message = msg.payload.decode()
    global angle_global_point2
    angle_global_point2 = receive_message
    print("Angle to Point 2 is: " + angle_global_point2)

def monitorDistPoint2(client, userdata, msg):
    receive_message = msg.payload.decode()
    global dist_point2
    dist_point2 = receive_message
    print("Distance from Point 2 is: " + dist_point2)
    
# Прием координат относительно второй точки (прав. верхн)

def monitorGlobalPoint3(client, userdata, msg):
    receive_message = msg.payload.decode()
    global angle_global_point3
    angle_global_point3 = receive_message
    print("Angle to Point 3 is: " + angle_global_point3)
    
def monitorDistPoint3(client, userdata, msg):
    receive_message = msg.payload.decode()
    global dist_point3
    dist_point3 = receive_message
    print("Distance from Point 3 is: " + dist_point3)
    
# Прием координат относительно третьей точки (лев.верхн)

def monitorGlobalPoint4(client, userdata, msg):
    receive_message = msg.payload.decode()
    global angle_global_point4
    angle_global_point4 = receive_message
    print("Angle to Point 4 is: " + angle_global_point4)

def monitorDistPoint4(client, userdata, msg):
    receive_message = msg.payload.decode()
    global dist_point4
    dist_point4 = receive_message
    print("Distance from Point 4 is: " + dist_point4)
    
# Прием координат относительно четвертой точки (лев. нижн)


def monitorCommand(client, userdata, msg):
    receive_message = msg.payload.decode()
    global command
    command = receive_message
    print("Current Command is: "+command)
            
def center_self(init_ang):
    global move_angle
    global move_time
    move_time = round(1000/(100/int(dist_center)))
    if int(init_ang) >= 180:
        move_angle = (init_ang - 90)
    elif int(init_ang)< 180:
        move_angle = (init_ang + 270)
    print("Motion Angle is: " +str(move_angle))
    move_atangle(move_angle, move_time)
    time.sleep(3)
    client.publish("techbkirill/from_bot_to_cam", "ok")
    
def goToPoint(angle, dist):
    global move_angle
    global move_time
    move_time = round(1000/(95/int(dist)))
    if angle >= 180:
        move_angle = (angle - 90)
    elif angle < 180:
        move_angle = (angle + 270)
    print("Motion Angle is: " +str(move_angle))
    move_atangle(move_angle, move_time)
    time.sleep(4)
    client.publish("techbkirill/from_bot_to_cam", "ok")
    
def straighten_self(angle):
    turn_time = 0
    counter_angle = 0
    if int(angle) < 0:
        counter_angle = int(angle) * -1
        turn_time = round((13000/(360/counter_angle)))
        mtime = str(turn_time)
        mtime += "/"
        print(mtime)
        msg_timeCount = str.encode(mtime)
        ser.write(msg_timeCount)
    elif int(angle) > 0:
        counter_angle = int(angle)
        turn_time = round((13000/(360/counter_angle)))
        print(turn_time)
        mtime = str(turn_time)
        mtime += "|" 
        print(time)
        msg_timeCl = str.encode(mtime)
        ser.write(msg_timeCl)
    elif int(angle) == 0:
        print("Already at Zero")
    time.sleep(3)
    client.publish("techbkirill/from_bot_to_cam", "ok")

def self_to180(angle):
    turn_time = 0
    counter_angle = 0
    if int(angle) < 0:
        counter_angle = 180 - (int(angle) * -1)
        turn_time = round((13000/(360/counter_angle)))
        mtime = str(turn_time)
        mtime += "/"
        print(mtime)
        msg_timeCount = str.encode(mtime)
        ser.write(msg_timeCount)
    elif int(angle) > 0:
        counter_angle = 180 - int(angle)
        turn_time = round((13000/(360/counter_angle)))
        print(turn_time)
        mtime = str(turn_time)
        mtime += "|" 
        print(time)
        msg_timeCl = str.encode(mtime)
        ser.write(msg_timeCl)
    elif int(angle) == 0:
        print("Already at Zero")
    time.sleep(3)
    client.publish("techbkirill/from_bot_to_cam", "ok")
    
def chargeCar1():
    move_atangle(270, 1400)
    time.sleep(3)
    straighten_self(angle_bot)
    move_atangle(180, 1100)
    time.sleep(3)
    client.publish("techbkirill/hand", "20")
    time.sleep(1)
    move_atangle(97, 450)
    
def chargeCar2():
    move_atangle(270, 1400)
    time.sleep(3)
    straighten_self(angle_bot)
    move_atangle(0, 1970)
    time.sleep(3)
    client.publish("techbkirill/hand", "20")
    time.sleep(1)
    move_atangle(90, 450)
    
def chargeCar3():
    global angle_bot
    move_atangle(90, 1500)
    time.sleep(3)
    straighten_self(angle_bot)
    move_atangle(180, 1700)
    time.sleep(3)
    client.publish("techbkirill/hand", "6")
    time.sleep(1)
    angle_bot = -115
    straighten_self(angle_bot)
    move_atangle(90, 450)
    
    
def chargeCar4():
    global angle_bot
    move_atangle(90, 1200)
    time.sleep(3)
    straighten_self(angle_bot)
    move_atangle(0, 1600)
    time.sleep(3)
    client.publish("techbkirill/hand", "20")
    time.sleep(1)
    angle_bot = 111
    straighten_self(angle_bot)
    move_atangle(90, 650)

def move_atangle(angle, move_time):
    power = 10
    angle_motion = angle
    a_r = math.radians(angle_motion)  # перевод угла в радианы
    y = round(math.cos(a_r), 2)
    x = round(math.sin(a_r), 2)
    ac = [[0.58, -0.33, 0.33], [-0.58, -0.33, 0.33], [0, 0.67, 0.33]]
    n = [-x, y, 0]
    c = [0, 0, 0]
    c[0] = round((ac[0][0] * n[0] + ac[0][1] * n[1] + ac[0][2] * n[2]) * power, 2)
    c[1] = round((ac[1][0] * n[0] + ac[1][1] * n[1] + ac[1][2] * n[2]) * power, 2)
    c[2] = round((ac[2][0] * n[0] + ac[2][1] * n[1] + ac[2][2] * n[2]) * power, 2)
    c[0] = c[0] * 10
    c[1] = c[1] * 10
    c[2] = c[2] * 10
    print(c[0], c[1], c[2])
    message = str(c[0]) + ','+str(c[1])+','+str(c[2])+','+str(move_time)+'*'
    message_send = str.encode(message)
    ser.write(message_send)

username_mqtt = 'techbkirill'
password = 'madshark'
hostName = 'mqtt.pi40.ru'
port = 1883
clientID = "kljljl"
ser = serial.Serial('/dev/ttyACM0', 9600)
#serH = serial.Serial('/dev/ttyACM3',9600)
client = mqtt.Client(clientID)
client.username_pw_set(username_mqtt, password)
client.connect(hostName, port)
client.subscribe("techbkirill/angle_global")
client.subscribe("techbkirill/angle_bot")
client.subscribe("techbkirill/bot_command")
client.subscribe("techbkirill/dist")

client.subscribe("techbkirill/dist_point")
client.subscribe("techbkirill/angle_point")
client.subscribe("techbkirill/dist_point_2")
client.subscribe("techbkirill/angle_point_2")
client.subscribe("techbkirill/dist_point_3")
client.subscribe("techbkirill/angle_point_3")
client.subscribe("techbkirill/dist_point_4")
client.subscribe("techbkirill/angle_point_4")

client.subscribe("techbkirill/hand")
client.subscribe("techbkirill/car")
client.subscribe("techbkirill/test_go")
client.message_callback_add("techbkirill/angle_bot", monitorAngle)
client.message_callback_add("techbkirill/angle_global", monitorGlobal)
client.message_callback_add("techbkirill/dist", monitorDist)
client.message_callback_add("techbkirill/bot_command", monitorCommand)

client.message_callback_add("techbkirill/dist_point", monitorDistPoint1)
client.message_callback_add("techbkirill/angle_point", monitorGlobalPoint1)
client.message_callback_add("techbkirill/dist_point_2", monitorDistPoint2)
client.message_callback_add("techbkirill/angle_point_2", monitorGlobalPoint2)
client.message_callback_add("techbkirill/dist_point_3", monitorDistPoint3)
client.message_callback_add("techbkirill/angle_point_3", monitorGlobalPoint3)
client.message_callback_add("techbkirill/dist_point_4", monitorDistPoint4)
client.message_callback_add("techbkirill/angle_point_4", monitorGlobalPoint4)

client.message_callback_add("techbkirill/hand", monitorManipulator)
# Функции обратного вызова для приема координат от точек
#client.on_message = on_message
client.on_connect = on_connect

client.loop_start()

while True:
    if command == "null" and abs(int(angle_bot)) >= 3:
        straighten_self(angle_bot)
        client.publish("techbkirill/from_bot_to_cam", "ok")
        command = ''
    elif command == "center" and abs(int(angle_bot)) < 5:
        center_self(int(angle_global_center))
        command = ''
    elif command == "point1":
        goToPoint(int(angle_global_point1), dist_point1)
        command = ''
    elif command == "point2" and abs(int(angle_bot)) < 6:
        goToPoint(int(angle_global_point2), dist_point2)
        command = ''
    elif command == "point3" and abs(int(angle_bot)) < 5:
        goToPoint(int(angle_global_point3), dist_point3)
        command = ''
    elif command == "point4" and abs(int(angle_bot)) < 5:
        goToPoint(int(angle_global_point4), dist_point4)
        command = ''
    elif command == "a333aa78" or command == "a333aa55":
        #goToPoint(int(angle_global_point2), dist_point2) 
        #time.sleep(3)
        client.publish("techbkirill/from_bot_to_cam", "ok")
        straighten_self(angle_bot)
        center_self(int(angle_global_center))
        straighten_self(angle_bot)
        client.publish("techbkirill/from_bot_to_cam", "ok")
        goToPoint(int(angle_global_point2), dist_point2)
        straighten_self(angle_bot)
        time.sleep(1)
        chargeCar1()
        command = ''
    elif command == "o000oo77":
        #goToPoint(int(angle_global_point2), dist_point2)
        #time.sleep(3)
        client.publish("techbkirill/from_bot_to_cam", "ok")
        straighten_self(angle_bot)
        center_self(int(angle_global_center))
        straighten_self(angle_bot)
        client.publish("techbkirill/from_bot_to_cam", "ok")
        goToPoint(int(angle_global_point2), dist_point2)
        straighten_self(angle_bot)
        time.sleep(1)
        chargeCar2()
        command = ''
    elif command == "p070bk92":
        client.publish("techbkirill/from_bot_to_cam", "ok")
        straighten_self(angle_bot)
        center_self(int(angle_global_center))
        straighten_self(angle_bot)
        client.publish("techbkirill/from_bot_to_cam", "ok")
        goToPoint(int(angle_global_point1), dist_point1)
        straighten_self(angle_bot)
        time.sleep(1)
        chargeCar3()
        command = ''
    elif command == "a123aa23" or command == "a123aa99":
        client.publish("techbkirill/from_bot_to_cam", "ok")
        straighten_self(angle_bot)
        center_self(int(angle_global_center))
        straighten_self(angle_bot)
        client.publish("techbkirill/from_bot_to_cam", "ok")
        goToPoint(int(angle_global_point1), dist_point1)
        straighten_self(angle_bot)
        time.sleep(1)
        chargeCar4()
        command = ''
    elif command == "letterp" and abs(int(angle_bot)) < 5:
        center_self(int(angle_global_center))
        time.sleep(4)
        straighten_self(angle_bot)
        goToPoint(int(angle_global_point1), dist_point1)
        time.sleep(4)
        straighten_self(angle_bot)
        goToPoint(int(angle_global_point3), dist_point3)
        time.sleep(4)
        straighten_self(angle_bot)
        goToPoint(int(angle_global_point4), dist_point4)
        time.sleep(4)
        straighten_self(angle_bot)
        goToPoint(int(angle_global_point1), dist_point1)
        time.sleep(4)
        command = ''
    
        

