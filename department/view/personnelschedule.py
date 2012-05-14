import department.sql as sql
import PySide.QtGui as gui
import PySide.QtCore as core
from PySide.QtUiTools import QUiLoader

class PersonnelSchedule(gui.QMainWindow):
    
    TableEditor = 1
    PositionManager = 2
    
    def __init__(self, application, department, parent=None):
        super(PersonnelSchedule, self).__init__(parent)
        self.application = application
        self.department = department
        
        self.ui = QUiLoader().load('view/personnelschedule.ui')
        self.setCentralWidget(self.ui)
        
        self.positions = sql.PositionTableModel()
        p_list = department.get_positions_list()
        self.positions.setPositionList(p_list)
        self.ui.position_table_view.setModel(self.positions)
        self.ui.position_table_view.setColumnWidth(1, 120)
        self.ui.position_table_view.setColumnWidth(3, 200)
        self.ui.position_table_view.hideColumn(self.positions.names['Код'])
        
        self.ui.position_le.setCompleter(self.__get_completer(self.positions,
                                                              self.positions.names['Должность']))
        cat_list = []
        for row in p_list:
            value = row[self.positions.names['Категория']]
            if value not in cat_list:
                self.ui.category_cmb.addItem(value)
                
        self.connect(self.ui.position_table_view, core.SIGNAL('doubleClicked(const QModelIndex&)'),
                     self, core.SLOT('closeWithPositionCode(const QModelIndex&)'))
        
    def __get_completer(self, model, column=0):
        completer = gui.QCompleter()
        completer.setModel(model)
        completer.setCompletionMode(gui.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(core.Qt.CaseInsensitive)
        completer.setCompletionColumn(column)
        return completer
    
    @core.Slot('const QModelIndex&')
    def closeWithPositionCode(self, index):
        positions = self.positions.getPositionList()
        row = index.row()
        if row < 0 or row >= len(positions):
            return
        self.emit(core.SIGNAL('positionChose(int)'), positions[row][0])
        self.close()
        
        