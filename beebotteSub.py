import paho.mqtt.client as mqtt
import json
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
    device = json.loads(msg.payload.decode())['data'][0]['DEVICE']
    action = json.loads(msg.payload.decode())['data'][0]['ACTION']
    print(f'{device} --- {action}')


if __name__ == '__main__':

    # Publisherと同様に v3.1.1を利用
    #client = mqtt.Client(client_id = clientID,clean_session=True,userdata=name,protocol=mqtt.MQTTv311,transport="tcp")
    client = mqtt.Client(client_id = clientID,clean_session=True,protocol=mqtt.MQTTv311,transport="tcp")
    client.username_pw_set(username, password=password)
    
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port=port, keepalive=60)

    # 待ち受け状態にする
    client.loop_forever()