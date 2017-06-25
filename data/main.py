from src.MongoHouse import MongoHouse
from src.OhMyHome import OhMyHome
import logging as log
import time
import os

logname = time.strftime("%Y_%m_%d-%H_%M")
log.basicConfig(
    format='%(asctime)s  - %(module)s - %(levelname)s - %(message)s',
    level=log.INFO, # Change debug level to choose how verbose you want logging to be
    filename=os.path.join('logs', logname+".txt"))

## stream to console
# log.basicConfig(stream=sys.stdout, level=log.DEBUG)

# mongo = MongoHouse()
# mongo.scrapeRecordIds()
# mongo.scrapeRecords('sale')
# mongo.scrapeRecords('list')

ohmy = OhMyHome()
data = ohmy.main()
