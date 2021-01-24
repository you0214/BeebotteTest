import requests
import pprint
import json
# -*- coding: utf-8 -*-
#curl -i -H "Content-Type: application/json" -H "X-Auth-Token: チャンネルトークン" 
# -X POST -d '{"data":"データ"}' http://api.beebotte.com/v1/data/publish/チャンネル名/リソース名
def main():
    send_Beebotte_API()

def send_Beebotte_API():
    beebotteUrl = "https://api.beebotte.com/v1/data/publish/lineChatBot/message"
    headers ={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Auth-Token": "token_EPQeCSWdNwi950h1"
    }
    obj = {
        'data': 'hello mac book'
        }
    json_data = json.dumps(obj).encode("utf-8")
    response = requests.post(beebotteUrl,headers=headers, data = json_data)
    print(response)
if __name__ == "__main__":
    main()