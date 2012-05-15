import PySide.QtCore as Core
import psycopg2
import logging
from department.sql import model

## Модель предметной области
class Department(Core.QObject):
    
    def __init__(self, connection):
        Core.QObject.__init__(self)
        self.cursor = connection.cursor()
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        if self.cursor is not None:
            self.cursor.close()
            del self.cursor
            
    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            del self.cursor
    
    ## Добавить сотрудника 
    def add_employee(self, employee):
        take_str = lambda x : "'{}'".format(x) if x is not None else 'NULL'
        take = lambda x : x if x is not None else 'NULL'
        query = "INSERT INTO contract(signed, \"type\") "
        query += ("VALUES ({}, {});"
                  .format(take_str(employee.signed), 
                          take_str(employee.type)))
        if not self.__try_execute(query):
            return 0
        query = "SELECT currval('contract_id_seq');"
        self.cursor.execute(query)
        contract_id = self.cursor.fetchone()[0]
        query = "INSERT INTO passport(id, issue, authority, address) "
        query += ("VALUES ({id}, {issue}, {authority}, {address});"
                  .format(id = take_str(employee.passport),
                          issue = take_str(employee.issue),
                          authority = take_str(employee.authority),
                          address = take_str(employee.address_1)))
        if not self.__try_execute(query):
            return 0
        query = ("INSERT INTO employee(contract, fullname, gender, birth, "
                 "education, degree, programme, family_status, address, "
                 "phone, experience, passport) ")
        query += ("VALUES ({contract}, INITCAP({fullname}), {gender}, {birth}, "
                 "lower({education}), lower({degree}), lower({programme}), {family_status}, {address}, "
                 "{phone}, {experience}, {passport});"
                 .format(contract = take(contract_id),
                         fullname = take_str(employee.fullname),
                         gender = take_str(employee.gender),
                         birth = take_str(employee.birth),
                         education = take_str(employee.education),
                         degree = take_str(employee.degree),
                         programme = take_str(employee.programme),
                         family_status = take(employee.family_status),
                         address = take_str(employee.address_2),
                         phone = take(employee.phone),
                         experience = take_str(employee.experience),
                         passport = take_str(employee.passport)))
        if not self.__try_execute(query):
            return 0
        query = "SELECT currval('employee_personnel_number_seq');"
        self.cursor.execute(query)
        contract_id = self.cursor.fetchone()[0]
        return contract_id if contract_id is not None else 0
    
    ## Удалить сотрудника
    def delete_employee(self, employee_id):
        query = "DELETE FROM employee WHERE personnel_number = {}".format(employee_id)
        return self.__try_execute(query)
    
    ## Добавить должность
    def add_position(self, position):
        take_str = lambda x : "'{}'".format(x) if x is not None else 'NULL'
        take = lambda x : x if x is not None else 'NULL'
        query = ("INSERT INTO personnel_schedule(position, rank, category, "
                 "salary, rate_amount) ")
        query += ("VALUES (lower({position_name}), lower({rank}), lower({category}), "
                  "{salary}, {rate_amount});"
                  .format(position_name = take_str(position.position),
                          rank = take_str(position.rank), 
                          category = take_str(position.category),
                          salary = take(position.salary),
                          rate_amount = take(position.rate_amount)))
        if not self.__try_execute(query):
            return 0
        query = "SELECT currval('personnel_schedule_code_seq');"
        self.cursor.execute(query)
        position_code = self.cursor.fetchone()[0]
        return position_code if position_code is not None else 0
    
    ## Удалить должность
    def delete_position(self, position_id):
        query = "DELETE FROM personnel_schedule WHERE code = {}".format(position_id)
        return self.__try_execute(query)
    
    ## Назначить на должность
    def set_position(self, employee_id, position_id, rate):
        query = "INSERT INTO employee_has_position "
        query += "VALUES ({}, {}, {});".format(employee_id, position_id, rate)
        return self.__try_execute(query)
    
    ## Снять с должности
    def remove_position(self, employee_id, position_id):
        query = "DELETE FROM employee_has_position "
        query += "WHERE employee = {} ".format(employee_id)
        query += "AND position = {};".format(position_id)
        return self.__try_execute(query)
    
    ## Изенить ставку
    #
    # По завершении генерирует сигнал с переданными параметрами
    # и успешности завершения операции
    def set_rate(self, employee_id, position_id, rate):
        query = "UPDATE employee_has_position "
        query += "SET rate = {} ".format(rate)
        query += "WHERE employee = {} ".format(employee_id)
        query += "AND position = {};".format(position_id)
        return self.__try_execute(query)
    
    ## Обновить данные сотрудника
    def update_employee(self, employee_id, **params):
        if len(params) == 0: 
            return False
        query = self.__get_update_string('employee', 'personnel_number', employee_id, **params)
        return self.__try_execute(query)
    
    ## Обновить данные контракта
    def update_contract(self, contract_id, **params):
        if len(params) == 0: 
            return False
        query = self.__get_update_string('contract', 'id', contract_id, **params)
        return self.__try_execute(query)
    
    ## Обновить данные паспорта
    def update_passport(self, passport_id, **params):
        if len(params) == 0: 
            return False
        query = self.__get_update_string('passport', 'id', passport_id, **params)
        return self.__try_execute(query)
    
    ## Обновить данные должности
    def update_position(self, position_id, **params):
        if len(params) == 0: 
            return False
        query = self.__get_update_string('personnel_schedule', 'code', position_id, **params)
        return self.__try_execute(query)
    
    ## Список сотрудников
    #
    # Возвращает в каждой строке 2 поля: табельный номер и полное имя 
    def get_employees_list(self, substring=None):
        query = "SELECT personnel_number, fullname "
        query += "FROM employee "
        if substring is not None:
            query += "WHERE fullname LIKE INITCAP('{}%') ".format(substring)
        query += "ORDER BY fullname;"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    ## Список должностей
    def get_positions_list(self, employee_id=None):
        if employee_id is None:
            query = ("SELECT code, position, rank, category, NULL, "
                     "CAST(salary AS REAL), rate_amount, rate_booked, employees ")
            query += "FROM personnel_schedule "
            query += "ORDER BY position, rank;"
        else:
            query = ("SELECT code, p.position, rank, category, e.rate, "
                     "e.rate*CAST(salary AS REAL), rate_amount, rate_booked, employees ")
            query += "FROM personnel_schedule p, employee_has_position e "
            query += "WHERE p.code = e.position "
            query += "AND e.employee = {} ".format(employee_id)
            query += "ORDER BY p.position, rank;"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    ## Подбробная информация о сотруднике
    #
    # Порядок полей:
    #    0. personnel_number INTEGER, -- табельный номер
    #    1. contract_id INTEGER, -- номер контракта
    #    2. signed VARCHAR, -- дата заключения
    #    3. "type" VARCHAR, -- тип контракта (временный/постоянный) 
    #    4. fullname VARCHAR,
    #    5. gender CHAR, -- 'f'/'m'
    #    6. birth VARCHAR, -- день рождения
    #    7. education VARCHAR, -- образование (срденее неполное, среднее полное, среднее специальное, неоконченное высшее, высшее)
    #    8. degree VARCHAR , -- академическая степень (бакалавр, специалист, магистр, к.н., д.н.)
    #    9. programme VARCHAR, -- профиль подготовки, напр. компьютерная безопасность, информационные системы, пр.
    #    10. family_status SMALLINT, -- {0:холост/незамужем, 1:женат/замужем, 2:разведён/разведена, 3:вдовец/вдова}
    #    11. current_address TEXT, -- адрес проживания
    #    12. phone BIGINT, -- телефон
    #    13. experience VARCHAR, -- начало стажа работы
    #    14. passport_id VARCHAR, -- номер паспорта
    #    15. issue VARCHAR, -- дата выдачи
    #    16. authority TEXT, -- кем выдан
    #    17. passport_address TEXT -- адрес регистрации
    def get_employee_info(self, employee_id):
        query =  "SELECT * FROM get_employee({});".format(employee_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()
            
    
    ## Подробная информация о должности
    #
    # Порядок полей:
    #    code INTEGER, -- код должности
    #    position VARCHAR, -- должность (инженер, доцент, зав. кафедрой и пр.)
    #    rank VARCHAR, -- разярд, напр.: 1-й, 2-й, 3-й или младший, старший
    #    category VARCHAR, -- категория, напр. (профессорско-преподавательский состав, технический персонал, административный состав, хозяйственный состав и т.д.
    #    NULL — это место зарезервировано для учёта ставки
    #    salary NUMERIC(13, 4), -- ну кто может получить запрлату больше 9 миллионов?
    #    rate_amount REAL, -- число доступных ставок
    #    rate_booked REAL, -- число занятынх ставок
    #    employees SMALLINT -- число занятых сотрудников
    def get_position_info(self, position_id):
        query = "SELECT code, position, rank, category, NULL, CAST(salary AS REAL), rate_amount, rate_booked, employees " 
        query += "FROM personnel_schedule "
        query += "WHERE code = {};".format(position_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    ## Обёртка для выполнения запросов
    def __try_execute(self, query):
        log = logging.getLogger()
        if query[0:6] == 'INSERT':
            is_succeed = True
            try:
                self.cursor.execute(query)
            except psycopg2.IntegrityError as integrity_error:
                log.error(integrity_error.pgerror)
                self.error = integrity_error.pgerror
                is_succeed = False
        elif query[0:6] == 'UPDATE':
            try: 
                self.cursor.execute(query)
                is_succeed = True if self.cursor.statusmessage != 'UPDATE 0' else False
            except psycopg2.IntegrityError as integrity_error:
                log.error(integrity_error.pgerror)
                self.error = integrity_error.pgerror
                is_succeed = False
            except psycopg2.InternalError as internal_error:
                log.error(internal_error.pgerror)
                self.error = internal_error.pgerror
                is_succeed = False 
        elif query[0:6] == 'DELETE':
            self.cursor.execute(query)
            is_succeed = True if self.cursor.statusmessage != 'DELETE 0' else False
        self.emit(Core.SIGNAL('updateDatabase(bool)'), is_succeed)
        if is_succeed:
            self.emit(Core.SIGNAL('dataChanged()'))
        log.warn(query)
        return is_succeed
    
    ## Сконструировать строку обновления данных
    #
    # Возвращает строку вида:
    # UPDATE table SET key1 = value1, key2 = value2 WHERE {id_name} = {id_value};
    # {id_name} и {id_value} — именя для функции str.format(**kwargs)
    def __get_update_string(self, table, id_name, id_value, **params):
        is_str = lambda x : type(x) == type(str()) and x.upper() != 'NULL'
        string = "UPDATE {} SET ".format(table)
        set_params = []
        for key in params:
            if params[key] is None:
                params[key] = 'NULL'
            set_params.append(("{k} = '{v}'" if is_str(params[key]) else "{k} = {v}")
                              .format(k = key, v = params[key]))        
        string += ", ".join(set_params)
        string += ((" WHERE {} = '{}';" if is_str(id_value) else " WHERE {} = {};")
                   .format(id_name, id_value))
        return string
    
    def get_error(self):
        return self.error
    
def Employee():
    return model.Employee()

def Position():
    return model.Position()

def EmployeeListModel(parent=None):
    return model.EmployeeListModel(parent)

def PositionTableModel(parent=None):
    return model.PositionTableModel(parent)