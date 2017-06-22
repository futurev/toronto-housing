import requests
import json


r_payload = {"latitude1":30.002461804899646,"longitude1":-100.11478763671875,"latitude2":50.588339099337574,"longitude2":-50.60563236328125}
r_payload = {"latitude1":43.700799103429205,"longitude1":-79.5900262451172,"latitude2":43.89903646281729,"longitude2":-79.12997375488283}

headers = {
    "Host": "watch.ohmyhome.ca",
    "Proxy-Connection": "keep-alive",
    "Content-Length": '126',
    "Accept": "application/json, text/plain, */*",
    "Origin": "http://watch.ohmyhome.ca",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": "http://watch.ohmyhome.ca/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.8,fr;q=0.6"
}


## http://watch.ohmyhome.ca/HouseSold/HouseSold.php
## http://watch.ohmyhome.ca/HouseForSale/HouseForSale.php

## http://watch.ohmyhome.ca/CondoSold/CondoSold.php
## http://watch.ohmyhome.ca/CondoForSale/CondoForSale.php


session = requests.session()
r = session.post('http://watch.ohmyhome.ca/CondoSold/CondoSold.php',data=json.dumps(r_payload), headers=headers)

print (r.status_code)
data = json.loads(r.text)


#
#
# {"latitude1":43.700799103429205,"longitude1":-79.5900262451172,"latitude2":43.89903646281729,"longitude2":-79.12997375488283}
#
#
#
# {"latitude1":42.78900762936104,"longitude1":-81.25239501953126,"latitude2":44.38046530469301,"longitude2":-77.57197509765626}
#
# {"latitude1":43.621817081568324,"longitude1":-81.50508056640626,"latitude2":45.191382966135095,"longitude2":-77.82466064453126}
