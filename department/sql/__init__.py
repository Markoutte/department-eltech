import PySide.QtCore as Core
import psycopg2
import logging

## Модель предметной области
class Department(Core.QObject):
    
    def __init__(self, connection):
        Core.QObject.__init__(self)
        self.cursor = connection.cursor()
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.cursor.close()
    
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
                          address = take_str(employee.address_1))
                  )
        if not self.__try_execute(query):
            return 0
        query = ("INSERT INTO employee(contract, fullname, gender, birth, "
                 "education, degree, programme, family_status, address, "
                 "phone, experience, passport) ")
        query += ("VALUES ({contract}, {fullname}, {gender}, {birth}, "
                 "{education}, {degree}, {programme}, {family_status}, {address}, "
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
                         passport = take_str(employee.passport)
                         )
                  )
        if not self.__try_execute(query):
            return 0
        query = "SELECT currval('employee_personnel_number_seq');"
        self.cursor.execute(query)
        contract_id = self.cursor.fetchone()[0]
        return contract_id if contract_id is not None else 0
            
    
    ## Добавить должность
    def add_position(self, position):
        pass
    
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
        pass
    
    ## Обновить данные должности
    def update_position(self, position_id, **params):
        pass
    
    ## Список сотрудников
    #
    # Возвращает в каждой строке 2 поля: табельный номер и полное имя 
    def get_employees_list(self, substring=None):
        query = "SELECT personnel_number, fullname "
        query += "FROM employee "
        if substring is not None:
            query += "WHERE fullname LIKE '{}%' ".format(substring)
        query += "ORDER BY fullname;"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    ## Список должностей
    #
    # Возвращает в каждой строке 3 поля: код, название и разряд,
    # если указано для кого, то вдобавок показывается поле со ставкой
    def get_positions_list(self, employee_id=None):
        if employee_id is None:
            query = "SELECT code, position, rank "
            query += "FROM personnel_schedule "
            query += "ORDER BY position, rank;"
        else:
            query = "SELECT code, p.position, rank, e.rate "
            query += "FROM personnel_schedule p, employee_has_position e "
            query += "WHERE p.code = e.position "
            query += "AND e.employee = {} ".format(employee_id)
            query += "ORDER BY p.position, rank;"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    ## Подбробная информация о сотруднике
    #
    # Порядок полей:
    #    personnel_number INTEGER, -- табельный номер
    #    contract_id INTEGER, -- номер контракта
    #    signed VARCHAR, -- дата заключения
    #    "type" VARCHAR, -- тип контракта (временный/постоянный) 
    #    fullname VARCHAR,
    #    gender CHAR, -- 'f'/'m'
    #    birth VARCHAR, -- день рождения
    #    education VARCHAR, -- образование (срденее неполное, среднее полное, среднее специальное, неоконченное высшее, высшее)
    #    degree VARCHAR , -- академическая степень (бакалавр, специалист, магистр, к.н., д.н.)
    #    programme VARCHAR, -- профиль подготовки, напр. компьютерная безопасность, информационные системы, пр.
    #    family_status SMALLINT, -- {0:холост/незамужем, 1:женат/замужем, 2:разведён/разведена, 3:вдовец/вдова}
    #    current_address TEXT, -- адрес проживания
    #    phone BIGINT, -- телефон
    #    experience VARCHAR, -- начало стажа работы
    #    passport_id VARCHAR, -- номер паспорта
    #    issue VARCHAR, -- дата выдачи
    #    authority TEXT, -- кем выдан
    #    passport_address TEXT -- адрес регистрации
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
    #    salary NUMERIC(13, 4), -- ну кто может получить запрлату больше 9 миллионов?
    #    rate_amount REAL, -- число доступных ставок
    #    rate_booked REAL, -- число занятынх ставок
    #    employees SMALLINT -- число занятых сотрудников
    def get_position_info(self, position_id):
        query = "SELECT code, position, rank, category, CAST(salary AS REAL), rate_amount, rate_booked, employees " 
        query += "FROM personnel_schedule "
        query += "WHERE code = {};".format(position_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    ## Обёртка для выполнения запросов
    def __try_execute(self, query):
        if query[0:6] == 'INSERT':
            is_succeed = True
            try:
                self.cursor.execute(query)
            except psycopg2.IntegrityError as integrity_error:
                log = logging.getLogger()
                log.error(integrity_error.pgerror)
                is_succeed = False
        elif query[0:6] == 'UPDATE':
            self.cursor.execute(query)
            is_succeed = True if self.cursor.statusmessage != 'UPDATE 0' else False
        elif query[0:6] == 'DELETE':
            self.cursor.execute(query)
            is_succeed = True if self.cursor.statusmessage != 'DELETE 0' else False
        self.emit(Core.SIGNAL('dataChanged(bool)'), is_succeed)
        return is_succeed
    
class Employee(object):
    ## Полное имя VARCHAR
    fullname = None
    ## Пол CHAR ('m'/'f')
    gender=None
    ## Дата рождения DATE
    #
    # В формате строки ('ГГГГ.ММ.ДД')
    __birth=None
    @property
    def birth(self):
        return self.__birth.toString('yyyy.M.d')
    @birth.setter
    def birth(self, date):
        self.__birth = Core.QDate.fromString(date, 'yyyy.M.d')
    ## Образование (напр. высшее) VARCHAR
    education=None
    ## Академическая степень (напр. бакалавр) VARCHAR
    degree=None
    ## Направление подготовки (напр. КБ) VARCHAR
    programme=None
    ## Семейный статус (0, 1, 2, 3) INTEGER
    family_status=None
    ## Адрес, указанный в пасроте TEXT
    address_1=None
    ## Адрес проживания TEXT
    address_2=None
    ## Телефон INTEGER
    #
    # Аргменты могут быть int или str
    __phone=None
    @property
    def phone(self):
        return self.__phone
    @phone.setter
    def phone(self, number):
        if type(number) == type(int()):
            self.__phone = number
        elif type(number) == type(str()):
            self.__phone = int(number.replace(' ', ''))
        else:
            self.__phone = None
    ## Дата начала опыта работы DATE
    #
    # В формате строки ('ГГГГ.ММ.ДД')
    __experience=None
    @property
    def experience(self):
        return self.__experience.toString('yyyy.M.d')
    @experience.setter
    def experience(self, date):
        self.__experience = Core.QDate.fromString(date, 'yyyy.M.d')
    ## Номер паспрорта VARCHAR
    passport=None
    ## Дата выдачи паспорта DATE
    __issue=None
    @property
    def issue(self):
        return self.__issue.toString('yyyy.M.d')
    @issue.setter
    def issue(self, date):
        self.__issue = Core.QDate.fromString(date, 'yyyy.M.d')
    ## Кем выдан TEXT
    authority=None
    ## Даата подписания контракта DATE
    __signed=None
    @property
    def signed(self):
        return self.__signed.toString('yyyy.M.d')
    @signed.setter
    def signed(self, date):
        self.__signed = Core.QDate.fromString(date, 'yyyy.M.d')
    ## Тип контракта (времменый, постоянный) VARCHAR
    type=None