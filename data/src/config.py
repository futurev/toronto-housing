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
SLEEP = 4

## coordinates
SOUTH = 42.7347443837978
WEST = -82.05335556083372
NORTH = 45.317234079179435
EAST = -77.49128280692747

DIVISIONS = 15

TEST_PAYLOAD = {
    "latitude1": 43.700799103429205,
    "longitude1": -79.5900262451172,
    "latitude2": 43.89903646281729,
    "longitude2": -79.12997375488283
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



OHMY_FIELD_MAP = {
    'sale': [
        {'name': 'mlsno', 'func': 'check_varchar', 'length': 20},
        {'name': 'city', 'func': 'check_varchar', 'length': 50},
        {'name': 'area', 'func': 'check_varchar', 'length': 50},

        {'name': 'solddate', 'func': 'check_date'},
        {'name': 'inputdate', 'func': 'check_date'},
        {'name': 'soldprice', 'func': 'check_int'},
        {'name': 'askprice', 'func': 'check_int'},

        {'name': 'stname', 'func': 'check_varchar', 'length': 50},
        {'name': 'stno', 'func': 'check_varchar', 'length': 50},
        {'name': 'sttype', 'func': 'check_varchar', 'length': 50},
        {'name': 'status', 'func': 'check_varchar', 'length': 20},

        {'name': 'style', 'func': 'check_varchar', 'length': 50},
        {'name': 'type', 'func': 'check_varchar', 'length': 50},

        {'name': 'wshrm', 'func': 'check_int'},
        {'name': 'bdrm', 'func': 'check_int'}
    ],
    'list': [
        {'name': 'mlsno', 'func': 'check_varchar', 'length': 20},
        {'name': 'city', 'func': 'check_varchar', 'length': 50},
        {'name': 'area', 'func': 'check_varchar', 'length': 50},

        {'name': 'inputdate', 'func': 'check_date'},
        {'name': 'askprice', 'func': 'check_int'},

        {'name': 'stname', 'func': 'check_varchar', 'length': 50},
        {'name': 'stno', 'func': 'check_varchar', 'length': 10},
        {'name': 'sttype', 'func': 'check_varchar', 'length': 20},
        {'name': 'status', 'func': 'check_varchar', 'length': 20},

        {'name': 'style', 'func': 'check_varchar', 'length': 50},
        {'name': 'type', 'func': 'check_varchar', 'length': 50},

        {'name': 'wshrm', 'func': 'check_int'},
        {'name': 'bdrm', 'func': 'check_int'}
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

OH_MY_URLS = [
    {'url': HOUSE_SOLD_URL, 'type': 'sale'},
    {'url': HOUSE_LIST_URL, 'type': 'list'}
    {'url': CONDO_SOLD_URL, 'type': 'sale'},
    {'url': CONDO_LIST_URL, 'type': 'list'}
    ]

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
