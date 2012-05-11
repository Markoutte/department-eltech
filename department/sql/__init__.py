import PySide.QtCore as Core
import psycopg2

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
        pass
    
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
        pass
    
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
            except psycopg2.IntegrityError:
                is_succeed = False
        elif query[0:6] == 'UPDATE':
            self.cursor.execute(query)
            is_succeed = True if self.cursor.statusmessage != 'UPDATE 0'else False
        self.emit(Core.SIGNAL('dataChanged(bool)'), is_succeed)
        return is_succeed