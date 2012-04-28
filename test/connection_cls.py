import unittest
from department.database import Connection
from department.utils import to_str_list

class Test(unittest.TestCase):

    def setUp(self):
        self.con = Connection()
        self.assertTrue(self.con.init(dbname="test_db"))

    def tearDown(self):
        self.con.close()

    def test_query(self):
        list = self.con.exec("SELECT * FROM human")
        self.assertEqual(3, len(list))

    def test_singletone(self):
        self.assertEqual(self.con, Connection(), "Connections do not use singletone")

    def test_to_str_list(self):
        x = [('a', 2), ('b', ) , (3, '2'), ()]
        self.assertEqual(to_str_list(x), ['2', '2'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()