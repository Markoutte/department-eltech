import unittest
import department.database as database
import department.database.queries as query

class Test(unittest.TestCase):

    def setUp(self):
        self.assertTrue(database.open(dbname="department_db"))

    def tearDown(self):
        database.close()

    def test_persons_list(self):
        response = query.get_persons_list('п')
        print(response)
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)
        # checks that string like this: 'Family N.M.'
        self.assertRegexpMatches(response[0], r'\w+\s(\w\.){2}')

    def test_person_id(self):
        print(query.get_person_by_id(1))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
