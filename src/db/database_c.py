import logging

class database:    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            database.connection = None
            database.cursor = None
            database.dbname = None
            database.user = None
            database.host = None
            database.password = None
            logging.basicConfig(filename="LOG", format="%(asctime)s %(message)s", level=logging.INFO)
            cls.instance = super(database, cls).__new__(cls)
        return cls.instance