from private import *
import os



###############################################################################
########################            GLOBAL          ###########################
###############################################################################


## POSTGRES CONECTION DETAILS
PS_HOST_NAME = "toronto.cfeeqz1xpx0l.us-west-2.rds.amazonaws.com"
PS_DB_NAME = "postgres"
PS_PORT = 5432

## max sleep time (seconds)
SLEEP = 5

## coordinates
SOUTH = 41.279572967087944
WEST = -84.46112094932249
NORTH = 45.33449283652978
EAST = -73.99664341025999

OHMY_PAYLOAD = {
    "latitude1": SOUTH,
    "longitude1":WEST,
    "latitude2": NORTH
    "longitude2":EAST
    }

################################
##      DATABASE INFO         ##
################################


MONGO_FIELD_MAP = {
    'sale': [
        {'name': '_id', 'func': 'check_varchar', 'length': 50},
        {'name': 'Address1', 'func': 'check_varchar', 'length': 200},
        {'name': 'Address2', 'func': 'check_varchar', 'length': 200},
        {'name': 'Bedrooms', 'func': 'check_varchar', 'length': 5},
        {'name': 'Community', 'func': 'check_varchar', 'length': 100},
        {'name': 'PostalCode', 'func': 'check_varchar', 'length': 10},
        {'name': 'Bedrooms', 'func': 'check_varchar', 'length': 10},
        {'name': '_Sold', 'func': 'check_int'},
        {'name': '_List', 'func': 'check_int'},
        {'name': '_Sold_Date', 'func': 'check_date'},
        {'name': '_Contract_Date', 'func': 'check_date'},
        {'name': 'Undefined', 'func': 'get_property_type'}

    ],
    'list': [
        {'name': '_id', 'func': 'check_varchar', 'length': 50},
        {'name': 'Address1', 'func': 'check_varchar', 'length': 200},
        {'name': 'Address2', 'func': 'check_varchar', 'length': 200},
        {'name': 'Bedrooms', 'func': 'check_varchar', 'length': 5},
        {'name': 'Community', 'func': 'check_varchar', 'length': 100},
        {'name': 'PostalCode', 'func': 'check_varchar', 'length': 10},
        {'name': 'Bedrooms', 'func': 'check_varchar', 'length': 10},
        {'name': '_List', 'func': 'check_int'},
        {'name': '_Contract_Date', 'func': 'check_date'},
        {'name': 'Undefined', 'func': 'get_property_type'}
    ]
}


###############################################################################
########################           OH MY HOME          ########################
###############################################################################



################################
##       API URL INFO         ##
################################

HOUSE_SOLD_URL = "http://watch.ohmyhome.ca/HouseSold/HouseSold.php"
HOUSE_LIST_URL = "http://watch.ohmyhome.ca/HouseForSale/HouseForSale.php"

CONDO_SOLD_URL = "http://watch.ohmyhome.ca/CondoSold/CondoSold.php"
CONDO_LIST_URL = "http://watch.ohmyhome.ca/CondoForSale/CondoForSale.php"


###############################################################################
########################            MONGO HOUSE          ######################
###############################################################################

## property types
PROPERTY_TYPES = [
    'Condo Townhouse',
    'Detached',
    'Semi-Detached',
    'Att/Row/Twnhouse',
    'Condo Apt',
    '2-Storey',
    'Mobile/Trailer',
    'Vacant Land',
    'Comm Element Condo',
    'Cottage',
    'Multiplex',
    'Duplex',
    'Co-Op Apt',
    'Farm'
]

################################
##       API URL INFO         ##
################################

# number of days back to query for sold records
SOLD_DAYS_BACK = 600

# number of days back to query for listings
LIST_DAYS_BACK = 600


BASE_URL = "http://www.mongohouse.com/api/"
SOLD_API = "soldrecords?&sold_day_back={0}"
LIST_API = "newlistings?&list_day_back={0}"
PARAMS = "query=true&price_min=$0&price_max=$999,999,999&ownershiptype=all&south={0}&west={1}&north={2}&east={3}&_2dsphere=true"

## ids must be a list of semi-colon separated ids
SOLD_LISTINGS_API = "soldrecords?ids={0}"
NEW_LISTINGS_API = "newlistings?ids={0}&openhouse=undefined"

SOLD_URL = BASE_URL + SOLD_API.format(SOLD_DAYS_BACK) + PARAMS.format(SOUTH, WEST, NORTH, EAST)
LIST_URL = BASE_URL + LIST_API.format(LIST_DAYS_BACK) + PARAMS.format(SOUTH, WEST, NORTH, EAST)


LISTING_URL = BASE_URL + 'newlistings/{0}'
SOLD_RECORD_URL = BASE_URL + 'soldrecords/{0}'
