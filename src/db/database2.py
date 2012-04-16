import logging
import psycopg2
from db.database_c import database
            
def setup(database, **kwargs):
    if (is_connected(database)):
        close(database)
    database.dbname = kwargs.get('dbname', 'default')
    database.user = kwargs.get('user', 'postgres')
    database.host = kwargs.get('host', 'localhost')
    database.password = kwargs.get('password', 'postgres')
    connect(database)
    return database

def connect(database):
    try:
        database.connection = psycopg2.connect(
            "dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
            .format(
               dbname = database.dbname,
               user = database.user, 
               host = database.host, 
               password = database.password
            ))
        logging.info("\n\nConnected to \"{}\"".format(database.dbname))
        database.cursor = database.connection.cursor()
        return True
    except:
        logging.error("\n\nCan't connect to \"{}\"".format(database.dbname))
        return False
        
def close(database):
    database.connection.close()
    logging.info("Connection \"{}\" closed".format(database.dbname))
    
def commit(database):
    database.connection.commit()
    logging.info("Committed changes in \"{}\"".format(database.dbname))
    
def rollback(database):
    database.connection.rollback()
    logging.info("Rollback in \"{}\"".format(database.dbname))
    

def is_connected(database):
    return database.cursor is not None

def get_cursor(database):        
    if (not is_connected(database)):
        connect(database)
    return database.cursor

def do_query(database):    
    def do_execute(query):
        try:
            get_cursor(database).execute(query)
            logging.info("Execute query \"{0}\"".format(query))
            return get_cursor(database).fetchall() 
        except Exception as e:
            logging.error("Can't execute query \"{}\"\n\tbecause of: \"{}\""
                          .format(query, e))
            return None
    return do_execute

def execute(database, query):
    return do_query(database)(query)

def select(database, table, *args):
    values = list(args)
    for i in range(0, len(args)):
        values.insert(2 * i + 1, ", ")
    return do_query(database)("SELECT {} FROM {}".format("".join(values), table))

def select_all(database, table):
    return execute(database, "SELECT * FROM {}".format(table))

if __name__ == "__main__":   
    make_query = do_query(setup(database(), dbname = "test_db"))
    print(make_query("SELECT * FROM human"))
    close(database())
    