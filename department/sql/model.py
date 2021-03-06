import PySide.QtCore as core
from PySide.QtCore import Qt
import re

class EmployeeListModel(core.QAbstractListModel):
    
    employees=[]
    
    def __init__(self, parent=None):
        super(EmployeeListModel, self).__init__(parent)
                
    def setEmployeeList(self, employees):
        self.employees = employees
        self.reset()
        
    def employeesList(self):
        return self.employees
        
    def rowCount(self, index=core.QModelIndex()):
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
    
class PositionTableModel(core.QAbstractTableModel):
    
    data_changed = core.Signal(core.QModelIndex, core.QModelIndex)
    
    positions=[]
    kColumns = 9
    names = {'Код':0,
             'Должность':1,
             'Разряд':2,
             'Категория':3,
             'Ставка':4,
             'Зарплата':5,
             'Ставок':6,
             'Занято':7,
             'Сотрудников':8}
    
    kCode = 0
    kPosition = 1
    kRank = 2
    kCategory = 3
    kRate = 4
    kSalary = 5
    kRateAmount = 6
    kRateBooked = 7
    kEmployees = 8
    
    def __init__(self, parent=None):
        super(PositionTableModel, self).__init__(parent)
        
    def setPositionList(self, positions):
        self.positions = positions
        self.reset()
        
    def getPositionList(self):
        return self.positions
        
    def positionList(self):
        return self.positions
    
    def rowCount(self, index=core.QModelIndex()):
        return len(self.positions)
    
    def columnCount(self, index=core.QModelIndex()):
        return self.kColumns
    
    def data(self, index, role=Qt.DisplayRole):
        if index.row() < 0 or index.row() >= len(self.positions):
            return None
        if index.column() < 0 or index.column() >= self.kColumns:
            return None
        if role in (Qt.DisplayRole, Qt.ToolTipRole, Qt.EditRole):
            return self.positions[index.row()][index.column()]
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            # Меняем местами ключ со значенями в словаре names
            columns = dict([(v,k) for (k,v) in self.names.items()])
            # Возвращаем название по номеру столбца
            return self.tr(columns[section])
        return None
    
    def insertRow(self, position, index=core.QModelIndex()):
        return self.insertRows(position, 1, index)
    
    def insertData(self, record, index=core.QModelIndex()):
        if record is None or type(record) != type(tuple()):
            return False
        position = len(self.positions)
        # Добавляем ставку
        self.beginInsertRows(index, position, position-1)
        self.positions.insert(position, record)
        self.endInsertRows()
        self.reset()
        return True
    
    def insertRows(self, position, rows, index=core.QModelIndex()):
        self.beginInsertRows(index, position, position+rows-1)
        for row in range(0, rows):
            record = []
            for i in range(0, 9):
                record.append(None)
            self.positions.insert(position + row, tuple(record))
        self.endInsertRows()
        return True
    
    def removeRow(self, position, index=core.QModelIndex()):
        self.removeRows(position, 1, index)
    
    def removeRows(self, position, rows, index=core.QModelIndex()):
        self.beginRemoveRows(index, position, position+rows-1)
        for row in range(0, rows):
            self.positions.remove(self.positions[position])
        self.endRemoveRows()
        
    def setItem(self, row, column, value):
        if (0 <= row < len(self.positions)
            and 0 <= column < self.kColumns):
            record = list(self.positions[row])
            record[column] = value
            self.positions.remove(self.positions[row])
            self.positions.insert(row, tuple(record))
    
    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            row = index.row()
        
        record = list(self.positions[row])
        if value == record[index.column()]:
            return False
        # Если меняем ставку, то пересчитвааем зарплату
        if index.column() == self.kRate: 
            # Выставляем значение, близкое к тем, что есть в перечне
            values = (0.25, 0.5, 1.0)
            # Когда пользователь впервые редактирует
            # данные и она возвращается в качестве str()
            # все введёныые буквы меяем на 0
            # ^((\d+(\.|,\d*)?)|((\d*\.|,)?\d+))$ — число с ПТ с точкой или запятой в разделите
            if type(value) == type(str()):
                if not re.match(r'^((\d+(\.|,\d*)?)|((\d*\.|,)?\d+))$', value):
                    return False
                else: 
                    value = float(re.sub(',', '.', value))
            get_abs = lambda x : lambda y : abs(x - y)
            differ = list(map(get_abs(value), values))
            value = values[differ.index(min(differ))]
            # Пересчитываем зарплату
            salary = record[self.kSalary]
            # Когда значение ставки не указано — ставим по умолчанию 1
            # для корректного пересчёта
            currval = record[index.column()] if record[index.column()] is not None else 1
            record[self.kSalary] = (value * salary) / float(currval)
        # если меняем зарпату и меняем это в общем окне
        # отсеиваем такие действия, т.к. если модель меняется
        # у сотрудника, то у него есть сведенья о ставке
        # в списке должностей такой информации нет
        elif (index.column() == self.kSalary and
              record[self.kRate] is None):
            record[self.kSalary] = value
        elif index.column() == self.kRateAmount:
            pass
        else:
            return False
        
        # Выставляем новое значение и меняем кортеж с данными    
        record[index.column()] = value
        self.positions.remove(self.positions[row])
        self.positions.insert(row, tuple(record))
        
        self.data_changed.emit(index, index)
        return True
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() not in (self.kRate, 
                                  self.kSalary,
                                  self.kRateAmount):
            return Qt.ItemFlags(core.QAbstractTableModel.flags(self, index))
        return Qt.ItemFlags(core.QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable) 
    
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
        return self.__birth.toString('d.M.yyyy')
    @birth.setter
    def birth(self, date):
        self.__birth = core.QDate.fromString(date, 'd.M.yyyy')
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
            numbers = re.sub('\D', '', number)
            if numbers != '':
                self.__phone = int(numbers) 
            else:
                self.__phone = None
        else:
            self.__phone = None
    ## Дата начала опыта работы DATE
    #
    # В формате строки ('ГГГГ.ММ.ДД')
    __experience=None
    @property
    def experience(self):
        return self.__experience.toString('d.M.yyyy')
    @experience.setter
    def experience(self, date):
        self.__experience =  core.QDate.fromString(date, 'd.M.yyyy')
    ## Номер паспрорта VARCHAR
    passport=None
    ## Дата выдачи паспорта DATE
    __issue=None
    @property
    def issue(self):
        return self.__issue.toString('d.M.yyyy')
    @issue.setter
    def issue(self, date):
        self.__issue =  core.QDate.fromString(date, 'd.M.yyyy')
    ## Кем выдан TEXT
    authority=None
    ## Даата подписания контракта DATE
    __signed=None
    @property
    def signed(self):
        return self.__signed.toString('d.M.yyyy')
    @signed.setter
    def signed(self, date):
        self.__signed =  core.QDate.fromString(date, 'd.M.yyyy')
    ## Тип контракта (времменый, постоянный) VARCHAR
    type=None

class Position():
    #Ид
    id=None
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
    # Занятых ставо
    rate_booked=None
    # Число сотрудников
    employees=None