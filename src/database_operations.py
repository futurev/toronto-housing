import os, sys
import config
import psycopg2
import logging as log


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
        log.error("Unable to connect to postgres due to error: " + e.message)
        # log.exception("Unable to connect to postgres due to error: " + e.message)
        return None


def closeConnection(cnxn):
    """Function to close connection
    ------
    param
        cnxn <PYODBC/pyscog2 Connection> : Connection to teradata/postgres data base
    return
        True/False <bool> : Close status
    """
    # log.info("Attempting to close connection.... ")
    try:
        cnxn.close()
        return True

    except Exception as e:
        log.error("Closing postgres connection failed due to error: " + e.message)
        # log.exception("Closing teradata/postgres connection failed due to error: " + e.message)
        return False

def query(conn, query, data=False, columns=False):
    """Function to carry out retrieval of records
    ------
    param
        query <string> : String sql query
        conn <pyscopg Connection> : Connection to postgres data base
        data <tuple> : tuple of parameters that filter sql query. Defaults to False.
        columns <boolean> : If True, returns resultset as a list of dicts with keys as column names. Defaults to False.
    return
        resultset <PYODBC Result> : The result of fetched data from Teradata.
            Returns None on a failed attempt
    """
    cur = conn.cursor()
    if data:
        if not isinstance(data, tuple): # data should be a single tuple
            data = (data,)
        cur.execute(query, data)
        resultset = cur.fetchall()
    else:
        cur.execute(query)
        resultset = cur.fetchall()
    if columns:
        colnames = tuple([desc[0] for desc in cur.description])
        return [colnames] + resultset
    cur.close()
    return resultset


def execute_query(conn, query, data=False, multiple=False):
    """
    Function to run insert or update statements on postgres DB
    ------
    param
        conn <Pyscopg Connection> : Connection to postgres data base
        query <string> : Single sql query
        data <list> : List of tuples (if multiple=True) or single tuple (if multiple=False)
        multiple <boolean> : If True, expects data as list of tuples, if False expects data as single tuple
    """
    try:
        cur = conn.cursor()
        if data:
            if multiple:  # data is a list of tuples
                cur.executemany(query, data)
            else:  # data is a single tuple
                cur.execute(query, data)
        else:
            cur.execute(query)
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        log.error("Unable to execute query due to error: " + e.message)
        return False
