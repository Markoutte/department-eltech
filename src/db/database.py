'''Class maintains general connections and queries
'''

import psycopg2

class DataBase(object):

    def __init__(self, db_name, user, password, host="localhost"):
        try:
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name, user, host, password))
            self.__cur = conn.cursor()
        except:
            pass
    
    def selectAll(self, table_name):
        try:
            self.__cur.execute("SELECT * FROM %s" % table_name)
            return self.__cur.fetchall()
        except:
            return None