import paho.mqtt.client as mqtt
import json
import requests
import RPi.GPIO as GPIO

ledPort =4
# -*- coding: utf-8 -*-

host = 'mqtt.beebotte.com'
username = "token_EPQeCSWdNwi950h1"
password = ""
clientID = "Raspberry456"
name ="raspberry"
port = 1883
topic = 'lineChatBot/message'

def on_connect(client, userdata, flags, respons_code):
    print('status {0},{1}'.format(respons_code,userdata))
    client.subscribe(topic)
    
def on_message(client, userdata, msg):
    
    #topic QOS payloadを取得
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if msg.payload.decode() == '[]':
        return
    
    lineData = json.loads(msg.payload.decode())
    token  = lineData['data'][0]['TOKEN']
    message = lineData['data'][0]['MESG']
    
    stickerId ='125'
    packageId = '1'
    resMessage ='了解しました！'
    
    
    print(f'{token} - {message}')
    
    if message == 'LED ON':
        stickerId ='138'
        packageId = '1'
        #GPIO.output(ledPort, 1)

    if message == 'LED OFF':
        stickerId ='125'
        packageId = '1'
        #GPIO.output(ledPort, 0)
    
    
    Url = 'https://api.line.me/v2/bot/message/reply'
    ACCESS_TOKEN = 'CfLvwfkkrYwDYCUvXMPBvRJfiTepJgntQE2x4zOzPbMbcl2UMQSHNPAOqNRUcpcqVldaWT5b6MSO3q/xUDoyoKKpB3XSp/gS60fM7YJVL+RaXH/v6KDARfrFLSwDh54XyRPq035U2lli8FbmzlFIXAdB04t89/1O/w1cDnyilFU=';
    headers ={
      'Content-Type': 'application/json; charset=UTF-8',
      'Authorization': 'Bearer ' + ACCESS_TOKEN,
    }
    
    #https://developers.line.biz/ja/reference/messaging-api/#leave-room
    
    obj = {
       'replyToken': token,
       'messages': [
           #{
        #'type': 'text',
        #'text': resMessage,
      #},
                    {
        'type':'sticker',
        'stickerId':stickerId,
        'packageId':packageId,
          }                    
        ]
        }
    json_data = json.dumps(obj).encode("utf-8")
    response = requests.post(Url,headers=headers, data = json_data)
    print(response)    
 
    
    
if __name__ == '__main__':
    #setup
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledPort, GPIO.OUT)


    # Publisherと同様に v3.1.1を利用
    #client = mqtt.Client(client_id = clientID,clean_session=True,userdata=name,protocol=mqtt.MQTTv311,transport="tcp")
    client = mqtt.Client(client_id = clientID,clean_session=True,protocol=mqtt.MQTTv311,transport="tcp")
    client.username_pw_set(username, password=password)
    
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port=port, keepalive=60)

    # 待ち受け状態にする
    client.loop_forever()