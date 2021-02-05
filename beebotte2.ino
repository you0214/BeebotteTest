//mosquitto_sub -h localhost -t tp1/sub1
//mosquitto_pub -h localhost -t tp1/sub1 -m Hello
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <PubSubClient.h>
#include <Arduino_JSON.h>
#define OnB_LED 4 

JSONVar obj1;

    // WiFi
    const char ssid[] = "HUAWEI P30";
    const char passwd[] = "a5b5a270f902";

    // Pub/Sub
    const char* mqttHost = "mqtt.beebotte.com"; // MQTTのIPかホスト名
    const int mqttPort = 1883;       // MQTTのポート
    const char* mqttUser = "token_EPQeCSWdNwi950h1";
    const char* mqttPassword = "";
    int qos =0;

   WiFiClient wifiClient;
   PubSubClient mqttClient(wifiClient);

    const char* topic =  "lineChatBot/message";     // リクエストするトピック名
    char* payload;                   // 受信データ

    /**
     * Connect WiFi
     */
    void connectWiFi()
    {
        WiFi.begin(ssid, passwd);
        Serial.print("WiFi connecting...");
        while(WiFi.status() != WL_CONNECTED) {
            Serial.print(".");
            delay(100);
        }
        Serial.print(" connected. ");
        Serial.println(WiFi.localIP());
    }
    /*line Message*/
    int lineSend(String replyToken,String message) {

      //String rToken = replyToken.substring(1,replyToken.length()-1);
      Serial.println(replyToken);
      //Serial.println(rToken);

     const char* host = "api.line.me";
     const char* URL = "https://api.line.me/v2/bot/message/reply";
     const char* token = "Bearer CfLvwfkkrYwDYCUvXMPBvRJfiTepJgntQE2x4zOzPbMbcl2UMQSHNPAOqNRUcpcqVldaWT5b6MSO3q/xUDoyoKKpB3XSp/gS60fM7YJVL+RaXH/v6KDARfrFLSwDh54XyRPq035U2lli8FbmzlFIXAdB04t89/1O/w1cDnyilFU=";
     String query = "{\"replyToken\":" + replyToken +",\"messages\":[{\"type\":\"text\",\"text\":\"" + message + "\"}]}";
     Serial.println(query);
     const char* body = query.c_str();
     //obj1=JSON.parse(body);
     
     HTTPClient http;
     http.begin(URL);
     http.addHeader("Content-Type","application/json; charset=UTF-8");
     http.addHeader("Authorization",token);
     int status_code = http.POST((uint8_t*)body, strlen(body));
     Serial.printf("status_code=%d\r\n", status_code);
     http.end();

     return(1);
    }
    /**
     * Connect MQTT
     */
     void callback(char* topic, byte* payload, unsigned int length)
   {
    char td[length+1];
    
     Serial.print("Message arrived in topic: ");
     Serial.println(topic);
     Serial.print("Message:");
   for (int i = 0; i < length; i++)
   {
     td[length] ='\0';
     td[i] = (char)payload[i];
   }
    Serial.println(td);
    Serial.println("-----------------------");

    obj1=JSON.parse(td);
     String result = JSON.stringify(obj1["data"][0]["MESG"]);
     String replytoken = JSON.stringify(obj1["data"][0]["TOKEN"]);
     Serial.println(result);  
     
     
     if(result.equals("\"LED OFF\"")){
                 digitalWrite(OnB_LED, LOW);
                 
     }

     if(result.equals("\"LED ON\"")){
                 digitalWrite(OnB_LED, HIGH);
     }

     lineSend(replytoken,"hello esp32");
     
  }   
    void connectMqtt()
    {
        mqttClient.setServer(mqttHost, mqttPort);
        mqttClient.setCallback(callback);
        Serial.println("Connecting to MQTT...");
        
        while( ! mqttClient.connected() ) {
            
            if (mqttClient.connect("ESP32Client", mqttUser, mqttPassword )) {
                Serial.println("connected"); 
            }
            delay(1000);
    }
    
         mqttClient.subscribe(topic);
}

    void setup() {
        Serial.begin(115200);
        pinMode(OnB_LED, OUTPUT);
        
        // Connect WiFi
        connectWiFi();

        // Connect MQTT
        connectMqtt();
        
    }

    void loop() {
        delay(100);  
        mqttClient.loop();  

    }
