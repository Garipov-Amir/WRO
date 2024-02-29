import paho.mqtt.client as mqtt


# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):


    receive_message = msg.payload.decode()
    print(receive_message)
    # if msg.topic == "techbkirill/angle_bot":
    #     global angle_bot
    #     angle_bot = receive_message
    # elif msg.topic == "techbkirill/angle_global":
    #     global angle_global
    #     angle_global = receive_message
    # elif msg.topic == "techbkirill/dist":
    #     global dist
    #     dist = receive_message
    # print("dist: " + str(dist) + " angle_bot: " + str(angle_bot) + " angle_global: " + str(angle_global))
    #


username_mqtt = 'techbkirill'
password = 'madshark'
hostName = 'mqtt.pi40.ru'
port = 1883
clientID = "jdkjdvkjdvkd"
client = mqtt.Client(clientID)
client.username_pw_set(username_mqtt, password)
client.connect(hostName, port)
client.subscribe("techbkirill/#")

client.on_message = on_message
client.on_connect = on_connect



client.loop_forever()
