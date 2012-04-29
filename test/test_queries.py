import unittest
import department.database as database
import department.database.queries as query

class Test(unittest.TestCase):

    def setUp(self):
        self.assertTrue(database.open(dbname="department_db"))

    def tearDown(self):
        database.close()

    def test_persons_list(self):
        print(query.get_persons_list())

    def test_person_id(self):
        print(query.get_person_by_id(1))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
