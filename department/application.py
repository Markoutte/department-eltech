import psycopg2
import department.sql as sql
import department.view as view
import PySide.QtCore as core
import PySide.QtGui as gui

class Application(gui.QApplication):
    
    def __init__(self, argv):
        super(Application, self).__init__(argv)
        codec = core.QTextCodec.codecForName('UTF8')
        core.QTextCodec.setCodecForTr(codec)
        self.conn = psycopg2.connect(dbname='department', user='postgres', password='postgres')
        self.department = sql.Department(self.conn)
        
        self.mw = view.MainWindow(self, self.department)
        self.mw.setWindowTitle('Управление кадрами')
        self.mw.resize(800, 600)
        self.mw.setMinimumSize(800, 480)
        self.mw.show()
        
        ## connections
        self.connect(self.mw, core.SIGNAL('updateEmployee(int)'), 
                     self, core.SLOT('updateEmployee(int)'))
        self.connect(self.department, core.SIGNAL('dataChanged(bool)'),
                     self, core.SLOT('rollback(bool)'))
    
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
        
        is_employee_updated = self.department.update_employee(employee_id,
            fullname = ui.fullname_le.text() if ui.fullname_le.text() not in ("", "'") else None, 
            family_status = ui.family_status_cmb.currentIndex(), 
            gender = {0:'m', 1:'f'}.get(ui.gender_cmb.currentIndex()), 
            birth = ui.birth_date.date().toString('d.M.yyyy'), 
            education = ui.education_cmb.currentText(), 
            degree = ui.degree_cmb.currentText() if ui.degree_cmb.isEnabled() else None, 
            programme = ui.programme_le.text() if ui.programme_le.isEnabled() and ui.programme_le.text() not in ("", "'") else None, 
            experience = ui.experience_date.date().toString('d.M.yyyy'), 
            address = ui.address_2_te.toPlainText() if ui.address_2_te.toPlainText() not in ("", "'") else None, 
            phone = int(ui.phone_le.text()) if ui.phone_le.text() not in ("", "'") else None,         
        )
        
        is_passport_updated = self.department.update_passport(employee[14],
            id = ("{} {}".format(ui.serial_le.text(), ui.number_le.text())), 
            issue = ui.issue_date.date().toString('d.M.yyyy'), 
            authority = ui.authority_te.toPlainText() if ui.authority_te.toPlainText() not in ("", "'") else None, 
            address = ui.address_1_te.toPlainText() if ui.address_1_te.toPlainText() not in ("", "'") else None
        )
        
        is_contract_updated = self.department.update_contract(employee[1],
            signed = ui.signed_date.date().toString('d.M.yyyy'),
            type = ui.type_cmb.currentText()
        )
        
        is_updated = is_employee_updated and is_passport_updated and is_contract_updated
        self.acceptChanges(is_updated)
        if is_updated:
            ui.err_output.setVisible(False)
        else:
            ui.err_output.setText(self.department.get_error())
            ui.err_output.setVisible(True)
            