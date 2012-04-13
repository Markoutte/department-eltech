import unittest
import psycopg2

class Test(unittest.TestCase):


    def setUp(self):
        try:
            self.conn = psycopg2.connect("dbname='test_db' user='postgres' host='localhost' password='postgres'")
            self.cur = self.conn.cursor()
            pass
        except:
            self.fail("Can't connect to db")


    def tearDown(self):
        self.conn.close()
        
    def testNumOfEntries(self):
        self.cur.execute('''SELECT * FROM human''')
        self.assertEqual(3, self.cur.rowcount, None)
        
    def testBrokenConnection(self):
        self.cur.execute('''INSERT INTO human DEFAULT VALUES''')
        self.cur.execute('''SELECT * FROM human''')       
        self.assertEqual(4, self.cur.rowcount, None)
        self.conn.rollback()
        self.cur.execute('''SELECT * FROM human''')
        self.assertEqual(3, self.cur.rowcount, None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()