import department.sql as sql
import PySide.QtCore as core
import PySide.QtGui as gui
from PySide.QtUiTools import QUiLoader

class MainWindow(gui.QMainWindow):
    ## Константы для кортежа, возаращаемого функцией Department::get_employee_info(int)
    PERSONNEL_NUMBER = 0
    CONTRACT_ID = 1
    SIGNED = 2
    TYPE = 3
    FULLNAME = 4
    GENDER = 5
    BIRTH = 6
    EDUCATION = 7
    DEGREE = 8
    PROGRAMME = 9
    FAMILY_STATUS = 10
    ADDRESS_2 = 11
    PHONE = 12
    EXPERIENCE = 13
    PASSPORT = 14
    ISSUE = 15
    AUTHORITY = 16
    ADDRESS_1 = 17
    
    ## Константы для кортежа, возаращаемого функцией Department::get_position_info(int)
    POSITION_ID = 0
    POSITION = 1
    RANK = 2
    CATEGORY = 3
    SALARY = 4
    RATE_AMOUNT = 5
    RATE_BOOKED = 6
    EMPLOYEES = 7 
    
    def __init__(self, application, department, parent=None):
        super(MainWindow, self).__init__(parent)
        self.department = department
        self.application = application
        
        self.ui = QUiLoader().load('view/mainwindow.ui')
        self.ui.err_output.setVisible(False)
        self.setCentralWidget(self.ui)
        
        self.employees = sql.EmployeeListModel()
        self.ui.employee_list_view.setModel(self.employees)
        self.update_employees_list()
        
        self.positions = sql.PositionTableModel()
        self.ui.position_table_view.setModel(self.positions)
        self.ui.position_table_view.setColumnWidth(1, 120)
        self.ui.position_table_view.setColumnWidth(3, 200)
        self.update_position_list()
        
        self.ui.search_btn.clicked.connect(self.update_employees_list)
        self.ui.employee_list_view.clicked.connect(self.set_employee_info)
        self.ui.education_cmb.currentIndexChanged.connect(self.enable_some_combo_box)
        self.ui.gender_cmb.currentIndexChanged[str].connect(self.update_family_status_combobox)
        self.ui.copy_address_btn.clicked.connect(self.copy_address)
        self.ui.clear_btn.clicked.connect(self.clear)
        self.ui.update_employee_btn.clicked.connect(self.update_employee)
        self.ui.add_employee_btn.clicked.connect(self.application.add_employee)
        self.ui.show_personnel_schedule_btn.clicked.connect(self.application.show_personnel_schedule)
        self.ui.accept_position_btn.clicked.connect(self.application.show_personnel_table)
        self.ui.reject_position_btn.clicked.connect(self.remove_from_position)
        self.application.data_changed.connect(self.update_position_list)
        
        self.update_family_status_combobox(self.ui.gender_cmb.currentText())
        self.ui.update_employee_btn.setEnabled(False)
        self.ui.position_table_view.hideColumn(self.positions.kCode)
        self.ui.position_table_view.hideColumn(self.positions.kRateAmount)
        self.ui.position_table_view.hideColumn(self.positions.kRateBooked)
        self.ui.position_table_view.hideColumn(self.positions.kEmployees)
        self.clear()
    
    ## Обновить список сотрудников в левой части окна
    @core.Slot()
    def update_employees_list(self):
        text = self.ui.search_le.text()
        if text == '' or text == "'":
            employees = self.department.get_employees_list()
        else:
            employees = self.department.get_employees_list(text)
        self.employees.setEmployeeList(employees)
        
    ## Обновить список должностей в нижней части окна
    @core.Slot()
    def update_position_list(self, employee_id=None):
        if employee_id is not None:
            positions = self.department.get_positions_list(employee_id)
            self.positions.setPositionList(positions)
        else:
            index = self.ui.employee_list_view.currentIndex()
            if 0 <= index.row() < self.employees.rowCount():
                employee_id = self.employees.employeesList()[index.row()][0]
                positions = self.department.get_positions_list(employee_id)
                self.positions.setPositionList(positions)
            else:
                self.positions.setPositionList([])
    
    ## Заполнить поля сотрудника или очищает его, если не указан индекс выделенного сотрудника
    @core.Slot('const QModelIndex &')
    def set_employee_info(self, index=None):
        self.ui.err_output.setVisible(False)
        is_ok = index is not None 
        if is_ok:
            employee_id = self.employees.personnel_number(index)
            employee = self.department.get_employee_info(employee_id)
        
        self.ui.fullname_le.setText(employee[self.FULLNAME] if is_ok else '')
        self.ui.gender_cmb.setCurrentIndex({'m':0, 'f':1}.get(employee[self.GENDER])
                                           if is_ok else 0)
        self.ui.family_status_cmb.setCurrentIndex(employee[self.FAMILY_STATUS]
                                                  if is_ok else 0)
        self.ui.birth_date.setDate(core.QDate.fromString(employee[self.BIRTH], 'd.MM.yyyy')
                                   if is_ok else core.QDate(1970, 1, 1))
        self.ui.education_cmb.setCurrentIndex({'высшее':0, 
                                               'высшее неоконченное':1, 
                                               'среднее неполное':2,
                                               'среднее полное':3,
                                               'среднее специальное':4}
                                              .get(employee[self.EDUCATION])
                                              if is_ok else 0)
        self.ui.programme_le.setText(employee[self.PROGRAMME] if is_ok else '')
        self.ui.experience_date.setDate(core.QDate.fromString(employee[self.EXPERIENCE], 'd.MM.yyyy')
                                        if is_ok else core.QDate(2000, 1, 1))
        self.ui.address_2_te.setPlainText(employee[self.ADDRESS_2] if is_ok else '')
        self.ui.phone_le.setText((str(employee[self.PHONE]) if employee[self.PHONE] is not None else None)
                                 if is_ok else '')
        
        passport = employee[self.PASSPORT].split(' ', 1) if is_ok else []
        self.ui.serial_le.setText(passport[0] if is_ok else '0000')
        self.ui.number_le.setText(passport[1] if is_ok else  '123456')
        self.ui.issue_date.setDate(core.QDate.fromString(employee[self.ISSUE], 'd.MM.yyyy')
                                   if is_ok else  core.QDate(2010, 1, 1))
        self.ui.authority_te.setPlainText(employee[self.AUTHORITY] if is_ok else '')
        self.ui.address_1_te.setPlainText(employee[self.ADDRESS_1] if is_ok else '')
        self.ui.contract_lbl.setText(self.tr('Контракт №{} заключён'.format(employee[self.CONTRACT_ID]))
                                     if is_ok else self.tr('Контракт заключён'))
        self.ui.signed_date.setDate(core.QDate.fromString(employee[self.SIGNED], 'd.MM.yyyy')
                                    if is_ok else  core.QDate(2010, 1, 1))
        self.ui.type_cmb.setCurrentIndex({'временный':0, 'постоянный':1}.get(employee[self.TYPE])
                                         if is_ok else 0)
        
        self.update_position_list(employee_id) if is_ok else self.positions.setPositionList([])
        self.ui.update_employee_btn.setEnabled(True)
        self.ui.add_employee_btn.setEnabled(False)
        self.ui.err_output.setVisible(False)
        
    @core.Slot()
    def remove_from_position(self):
        index = self.ui.position_table_view.currentIndex()
        if 0 <= index.row() < self.positions.rowCount():
            self.positions.removeRow(index.row())
        
    ## Делает активным или неактивном некоторые выпадающие списки
    @core.Slot()
    def enable_some_combo_box(self):
        text = self.ui.education_cmb.currentText()
        self.ui.degree_cmb.setEnabled(text == 'высшее')
        self.ui.programme_le.setEnabled(text in ('высшее', 'высшее неоконченное'))
    
    ## Обновляет список вариантов для семейного статуса в зависимости от выбранного полаы
    @core.Slot('const QString&')
    def update_family_status_combobox(self, string):
        self.ui.family_status_cmb.clear()
        if string == 'мужской':
            self.ui.family_status_cmb.addItems(['холост', 'женат', 'разведён', 'вдовец'])
        elif string == 'женский':
            self.ui.family_status_cmb.addItems(['не замужем', 'замужем', 'разведёна', 'вдова'])
    
    ## Коприует адрес из адреса проживания в адрес регистрации
    @core.Slot()
    def copy_address(self):
        text = self.ui.address_2_te.toPlainText()
        if text != '':
            self.ui.address_1_te.setPlainText(text)
    
    ## Очищает все поля        
    @core.Slot()
    def clear(self):
        self.set_employee_info(None)
        self.ui.update_employee_btn.setEnabled(False)
        self.ui.add_employee_btn.setEnabled(True)
        # Снять выделение
        self.ui.employee_list_view.setCurrentIndex(self.ui.employee_list_view.rootIndex())
        
    @core.Slot()
    def update_employee(self):
        self.application.update_employee(
            self.employees.personnel_number(self.ui.employee_list_view.currentIndex())
        )
    
    @core.Slot('tuple')
    def add_position(self, record):
        self.positions.insertData(record)
    
    def keyPressEvent(self, event):
        if event.key() in (core.Qt.Key_Return, core.Qt.Key_Enter):
            self.update_employees_list()