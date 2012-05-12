import PySide.QtCore as Core

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