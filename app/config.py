from private import *
import os


## POSTGRES CONECTION DETAILS
PS_HOST_NAME = "toronto.cfeeqz1xpx0l.us-west-2.rds.amazonaws.com"
PS_DB_NAME = "postgres"
PS_PORT = 5432


currDir = os.getcwd()

QUERIES_PATH = os.path.join(currDir, 'app', 'data', 'queries')
LOG_PATH = os.path.join(currDir, 'logs')
