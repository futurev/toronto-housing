from fake_useragent import UserAgent
import config
from pprint import pprint
from Login import Login
import requests
import json
import random
import time
import DataCleaning
import database_operations as dbo
import logging as log

class OhMyHome:
    """This is the class that handles all operations for retreiving data
    from ohmyhome.ca
    """

    def __init__(self):
        self._getHeaders()
        self._getStoredRecords()
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

    def _getStoredRecords(self):
        """Internal function to retrieve the ids of all properties that have already been
        scraped"""
        log.info('Getting stored records')
        conn = dbo.getConnection()

        query = "SELECT id FROM sale_records"
        data = dbo.query(conn, query)
        self.stored_sales = [d[0] for d in data]

        query = "SELECT id FROM list_records"
        data = dbo.query(conn, query)
        self.stored_listings = [d[0] for d in data]

        dbo.closeConnection(conn)
        return

    def _getJason(self, url, r_payload, callback=False):
        """Internal Function to hit the ohmyhome API and return a json object
        """
        log.info('Retrieving Jason for %s' % url)

        session = requests.session()
        data = None
        try:
            resp = session.post(url, data=json.dumps(r_payload),
                                headers=self.headers)
            if resp.status_code == 200:
                data = resp.json()
                log.info('%s rows successfully retrieved' % str(len(data)))
            else:
                log.error('Unable to get data, status code %s' % resp.status_code)
        except Exception as e:
            log.error("Unable to connect to ohmyhome due to error %s" % e.message)
            if callback == False: ## this prevents the callback from being executed more than once
                time.sleep(10)
                data = self._getJason(url, r_payload, callback=True)

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

    def _storeData(self, data, query):
        """Interal function to store scraped data"""
        log.info('Storing data')
        conn = dbo.getConnection()
        dbo.execute_query(conn, query, data, multiple=True)
        dbo.closeConnection(conn)
        return

    def _scrapeRecord(self, data, record_type):
        """Internal function to clean the data for a specific property
        """
        fields = []
        for field in config.OHMY_FIELD_MAP[record_type]:
            val = data.get(field['name'], None)
            if val:
                cleaned_val = getattr(DataCleaning, field['func'])(val=val,
                                length=field.get('length',0))
            else:
                cleaned_val = None
            fields.append(cleaned_val)
        base_coords = [data.get('longitude', None), data.get('latitude', None)]
        coords = DataCleaning.get_coords(val=base_coords)
        if coords:
            fields += coords
        else:
            fields += [None, None]
        return fields

    def _parseData(self, data, record_type):
        """Internal function to clean and store the returned json data"""
        if record_type == 'list':
            base_url = config.LISTING_URL
            num_cols = 13
            table = 'list_records'
            stored_records = self.stored_listings
        else:
            base_url = config.SOLD_RECORD_URL
            num_cols = 15
            table = 'sale_records'
            stored_records = self.stored_sales

        parsed_records = []
        for record in data:
            if record['mlsno'] not in stored_records:
                fields = self._scrapeRecord(record, record_type)
                parsed_records.append(tuple(fields))

        if parsed_records:
            conn = dbo.getConnection()
            cols = ','.join(['%s ' for i in range(0, num_cols)])
            query = "INSERT INTO " + table + " VALUES (" + cols + \
                ", ST_GeomFromText('POINT(%s %s)', 4326))"
            self._storeData(parsed_records, query)
        else:
            log.info('All records have already been stored for this area')
        return

    def main(self):
        payloads = self._buildPayloads()
        for api in config.OH_MY_URLS:
            self._getHeaders()
            for x, payload in enumerate(payloads):
                log.info('getting payload #%s \n%s' % (str(x), payload))
                data = self._getJason(api['url'], payload)
                if data:
                    self._parseData(data, api['type'])
                else:
                    log.info('no data returned')
                time.sleep(random.randint(0, config.SLEEP))
        return

    def test(self):
        payload = config.TEST_PAYLOAD
        url = config.HOUSE_SOLD_URL
        data = self._getJason(url, payload)
        self._parseData(data, 'sale')
        return

## TODO
# 1) update listing status to sold once it appears in sold records
# 2) list_records_chng_hist table
