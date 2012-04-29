import unittest
import department.database as database

class Test(unittest.TestCase):

    def setUp(self):
        self.assertTrue(database.open(dbname="test_db"))

    def tearDown(self):
        database.close()

    def test_is_opened(self):
        self.assertTrue(database.is_connected())

    def test_singletone(self):
        from department.database import Connection
        self.assertTrue(Connection(), Connection())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()