import logging
import psycopg2
from psycopg2 import ProgrammingError

def connect(**kwargs):
    """Connect to db. Makes log file LOG_DBNAME"""
    connector = None
    logging.basicConfig(filename="LOG_{}".format(kwargs.get('dbname', 'default')),
                        format="%(asctime)s %(message)s", level=logging.INFO)
    try:
        connector = psycopg2.connect(
            "dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
            .format(
                dbname = kwargs.get('dbname', 'default'),
                user = kwargs.get('user', 'postgres'),
                host = kwargs.get('host', 'localhost'),
                password = kwargs.get('password', 'postgres')
            ))
        logging.info("Connected with \"{}\"".format(kwargs.get('user', 'postgres')))
    except:
        logging.error("Can't connect with \"{}\"".format(kwargs.get('user', 'postgres')))

    def get_connector():
        return connector
    return get_connector

def is_connected(connector):
    """Test connection. If it exists returns True or False otherwise"""
    return connector != None

def close(connector):
    """Commit changes to server. and close connection Return True if succeed or False otherwise"""
    commit(connector)
    try:
        connector.close()
        logging.info("Connection closed\n\n")
        return True
    except Exception as e:
        logging.error("Something wrong during close: {}".format(e))
        return False

def commit(connector):
    """Commit changes to server"""
    try:
        connector.commit()
        logging.info("Committed changes")
        return True
    except:
        logging.error("Committed failed")
        return False

def rollback(connector):
    """Discard all changes. Return None"""
    try:
        connector.rollback()
        logging.info("Rollback succeed")
        return True
    except:
        logging.error("Rollback failed")
        return False

def do_query(connector, query):
    """Execute query with connector. Return list of values if query has response, otherwise return None"""
    cursor = connector.cursor()
    try:
        cursor.execute(query)
        logging.info("Execute query \"{}\"".format(query))
    except ProgrammingError as e:
        logging.error("Can't execute query \"{}\"\n\tbecause of: \"{}\"".format(query, e))
    finally:
        logging.info(connector.notices)

    return cursor.fetchall() if cursor.rowcount != 1 else None

def gen_select(table, *args):
    """Generate String for query of selecting columns *args in table"""
    values = list(args)
    for i in range(0, len(args) - 1):
        values.insert(2 * i + 1, ", ")
    return "SELECT {} FROM {}".format("".join(values), table)

def gen_select_all(table):
    """Generate String for query of selecting all rows from table"""
    return "SELECT * FROM {}".format(table)