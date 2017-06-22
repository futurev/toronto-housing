from fake_useragent import UserAgent
import config
from pprint import pprint
from Login import Login
import requests
import json
import random
import time

class OhMyHome:
    """This is the class that handles all operations for retreiving data
    from ohmyhome.ca
    """

    def __init__(self):
        self._getHeaders()
        return

    def _getHeaders(self):
        """Internal function to produce the web request headers
        """
        ua = UserAgent()

        self.headers = {
            "Host": "watch.ohmyhome.ca",
            "Proxy-Connection": "keep-alive",
            "Content-Length": '133',
            "Accept": "application/json, text/plain, */*",
            "Origin": "http://watch.ohmyhome.ca",
            "User-Agent": ua['random'],
            "Content-Type": "application/json;charset=UTF-8",
            "Referer": "http://watch.ohmyhome.ca/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.8,fr;q=0.6"
        }
        return

    def _getJason(self, url, r_payload):
        """Internal Function to hit the ohmyhome API and return a json object
        """
        print ('Retrieving Jason for %s' % url)

        session = requests.session()
        resp = session.post(url, data=json.dumps(r_payload),
                            headers=self.headers)
        if resp.status_code == 200:
            print ('Data successfully retrieved')
            data = resp.json()
        else:
            print ('Unable to get data, status code %s' % resp.status_code)
            data = None
        return data

    def _getCoords(self):
        south = config.SOUTH
        west = config.WEST
        lat_div = (config.NORTH - config.SOUTH)/config.DIVISIONS
        long_div = (abs(config.WEST) - abs(config.EAST))/config.DIVISIONS
        lat_coords = [south]
        long_coords = [west]

        for x in range(0, config.DIVISIONS):
            south += lat_div
            west += long_div
            lat_coords.append(south)
            long_coords.append(west)
        return lat_coords, long_coords

    def _buildPayloads(self):
        lat_coords, long_coords = self._getCoords()
        payloads = []
        for x in range(1, config.DIVISIONS+1):
            for y in range(1, config.DIVISIONS+1):
                payloads.append({
                    "latitude1": lat_coords[y-1],
                    "longitude1": long_coords[x-1],
                    "latitude2": lat_coords[y],
                    "longitude2": long_coords[x]
                    })

        return payloads

    def main(self):
        payloads = self._buildPayloads()
        for x, payload in enumerate(payloads):
            data = self._getJason(config.HOUSE_SOLD_URL, payload)
            time.sleep(random.randint(0, config.SLEEP))
        return

    def get(self):
        r_payload = config.OHMY_PAYLOAD
        # print r_payload
        url = config.HOUSE_SOLD_URL
        data = self._getJason(url, r_payload)
        return data
