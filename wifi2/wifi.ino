#include <WiFi.h>
#include <PubSubClient.h>
#include<Arduino.h>
const char* ssid = "AIE_509_2.4G";
const char* password = "addinedu_class1";
const char* mqtt_server = "192.168.0.5";
const int mqtt_port = 1883;
const char* mqtt_user = "jun";
const char* mqtt_password = "gg5860ktm";

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("connected");
      client.subscribe("yourTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n'); // '\n'까지 읽기
    message.trim(); // 시작과 끝의 공백과 줄바꿈 문자 제거
    if (message.length() > 0 && message.startsWith("door")) {
        client.publish("post/door", message.c_str());
    }
    if (message.length() > 0 && message.startsWith("count")) {
        message=message.substring(6);
        client.publish("post/sensor", message.c_str());
    }
    if (message.length() > 0 && message.startsWith("문을")){
      client.publish("post/doorstate", message.c_str());
    }
    }
}
