import unittest
import department.sql as sql
import psycopg2

class Test(unittest.TestCase):

    def setUp(self):
        
        self.conn = psycopg2.connect(dbname = 'department', 
                                user = 'postgres', 
                                password = 'postgres')
        self.db = sql.Department(self.conn)

    def tearDown(self):
        self.conn.rollback()
        self.conn.close()

    def test_add_employee(self):
        with self.db:
            pass

    def test_set_position(self):
        with self.db:
            # No employee
            self.assertFalse(self.db.set_position(1, 1, 0.5))
            self.conn.rollback()
            # No position
            self.assertFalse(self.db.set_position(3, 100, 0.5))
            self.conn.rollback()
            # No employee and no position
            self.assertFalse(self.db.set_position(1, 0, 0.5))
            self.conn.rollback()
            # All good
            self.assertTrue(self.db.set_position(3, 11, 0.5))
            print(self.db.get_positions_list(3))
            # Duplicate
            self.assertFalse(self.db.set_position(3, 1, 0.5))
            self.conn.rollback()

    def test_set_rate(self):
        with self.db:
            self.assertTrue(self.db.set_rate(3, 1, 1.0), 'Something wrong!')
            self.assertFalse(self.db.set_rate(1, 1, 1.0), 'Something wrong!')

    def test_get_employees_list(self):
        with self.db:
            self.assertIsNotNone(self.db.get_employees_list('Пел'), 'Not employees found')

    def test_get_positions_list(self):
        with self.db:
            self.assertIsNotNone(self.db.get_positions_list(), 'Not positions exists')
            self.assertIsNotNone(self.db.get_positions_list(3), 'Not positions for employee')
    
    def test_get_employee_info(self):
        with self.db:
            self.assertIsNotNone(self.db.get_employee_info(3), 'No employee with this id')
            
    def test_get_position_info(self):
        with self.db:
            self.assertIsNotNone(self.db.get_position_info(11), 'No such positions')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()