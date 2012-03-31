# test connection to database

import psycopg2

db_name = 'department_db'

try:
    conn = psycopg2.connect("dbname='{}' user='postgres' host='localhost' password='postgres'".format(db_name))
except:
    print("Can't connect to db:", db_name)
    
cur = conn.cursor() # get cursor for work with
cur.execute("""SELECT * FROM test""") # select all rows from "test" table
rows = cur.fetchall()
print(('id', 'name', 'group'), '\n=======================')
for row in rows:
    print(row)
    print('------------------------')