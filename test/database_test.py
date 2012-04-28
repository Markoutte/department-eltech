import unittest
from department.database import *
from department.utils import gen_select, gen_select_all
from functools import partial

class Test(unittest.TestCase):

    def setUp(self):
        self.get_connector = connect(dbname="test_db")
        self.do_query = partial(do_query, self.get_connector())

    def tearDown(self):
        close(self.get_connector())

    def test_is_connected(self):
        self.assertTrue(is_connected(self.get_connector()), "Something wrong")

    def test_rollback_and_commit(self):
        self.assertTrue(commit(self.get_connector()))
        self.assertTrue(rollback(self.get_connector()))
        
    def test_num_of_entries(self):
        list = self.do_query(gen_select_all("human"))
        self.assertEqual(3, len(list))

    def test_broken_connection(self):
        self.do_query("INSERT INTO human DEFAULT VALUES")
        values = self.do_query(gen_select_all("human"))
        self.assertEqual(4, len(values))
        rollback(self.get_connector())
        values = self.do_query(gen_select_all("human"))
        self.assertEqual(3, len(values))

    def test_gen(self):
        self.assertEqual(gen_select("human", "id"), "SELECT id FROM human")
        self.assertEqual(gen_select("human", "id", "name"), "SELECT id, name FROM human")
        self.assertEqual(gen_select("human", "id", "name", "phone"), "SELECT id, name, phone FROM human")
        self.assertEqual(gen_select_all("human"), "SELECT * FROM human")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()