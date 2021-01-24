import requests
import pprint
import json
# -*- coding: utf-8 -*-
def main():
    send_Beebotte_API()

def send_Beebotte_API():
    limit = '1'
    source = 'raw'
    timeRange = '1hour'
    beebotteUrl = "https://api.beebotte.com/v1/data/read/lineChatBot/message?limit={0}&source={1}&time-range={2}".format(limit,source,timeRange)
    
    headers ={
        "X-Auth-Token": "token_EPQeCSWdNwi950h1"
    }
    response = requests.get(beebotteUrl,headers=headers)
    td = response.json()[0]['data']
    print(type(td))
    print(td)
if __name__ == "__main__":
    main()
