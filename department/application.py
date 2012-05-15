import psycopg2
import department.sql as sql
import department.view as view
import PySide.QtCore as core
import PySide.QtGui as gui

class Application(gui.QApplication):
    
    dataChanged = core.Signal()
    
    def __init__(self, argv):
        super(Application, self).__init__(argv)
        codec = core.QTextCodec.codecForName('UTF8')
        core.QTextCodec.setCodecForTr(codec)
        self.conn = psycopg2.connect(dbname='department', user='postgres', password='postgres')
        self.department = sql.Department(self.conn)
        
        # Главное окно программы
        self.mw = view.MainWindow(self, self.department)
        self.mw.setWindowTitle(self.tr('Управление кадрами'))
        self.mw.resize(960, 620)
        self.mw.setMinimumSize(800, 480)
        self.mw.setMaximumSize(1280, 800)
        self.mw.show()
        
        ## connections
#        self.connect(self.department, core.SIGNAL('updateDatabase(bool)'),
#                     self, core.SLOT('rollback(bool)'))
        self.department.updateDatabase.connect(self.rollback)
#        core.QObject.connect(self, core.SIGNAL('aboutToQuit()'), self.close)
        self.aboutToQuit.connect(self.close)
    
    def close(self):
        self.department.close()
        self.conn.close()
    
    @core.Slot('bool')
    def rollback(self, ok):
        if not ok:
            self.conn.rollback()
        
    def acceptChanges(self, ok):
        if ok:
            self.conn.commit()
        else:
            self.conn.rollback()
            
    @core.Slot('int')
    def updateEmployee(self, employee_id):
        ui = self.mw.ui
        employee = self.department.get_employee_info(employee_id)
        empl = self.__get_employee()
        
        is_employee_updated = self.department.update_employee(employee_id,
            fullname = empl.fullname, 
            family_status = empl.family_status, 
            gender = empl.gender, 
            birth = empl.birth, 
            education = empl.education, 
            degree = empl.degree, 
            programme = empl.programme, 
            experience = empl.experience, 
            address = empl.address_2, 
            phone = empl.phone,         
        )
        
        
        if not is_employee_updated:            
            return self.__show_err(self.mw.ui, is_employee_updated == False,
                                   self.department.get_error() if not is_employee_updated else "")
        
        is_passport_updated = self.department.update_passport(employee[14],
            id = empl.passport, 
            issue = empl.issue, 
            authority = empl.authority, 
            address = empl.address_1
        )
        if not is_passport_updated:
            return self.__show_err(self.mw.ui, is_passport_updated == False,
                                   self.department.get_error() if not is_passport_updated else "")
        is_contract_updated = self.department.update_contract(employee[1],
            signed = empl.signed,
            type = empl.type
        )
        
        # Комитим изменения в БД, если удалось всё выполнить
        is_updated = is_employee_updated and is_passport_updated and is_contract_updated
        self.acceptChanges(is_updated)
        if is_updated:
            # Обновить сведенья о занимаемых должностях
            self.__update_employee_position(employee_id)
            ui.err_output.setVisible(False)
        else:
            return self.__show_err(self.mw.ui, is_updated == False,
                                   self.department.get_error() if not is_updated else '')
        
            
    @core.Slot()
    def addEmployee(self):
        current_positions = self.mw.positions.getPositionList()
        employee = self.__get_employee()
        employee_id = self.department.add_employee(employee)
        self.acceptChanges(employee_id != 0)
        if employee_id == 0:
            self.mw.positions.setPositionList(current_positions)
            return self.__show_err(self.mw.ui, employee_id == 0, 
                                   self.department.get_error() if employee_id == 0 else "")
        
        ids = [x[0] for x in current_positions]
        RATE = 4
        rates = [x[RATE] for x in current_positions]
        for i, position_id in enumerate(ids):
            ok = self.department.set_position(employee_id, position_id, rates[i])
            self.acceptChanges(ok)
        
        self.mw.updateEmployeesList()
        
    @core.Slot()
    def showPersonnelSchedule(self):
        # Штатное расписание
        self.ps = self.__show_personnal_schedule_window()
#        self.connect(self.ps, core.SIGNAL('addPosition()'), self, core.SLOT('addPosition()'))
        self.ps.addPosition.connect(self.addPosition)
#        self.connect(self.ps, core.SIGNAL('deletePosition(int)'), self, core.SLOT('deletePosition(int)'))
        self.ps.deletePosition.connect(self.deletePosition)
#        self.connect(self.ps, core.SIGNAL('updatePosition(int, QString, int)'), self, core.SLOT('updatePosition(int, QString, int)'))
        self.ps.updatePosition.connect(self.updatePosition)
        self.ps.show()
        
    @core.Slot()
    def showPersonnelTable(self):
        self.pt = view.PersonnelTable(self.department, self.mw)
        self.pt.resize(680, 480)
        self.pt.setMinimumSize(640, 480)
        self.pt.setMaximumSize(800, 800)   
        self.pt.show()
#        self.connect(self.pt, core.SIGNAL('positionChose(int)'),
#                     self, core.SLOT('addPositionToList(int)'))
        self.pt.positionChose.connect(self.addPositionToList)
        
    @core.Slot('int')
    def addPositionToList(self, position_id):
        # Проверка на факт уже наличия такой должности в списке
        current_positions = self.mw.positions.getPositionList()
        if position_id in [x[0] for x in current_positions]:
            return
        self.mw.addPosition(self.department.get_position_info(position_id))
        # В новой записи, которая появится в конце, — ставка равно 1.0 
        RATE = 4
        self.mw.positions.setItem(len(current_positions) - 1, RATE, 1.0)
        
    @core.Slot()
    def addPosition(self):
        ui = self.ps.ui
        position = sql.Position()
        position.position = ui.position_le.text() if ui.position_le.text() not in ("", "'") else None
        position.rank = ui.rank_le.text() if ui.rank_le.text() not in ("", "'") else None
        position.category = ui.category_cmb.currentText() if ui.category_cmb.currentText() not in ("", "'") else None
        position.rate_amount = ui.rate_amount_le.text() if ui.rate_amount_le.text() not in ("", "'") else None
        position.salary =  ui.salary_le.text() if ui.salary_le.text() not in ("", "'") else None
        is_added = self.department.add_position(position)
        self.acceptChanges(is_added)
        self.__show_err(self.ps.ui, is_added == False, 
                                   self.department.get_error() if not is_added else "")
        
    @core.Slot('int')
    def deletePosition(self, position_id):
        is_ok = self.department.delete_position(position_id)
        self.acceptChanges(is_ok)
        
    @core.Slot('int', 'QString', 'int')
    def updatePosition(self, position_id, field, value):
        if field == 'Зарплата':
            arg = {'salary':value}
        elif field == 'Ставок':
            arg = {'rate_amount':value}
        else:
            return
        is_ok = self.department.update_position(position_id, **arg)
        self.acceptChanges(is_ok)
        
    
    def __get_employee(self):
        ui = self.mw.ui
        employee = sql.Employee()
        employee.fullname = ui.fullname_le.text() if ui.fullname_le.text() not in ("", "'") else None
        employee.family_status = ui.family_status_cmb.currentIndex() 
        employee.gender = {0:'m', 1:'f'}.get(ui.gender_cmb.currentIndex()) 
        employee.birth = ui.birth_date.date().toString('d.M.yyyy') 
        employee.education = ui.education_cmb.currentText()
        employee.degree = ui.degree_cmb.currentText() if ui.degree_cmb.isEnabled() else None 
        employee.programme = ui.programme_le.text() if ui.programme_le.isEnabled() and ui.programme_le.text() not in ("", "'") else None
        employee.experience = ui.experience_date.date().toString('d.M.yyyy') 
        employee.address_2 = ui.address_2_te.toPlainText() if ui.address_2_te.toPlainText() not in ("", "'") else None 
        employee.phone = ui.phone_le.text() if ui.phone_le.text() not in ("", "'") else None
        employee.passport = ("{} {}".format(ui.serial_le.text(), ui.number_le.text()))
        employee.issue = ui.issue_date.date().toString('d.M.yyyy')
        employee.authority = ui.authority_te.toPlainText() if ui.authority_te.toPlainText() not in ("", "'") else None 
        employee.address_1 = ui.address_1_te.toPlainText() if ui.address_1_te.toPlainText() not in ("", "'") else None
        employee.signed = ui.signed_date.date().toString('d.M.yyyy')
        employee.type = ui.type_cmb.currentText()
        return employee
    
    def __show_err(self, window, status, error):
        window.err_output.setText(error)
        window.err_output.setVisible(status)
        
    def __show_personnal_schedule_window(self):
        ps = view.PersonnelSchedule(self, self.department, self.mw)
        ps.setWindowTitle(self.tr('Штатное расписание'))
        ps.resize(680, 480)
        ps.setMinimumSize(640, 480)
        ps.setMaximumSize(800, 800)        
        return ps
    
    def __update_employee_position(self, employee_id):
        if employee_id <= 0:
            return False
        RATE = self.mw.positions.names['Ставка']
        employee_position = self.department.get_positions_list(employee_id)
        current_position = self.mw.positions.getPositionList()
        # Получить список id из модели (список кортежей [()])
        ids = lambda l : set([x[0] for x in l])
        # Список значения конкрентного столбца i в моделе l
        items_list = lambda i : lambda l : [x[i] for x in l]
        empl = ids(employee_position)
        curr = ids(current_position)
        intersect = ids(current_position) & ids(employee_position)

        # Позиции для снятия с должности
        for position_id in empl - intersect:
            ok = self.department.remove_position(employee_id, position_id)
            self.acceptChanges(ok)
        # Список из passport_id
        ids = items_list(0)(current_position)
        # Позиции для назначения на должности
        for position_id in curr - intersect:
            index = ids.index(position_id)
            ok = self.department.set_position(employee_id, position_id, current_position[index][RATE])
            self.acceptChanges(ok)
        ids = items_list(0)(current_position)
        # Списки со щначениями ставок
        e_il = items_list(RATE)(employee_position)
        c_il = items_list(RATE)(current_position)
        # Позиции, которые, возможно, нужно изменить
        for position_id in intersect:
            index = ids.index(position_id)
            if e_il[index] != c_il[index]:                
                ok = self.department.set_rate(employee_id, position_id, 
                                              current_position[index][RATE])
                self.acceptChanges(ok)
        
        
        