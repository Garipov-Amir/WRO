from paho.mqtt import client as mqtt

username_mqtt = 'techbkirill'
password = 'madshark'
hostName = 'mqtt.pi40.ru'
port = 1883
clientID = "0987899"
client = mqtt.Client(clientID)
client.username_pw_set(username_mqtt, password)
client.connect(hostName, port)

def on_message_angle_bot(client, userdata, msg):
    message = msg.payload.decode()
    print("angle_bot: ", message)

def on_message_angle(client, userdata, msg):
    message = msg.payload.decode()
    print("angle: ", message)

def on_message_distance(client, userdata, msg):
    message = msg.payload.decode()
    print("distance: ", message)

client.message_callback_add('techbkirill/angle_bot', on_message_angle_bot)
client.message_callback_add('techbkirill/angle', on_message_angle)
client.message_callback_add('techbkirill/distance', on_message_distance)
client.subscribe('techbkirill/angle_bot')
client.subscribe('techbkirill/angle')
client.subscribe('techbkirill/distance')
client.loop_forever()