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
            employee = sql.Employee()
            employee.fullname = 'John Doe'
            employee.gender = 'm'
            employee.birth = '2012.05.12'
            employee.education = 'высшее'
            employee.degree = 'специалист'
            employee.programme = 'информационные технологии'
            employee.family_status = 0
            employee.address_1 = '199178, СПб, ул. профессора Попова, д. 5'
            employee.phone = '+7 911 835 2559'
            employee.experience = '2011.05.11'
            employee.passport = '4009 214153'
            employee.issue = '2011.01.01'
            employee.authority = '30-е отделение милиции'
            employee.signed = '2012.05.12'
            employee.type = 'временный'
            employee_id = self.db.add_employee(employee)
            self.assertNotEqual(0, employee_id, 'Oh, no!')
            self.assertIsNotNone(self.db.get_employee_info(employee_id))
            
    def test_add_position(self):
        with self.db:
            position = sql.Position()
            position.position = 'Test name'
            position.category = 'Технический персонал'
            position.rate_amount = 7
            position.salary = 23456.234
            position_id = self.db.add_position(position)
            self.assertNotEqual(0, position_id, "Oh, no!")
            self.assertIsNotNone(self.db.get_position_info(position_id))

    def test_update(self):
        with self.db:
            # No employee
            self.assertFalse(self.db.update_employee(0))
            # Ok
            self.assertTrue(self.db.update_employee(3, fullname='John Doe', phone = 'null'))
            # Cannot be null exception
            self.assertFalse(self.db.update_employee(3, fullname='null'))
            self.conn.rollback()

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
            # Duplicate
            self.assertFalse(self.db.set_position(3, 1, 0.5))
            self.conn.rollback()
            
    def test_remove_position(self):
        with self.db:
            EMPLOYEE = 3
            POSITION = 2
            # Fail delete (no such entry)
            self.assertFalse(self.db.remove_position(EMPLOYEE, POSITION))
            # Succeed delete
            self.assertTrue(self.db.remove_position(EMPLOYEE, POSITION - 1))
            
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