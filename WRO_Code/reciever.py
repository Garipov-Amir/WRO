from paho.mqtt import client as mqtt
angle_bot = ""
angle_global = ""
dist = ""
def on_message(client, userdata, message):
    global run
    receive_message = message.payload.decode()
    print(receive_message)
    if receive_message == 'stop':
        run = False
    if message.topic == "techbkirill/angle_bot":
        global angle_bot
        angle_bot = receive_message
    elif message.topic == "techbkirill/angle_global":
        global angle_global
        angle_global = receive_message
    elif message.topic == "techbkirill/dist":
        global dist
        dist = receive_message
    print("dist: " + str(dist) + " angle_bot: " + str(angle_bot) + " angle_global: " + str(angle_global))

username_mqtt = 'techbkirill'
password = 'madshark'
hostName = 'mqtt.pi40.ru'
port = 1883
clientID = "jdkjdvkjdvkd2"
client = mqtt.Client(clientID)
client.username_pw_set(username_mqtt, password)
client.connect(hostName, port)
client.subscribe("techbkirill/angle_bot")
client.subscribe("techbkirill/dist")
client.subscribe("techbkirill/angle_global")

client.on_message = on_message



run = True
client.loop_start()

while run:
    pass

client.loop_stop()
client.disconnect()
