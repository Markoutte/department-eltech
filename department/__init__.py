import department.sql as sql
import psycopg2

def main():
    conn = psycopg2.connect(dbname='department', user='postgres', password='postgres')
    with sql.Department(conn) as m:
        m.add_employee(None)
        
    return True

if __name__ == '__main__':
    main()