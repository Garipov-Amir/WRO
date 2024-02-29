#include <ESP8266WiFi.h>
#include <PubSubClient.h>

String login = "RoboLand";
String password = "sibrland";
const char* hostname = "mqtt.pi40.ru";
const char* client_id = "arywgsasdxs";
const char* username = "techbkirill";
const char* passwrd = "madshark";
const char* topic = "techbkirill/car1";
const int port = 1883;
char message[100];
const int ledPin = D1;
int i;

WiFiClient espClient;
PubSubClient client(espClient);
void message_receiving(char* topic, byte* payload, unsigned int length)
{
  for (i = 0; i < length; i++)
  {
    message[i] = payload[i];
  }
  //message[i] = '\0';
  Serial.println(message);
  digitalWrite(ledPin, HIGH);
  delay(1000);
  digitalWrite(ledPin, LOW);
}

void setup() {
  WiFi.begin(login, password);
    Serial.begin(115200);
  while(WiFi.status() !=WL_CONNECTED) {
    Serial.print("no connection");
    delay(1000);
  }
  Serial.println();
  Serial.print(WiFi.localIP());
  client.setServer(hostname, port);
  Serial.begin(115200);
  client.setCallback(message_receiving);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  if (client.connected() == 0) {
    client.connect(client_id, username, passwrd);
  }
  client.subscribe(topic);
  client.loop();
}
