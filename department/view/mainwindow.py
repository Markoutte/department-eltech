import department.sql as sql
import PySide.QtGui as gui
from PySide.QtUiTools import QUiLoader

class MainWindow(gui.QMainWindow):
    
    def __init__(self, department, parent=None):
        super(MainWindow, self).__init__(parent)
        self.department = department
        self.ui = QUiLoader().load('view/mainwindow.ui')
        self.setCentralWidget(self.ui)
        
        self.employees = sql.EmployeeListModel()
        self.ui.employee_list_view.setModel(self.employees)
        
    def set_employees_list(self, employees):
        self.employees.setEmployeeList(employees)