from fake_useragent import UserAgent
import config
from pprint import pprint
from Login import Login
import requests
import json

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
            "Content-Length": 126,
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
        r = session.post(url, data=json.dumps(r_payload), headers=self.headers)
        data = r.json()
        return data

    def _buildPayload(self):
        pass
        return

    def get(self):
        r_payload = config.OHMY_PAYLOAD
        url = config.HOUSE_SOLD_URL
        data = self._getJason(url, r_payload)
        return data
