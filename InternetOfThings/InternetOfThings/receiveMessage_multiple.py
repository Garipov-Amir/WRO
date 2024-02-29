from paho.mqtt import client as mqtt

username_mqtt = 'techbkirill'
password = 'madshark'
hostName = 'mqtt.pi40.ru'
port = 1883
clientID = "0983647899013830"
client = mqtt.Client(clientID)
client.username_pw_set(username_mqtt, password)
client.connect(hostName, port)

#client.subscribe("techbkirill/meteo/temp")

#client.subscribe("techbkirill/meteo/humid")

#client.subscribe("techbkirill/meteo/press")#


client.subscribe("techbkirill/meteo/#")
def proceed_message(client, userdata, msg):
    print(msg.payload)

client.on_message = proceed_message

client.loop_forever()




