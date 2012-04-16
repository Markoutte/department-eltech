import unittest
from db.database2 import *

class Test(unittest.TestCase):

    def setUp(self):
        self.assertTrue(connect(setup(database(), dbname="test_db")), "Something wrong")
        
    def tearDown(self):
        close(database())
        
    def testSingletone(self):
        one = database()
        two = database()
        self.assertTrue(one is two)
        
    def testNumOfEntries(self):
        list = select_all(database(), "human")
        self.assertEqual(3, len(list), None)

    def testBrokenConnection(self):
        execute(database(), "INSERT INTO human DEFAULT VALUES")
        values = select_all(database(), "human")    
        self.assertEqual(4, len(values), None)
        rollback(database())
        values = select_all(database(), "human")    
        self.assertEqual(3, len(values), None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()