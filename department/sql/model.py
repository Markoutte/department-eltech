from PySide.QtCore import (Qt, QAbstractListModel, QModelIndex, QDate)

class EmployeeListModel(QAbstractListModel):
    
    employees=None
    
    def __init__(self, parent=None):
        super(EmployeeListModel, self).__init__(parent)
                
    def setEmployeeList(self, employees=None):
        if employees is None:
            self.employees = [()]
        else:
            self.employees = employees
        
    def rowCount(self, index=QModelIndex()):
        return len(self.employees)
    
    def data(self, index, role=Qt.DisplayRole):
        if index is None:
            return None        
        if 0 > index.row() >= len(self.employees):
            return None        
        if role == Qt.DisplayRole:
            return self.employees[index.row()][1]
        else:
            return None
        
    def personnel_number(self, index):
        if index is None:
            return None
        if (0 > index.row() >= len(self.employees)):
            return None        
        return self.employees[index.row()][0]
    
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
        self.__birth = QDate.fromString(date, 'yyyy.M.d')
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
        self.__experience = QDate.fromString(date, 'yyyy.M.d')
    ## Номер паспрорта VARCHAR
    passport=None
    ## Дата выдачи паспорта DATE
    __issue=None
    @property
    def issue(self):
        return self.__issue.toString('yyyy.M.d')
    @issue.setter
    def issue(self, date):
        self.__issue = QDate.fromString(date, 'yyyy.M.d')
    ## Кем выдан TEXT
    authority=None
    ## Даата подписания контракта DATE
    __signed=None
    @property
    def signed(self):
        return self.__signed.toString('yyyy.M.d')
    @signed.setter
    def signed(self, date):
        self.__signed = QDate.fromString(date, 'yyyy.M.d')
    ## Тип контракта (времменый, постоянный) VARCHAR
    type=None

class Position():
    # Название
    position=None
    # Разярд
    rank=None
    # Группа
    category=None
    # Зарплата
    salary=None
    # Всего ставок
    rate_amount=None