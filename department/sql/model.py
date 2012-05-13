from PySide.QtCore import (Qt, QAbstractListModel, QAbstractTableModel, QModelIndex, QDate)

class EmployeeListModel(QAbstractListModel):
    
    employees=[]
    
    def __init__(self, parent=None):
        super(EmployeeListModel, self).__init__(parent)
                
    def setEmployeeList(self, employees):
        self.employees = employees
        self.reset()
        
    def employeesList(self):
        return self.employees
        
    def rowCount(self, index=QModelIndex()):
        return len(self.employees)
    
    def data(self, index, role=Qt.DisplayRole):
        if index.row() < 0 or index.row() >= len(self.employees):
            return None
        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            return self.employees[index.row()][1]
        return None
        
    def personnel_number(self, index):
        if index is None:
            return None
        if (0 > index.row() >= len(self.employees)):
            return None        
        return self.employees[index.row()][0]
    
class PositionTableModel(QAbstractTableModel):
    positions=[]
    COLUMNS = 5
    
    def __init__(self, parent=None):
        super(PositionTableModel, self).__init__(parent)
        
    def setPositionList(self, positions):
        self.positions = positions
        self.reset()
        
    def positionList(self):
        return self.positions
    
    def rowCount(self, index=QModelIndex()):
        return len(self.positions)
    
    def columnCount(self, index=QModelIndex()):
        return self.COLUMNS
    
    def data(self, index, role=Qt.DisplayRole):
        if index.row() < 0 or index.row() >= len(self.positions):
            return None
        if index.column() < 0 or index.column() >= self.COLUMNS - 1:
            return None
        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            return self.positions[index.row()][index.column() + 1]
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == 0:
                return "Название"
            elif section == 1:
                return "Разряд"
            elif section == 2:
                return "Категория"
            elif section == 3:
                return "Ставка"
        return None
    
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