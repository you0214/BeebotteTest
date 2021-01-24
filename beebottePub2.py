from time import sleep
import paho.mqtt.client as mqtt
#import ssl

host = 'mqtt.beebotte.com'
username = "token_EPQeCSWdNwi950h1"
password = ""
clientID = "Raspberry123"
name ="raspberry"
port = 1883
topic = 'lineChatBot/message'
qos = 0

#cacert = './cert/ca.crt'
#clientCert = './cert/client.crt'
#clientKey = './cert/client_nopass.key'
# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))
 

# publishが完了したときの処理
def on_publish(client, userdata, mid):
  print("publish: {0},{1}".format(userdata,mid))

# インスタンス作成時に protocol v3.1.1 を指定します
#client = mqtt.Client(client_id = clientID,clean_session=True,userdata=name,protocol=mqtt.MQTTv311,transport="tcp")

client = mqtt.Client(client_id = clientID,clean_session=True,protocol=mqtt.MQTTv311,transport="tcp")
client.username_pw_set(username, password=password)
### SSL
#client.tls_set(cacert,
#  certfile = clientCert,
#  keyfile = clientKey,
#  tls_version = ssl.PROTOCOL_TLSv1_2)
#client.tls_insecure_set(True)

client.on_connect = on_connect         # 接続時のコールバック関数を登録
client.on_publish = on_publish         # メッセージ送信時のコールバック
#client.tls_set()
client.connect(host, port=port, keepalive=60)
client.loop_start()
sleep(1)

res = client.publish(topic, 'testmessage',qos = qos)

print(res)

sleep(2)
client.disconnect()
