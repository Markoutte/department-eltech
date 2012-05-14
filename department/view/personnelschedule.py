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
        
        self.ui.err_output.setVisible(False)
        
        self.ui.position_le.setCompleter(self.__get_completer(self.positions,
                                                              self.positions.names['Должность']))
        self.ui.position_table_view.hideColumn(self.positions.names['Ставка'])
        cat_list = []
        for row in p_list:
            value = row[self.positions.names['Категория']]
            if value not in cat_list:
                self.ui.category_cmb.addItem(value)
                
        self.connect(self.ui.add_position_btn, core.SIGNAL('clicked()'),
                     self, core.SIGNAL('addPosition()'))
        self.connect(self.ui.delete_position_btn, core.SIGNAL('clicked()'),
                     self, core.SLOT('deletePosition()'))
        self.connect(self.positions, core.SIGNAL('dataChanged(QModelIndex, QModelIndex)'),
                     self, core.SLOT('updatePosition(QModelIndex)'))
        self.connect(self.ui.accept_position_btn, core.SIGNAL('clicked()'),
                     self, core.SLOT('closeWithPositionCode()'))
        self.connect(self.department, core.SIGNAL('dataChanged()'), 
                     self, core.SLOT('updatePositionList()'))
        
    @core.Slot()
    def updatePositionList(self):
        positions = self.department.get_positions_list()
        self.positions.setPositionList(positions)
            
    def __get_completer(self, model, column=0):
        completer = gui.QCompleter()
        completer.setModel(model)
        completer.setCompletionMode(gui.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(core.Qt.CaseInsensitive)
        completer.setCompletionColumn(column)
        return completer
    
    @core.Slot()
    @core.Slot('const QModelIndex&')
    def closeWithPositionCode(self, index=None):
        if index is None:
            index = self.ui.position_table_view.currentIndex()
        positions = self.positions.getPositionList()
        row = index.row()
        if row < 0 or row >= len(positions):
            return
        self.emit(core.SIGNAL('positionChose(int)'), positions[row][0])
        self.close()
    
    @core.Slot()
    def deletePosition(self):
        positions = self.positions.getPositionList()
        index = self.ui.position_table_view.currentIndex()
        row = index.row()
        if 0 <= row < len(positions):
            self.emit(core.SIGNAL('deletePosition(int)'), positions[row][0])
    
    @core.Slot('QModelIndex')
    def updatePosition(self, index):
        columns = dict([(v,k) for (k,v) in self.positions.names.items()])
        positions = self.positions.getPositionList()
        self.emit(core.SIGNAL('updatePosition(int, QString, int)'), 
                  positions[index.row()][0], 
                  columns[index.column()],
                  positions[index.row()][index.column()])
        