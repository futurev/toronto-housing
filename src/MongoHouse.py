import requests
import json
import config
import database_operations as dbo
from Login import Login
import DataCleaning
import random
import time
import math

class MongoHouse:
    """This is the class that handles all operations for using the
    MongoHouse APIs.
    """

    def __init__(self):
        self.login = Login()
        self.session = self.login.get_session()
        return


    def _getJason(self, url, use_session = False):
        """Internal function to hit the mongohouse API and return a json object
        For APIs requiring authorization, specify use_session=True
        """
        print ('Retrieving Jason for %s' % url)
        if use_session:
            r = session.get(url)
        else:
            r = requests.get(url)
        data = json.loads(r.text)
        return data

    def _storeData(self, data, table, query=None):
        """Interal function to store scraped data"""
        print ('Storing data')
        conn = dbo.getConnection()

        if query == None:
            num_cols = len(data[0])
            cols = ','.join(['%s ' for i in range(0, num_cols)])
            query = "INSERT INTO " + table + " VALUES (" + cols + ")"

        dbo.execute_query(conn, query, data, multiple=True)
        dbo.closeConnection(conn)
        return

    def _queryScrapedIds(self, table, record_type, scraped=None):
        """Internal function to retrieve the ids of all properties that have already been
        scraped"""
        print ('Querying %s for %s' % (table, record_type))
        conn = dbo.getConnection()
        if scraped:
            query = "SELECT id FROM {0} WHERE scraped = {1} AND type={2}"
            query = query.format(table, scraped, "'{0}'".format(record_type))

        else:
            query = "SELECT id FROM {0} WHERE type={1}"
            query = query.format(table, "'{0}'".format(record_type))
        data = dbo.query(conn, query)
        data = [d[0] for d in data]
        dbo.closeConnection(conn)
        return data

    def scrapeRecordIds(self):
        """External function to retrieve and store all for sale
        and sold property IDs
        """
        data = self._getJason(config.SOLD_URL)
        stored_records = self._queryScrapedIds('records', 'sale')
        records = [(d['_id'], 'sale', False) for d in data
                    if d['_id'] not in stored_records]
        if records:
            self._storeData(records, 'records')
        else:
            print ('No new records')
        stored_records = self._queryScrapedIds('records', 'list')
        data = self._getJason(config.LIST_URL)
        listings = [(d['_id'], 'list', False) for d in data
                    if d['_id'] not in stored_records]
        if listings:
            self._storeData(listings, 'records')
        else:
            print ('No new listings')
        return

    def _updateScraped(self, table, record_type):
        """Internal function to set scraped=True in the records tracking
        table
        """
        print ('Updating scraped ids from %s' % table)
        conn = dbo.getConnection()
        query = """
            UPDATE records
            SET scraped=True
            FROM %s AS updater
            WHERE updater.id=records.id
            AND records.type=%s
        """ % (table, "'{0}'".format(record_type))
        dbo.execute_query(conn, query)
        dbo.closeConnection(conn)
        return

    def _scrapeRecord(self, base_url, record_id, record_type):
        """Internal function to retrieve and clean the data for a
        specific property
        """
        url = base_url.format(record_id)
        data = self._getJason(url, use_session=(True if record_type == 'sale' else False))
        fields = []
        for field in config.MONGO_FIELD_MAP[record_type]:
            val = data.get(field['name'], None)
            if val:
                cleaned_val = getattr(DataCleaning, field['func'])(val=val,
                                length=field.get('length',0))
            else:
                cleaned_val = None
            fields.append(cleaned_val)
        coords = DataCleaning.get_coords(
                        val = data.get('_2dsphere', None))
        if coords:
            fields += coords
        else:
            fields += [None, None]
        return fields

    def scrapeRecords(self, record_type):
        """External function to ping the mongohouse API for each record in
        the records database_operations that has not been scraped
        """
        if record_type == 'list':
            base_url = config.LISTING_URL
            num_cols = 10
            table = 'list_records'
        else:
            base_url = config.SOLD_RECORD_URL
            num_cols = 12
            table = 'sale_records'

        records = self._queryScrapedIds('records', record_type, 'FALSE')
        parsed_records = []
        for record_id in records:
            fields = self._scrapeRecord(base_url, record_id, record_type)
            parsed_records.append(tuple(fields))
            time.sleep(random.randint(0, config.SLEEP))

        cols = ','.join(['%s ' for i in range(0, num_cols)])
        query = "INSERT INTO " + table + " VALUES (" + cols + \
            ", ST_GeomFromText('POINT(%s %s)', 4326))"

        self._storeData(parsed_records, table, query)
        self._updateScraped(table, record_type)
        return
