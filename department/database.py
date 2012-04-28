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
        logging.info("Connected to {} with \"{}\"".format(
            kwargs.get('dbname', 'default'),
            kwargs.get('user', 'postgres'))
        )
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
        logging.info("Committes succeed")
        return True
    except:
        logging.error("Committes failed")
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
    list = None
    try:
        cursor.execute(query)
        logging.info("Execute query \"{}\"".format(query))
        list = cursor.fetchall()
    except ProgrammingError as e:
        logging.error("Can't execute query \"{}\"\n\tbecause of: \"{}\"".format(query, e))
        return None
    finally:
        logging.info(connector.notices)

    return list


# Connection class

class Connection(object):
    __con = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Connection, cls).__new__(cls, *args, **kwargs)
        return  cls._instance

    def init(self, **kwargs):
        self.__con = (connect(**kwargs))
        if is_connected(self.__con()):
            return True
        else:
            self.__con = None
            return False

    def exec(self, query):
        return do_query(self.__con(), query)

    def close(self):
        close(self.__con())
