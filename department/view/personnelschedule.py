import department.sql as sql
import PySide.QtCore as core
import PySide.QtGui as gui
from PySide.QtUiTools import QUiLoader

class PersonnelSchedule(gui.QMainWindow):
    
    add_position = core.Signal()
    delete_position = core.Signal(int)
    update_position = core.Signal(int, int, int)
    
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
        self.ui.position_table_view.hideColumn(self.positions.kCode)
        
        self.ui.err_output.setVisible(False)
        
        self.ui.position_le.setCompleter(self.__get_completer(self.positions,
                                                              self.positions.kPosition))
        self.ui.position_table_view.hideColumn(self.positions.kRate)
        cat_list = []
        for row in p_list:
            value = row[self.positions.kCategory]
            if value not in cat_list:
                self.ui.category_cmb.addItem(value)
                
        self.ui.add_position_btn.clicked.connect(self.add_position)
        self.ui.delete_position_btn.clicked.connect(self.delete_position_from_table)
        self.positions.data_changed.connect(self.update_position_item)
        self.department.data_changed.connect(self.update_position_list)
        
    @core.Slot()
    def update_position_list(self):
        positions = self.department.get_positions_list()
        self.positions.setPositionList(positions)
        self.ui.position_le.setText('')
        self.ui.rank_le.setText('')
        self.ui.salary_le.setText('')
        self.ui.rate_amount_le.setText('')
            
    def __get_completer(self, model, column=0):
        completer = gui.QCompleter()
        completer.setModel(model)
        completer.setCompletionMode(gui.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(core.Qt.CaseInsensitive)
        completer.setCompletionColumn(column)
        return completer
    
    @core.Slot()
    def delete_position_from_table(self):
        positions = self.positions.getPositionList()
        index = self.ui.position_table_view.currentIndex()
        row = index.row()
        if 0 <= row < len(positions):
            self.delete_position.emit(positions[row][0])
    
    @core.Slot('QModelIndex')
    def update_position_item(self, index):
        positions = self.positions.getPositionList()
        self.update_position.emit(positions[index.row()][0], index.column(),
                                 positions[index.row()][index.column()])
        
class PersonnelTable(gui.QMainWindow):
    
    positionChose = core.Signal(int)
    
    def __init__(self, department, parent=None):
        super(PersonnelTable, self).__init__(parent)
        self.department = department
        self.model = sql.PositionTableModel()
        self.model.setPositionList(department.get_positions_list())
        self.table = gui.QTableView()
        self.table.setEditTriggers(0)
        self.table.setModel(self.model)
        
        self.table.setHorizontalScrollMode(gui.QAbstractItemView.ScrollPerPixel)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(20)
        self.table.horizontalHeader().setDefaultSectionSize(60)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(gui.QAbstractItemView.SelectRows)
        self.table.setVerticalScrollMode(gui.QAbstractItemView.ScrollPerPixel)
        self.table.setSelectionMode(gui.QAbstractItemView.SingleSelection)
        self.table.hideColumn(sql.model.PositionTableModel.kCode)
        self.table.hideColumn(sql.model.PositionTableModel.kRate)
            
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(3, 200)
            
        self.setCentralWidget(self.table)
        
        self.table.doubleClicked.connect(self.close_with_position_code)
        
    @core.Slot('QModelIndex')
    def close_with_position_code(self, index=None):
        if index is None:
            index = self.table.currentIndex()
        positions = self.model.getPositionList()
        row = index.row()
        if row < 0 or row >= len(positions):
            return
        self.positionChose.emit(positions[row][0])
        self.close()