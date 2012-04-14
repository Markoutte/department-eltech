import unittest
from db.database import DB 

class Test(unittest.TestCase):

    def setUp(self):
        self.__db = DB()
        self.assertTrue(self.__db.connect("test_db"), "Something wrong")
        self.assertTrue(self.__db.is_connected(), "Can't connect to db")


    def tearDown(self):
        self.__db.close()
        
    def testSingletone(self):
        self.assertTrue(self.__db is DB())
        
    def testNumOfEntries(self):
        list = self.__db.select_all("human")
        self.assertEqual(3, len(list), None)
        
    def testBrokenConnection(self):
        self.__db.execute('''INSERT INTO human DEFAULT VALUES''')
        values = self.__db.select_all("human")    
        self.assertEqual(4, len(values), None)
        self.__db.rollback()
        values = self.__db.select_all("human")    
        self.assertEqual(3, len(values), None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()