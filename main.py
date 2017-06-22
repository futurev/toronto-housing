from src.MongoHouse import MongoHouse
from src.OhMyHome import OhMyHome


# mongo = MongoHouse()
# mongo.scrapeRecordIds()
# mongo.scrapeRecords('sale')
# mongo.scrapeRecords('list')

ohmy = OhMyHome()
data = ohmy.get()
