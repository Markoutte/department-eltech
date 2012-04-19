import unittest
from department.database import *

class Test(unittest.TestCase):

    def setUp(self):
        self.__db = setup(database(), dbname="test_db")
        self.assertTrue(connect(self.__db), "Something wrong")
        
    def tearDown(self):
        close(self.__db)

    def test_is_connected(self):
        self.assertTrue(is_connected(self.__db))
        self.assertFalse(not is_connected(self.__db))
        
    def test_num_of_entries(self):
        list = select_all(self.__db, "human")
        self.assertEqual(3, len(list), None)

    def test_broken_connection(self):
        execute(self.__db, "INSERT INTO human DEFAULT VALUES")
        values = select_all(self.__db, "human")
        self.assertEqual(4, len(values), None)
        rollback(self.__db)
        values = select_all(self.__db, "human")
        self.assertEqual(3, len(values), None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()