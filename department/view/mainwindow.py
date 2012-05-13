import department.sql as sql
import PySide.QtGui as gui
import PySide.QtCore as core
from PySide.QtUiTools import QUiLoader

class MainWindow(gui.QMainWindow):
    
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
        self.ui.position_table_view.setColumnWidth(0, 160)
        self.ui.position_table_view.setColumnWidth(1, 80)
        self.ui.position_table_view.setColumnWidth(2, 200)
        self.ui.position_table_view.setColumnWidth(3, 80)
        self.update_position_list()
        
        self.connect(self.ui.search_btn, core.SIGNAL('clicked()'), self, core.SLOT('update_employees_list()'))
        self.connect(self.ui.employee_list_view, core.SIGNAL('doubleClicked(const QModelIndex &)'),
                     self, core.SLOT('update_employee_info(const QModelIndex &)'))
        
    @core.Slot()
    def update_employees_list(self):
        text = self.ui.search_le.text()
        if text == '' or text == "'":
            employees = self.department.get_employees_list()
        else:
            employees = self.department.get_employees_list(text)
        self.employees.setEmployeeList(employees)
        
    @core.Slot()
    def update_position_list(self, employee_id=None):
        if employee_id is None:
            return
        positions = self.department.get_positions_list(employee_id)
        self.positions.setPositionList(positions)
        
    @core.Slot('const QModelIndex &')
    def update_employee_info(self, index):
        self.update_position_list(self.employees.personnel_number(index))
        
    def keyPressEvent(self, event):
        if event.key() in (core.Qt.Key_Return, core.Qt.Key_Enter):
            self.update_employees_list()