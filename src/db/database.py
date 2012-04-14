''' Module for working with database'''
import logging
import psycopg2

class DB(object):
    '''Is a wrapper for psycopg2. 
    It offers two evident query for selecting columns'''
    
    __conn = None
    __cur = None
    __log = logging
    __log.basicConfig(filename="LOG", format="%(asctime)s %(message)s", level=logging.INFO)
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DB, cls).__new__(cls)
        return cls.instance

    def connect(self, db_name, user="postgres", password="postgres", host="localhost"):
        if (db_name == "" or 
            user == "" or 
            password == "" or 
            host == ""):
            self.__log.warn("Empty login data ({}, {}, {}, {})".format(db_name,
                                                                       user,
                                                                       password,
                                                                       host))
            return False
        self.db_name = db_name
        try:
            self.__conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name, user, host, password))
            self.__cur = self.__conn.cursor()
            self.__log.info("Connected to \"%s\"" % db_name)
            return True
        except:
            self.__cur = None
            self.__log.error("Can't connect to \"%s\"" % db_name)
            return False
    
    def close(self):
        if (self.__conn == None):
            return
        
        self.__conn.close()
        self.__cur = None
        self.__log.info("Connection \"%s\" closed" % self.db_name)
        
    def is_allowed(self):
        ''' Checks is db which was connected true or false source db'''
        return True
            
    def is_connected(self):
        return self.__cur != None
    
    def get_columns_name(self, table):
        query = "select column_name from information_schema.columns where table_name='{0}';"
        return self.execute(query.format(table))
    
    def select(self, table, *args):
        '''Selects particular columns from table_name'''
        values = list(args)
        get_odd = lambda x : 2 * x + 1 
        for i in range(0, len(args)- 1):
            values.insert(get_odd(i), ", ")
        query = "SELECT %s FROM %s;" % ("".join(values), table)
        return self.execute(query)
    
    def select_all(self, table):
        ''' Selects all data from table with table_name'''
        return self.execute("SELECT * FROM %s;" % table)
        
    def execute(self, query):
        try:
            self.__cur.execute(query)
            self.__log.info("Execute query \"{0}\"".format(query))
            return self.__cur.fetchall()
        except Exception as e:
            self.__log.error(e)
            return None
      
    def commit(self):
        self.__conn.commit()
        
    def rollback(self):
        self.__conn.rollback()