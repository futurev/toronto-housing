import os, sys
import config
import psycopg2


def getConnection():
    """
    Function to create a connection to postgres.
    ------
    param
        None
    return
        cnxn <Pyscopg Connection> : Connection to postgres data base
    """
    # log.info("Attempting to establish connection to postgres...")
    try:
        cnxn = psycopg2.connect(host=config.PS_HOST_NAME,
                                port=config.PS_PORT,
                                database=config.PS_DB_NAME,
                                user=config.PS_UID,
                                password=config.PS_PWD)
        return cnxn
    except Exception as e:
        print ('Error occured: %s' + e.message)
        # log.exception("Unable to connect to postgres due to error: " + e.message)
        return None

def query(conn, query, cols=False, cols_format='dict'):
    """
    Function to run select statements on postgres DB
    ------
    param
        conn <Pyscopg Connection> : Connection to postgres data base
        query <string> : Single sql query
        cols <boolean> : if True, include colnames with associated cols_format
                         if False, return list of tuples
        cols_format <string> : 'dict' to return list of dicts as resultset,
                                'list' to return colnames as first entry of resultset lists
    return
        resultset <list> : list of dicts/tuples
    """
    try:
        print('Running select query \n%s' % query)
        cur = conn.cursor()
        cur.execute(query)
        resultset = cur.fetchall()
        colnames = tuple([desc[0] for desc in cur.description])
        if cols and resultset:
            if cols_format == 'dict':
                resultset = [{colnames[col_index]:value
                                for col_index, value in enumerate(result)}
                                for result in resultset]
            elif cols_format == 'list':
                resultset = [colnames] + resultset
        cur.close()
        return resultset
    except Exception as e:
        print("Unable to run select query due to error: " + e.message)
        return
