
""" MainWindow contains general window which is entry point for user
"""
import PySide.QtGui as ui
import PySide.QtCore as core
import department.database.queries as _query
import department.gui.widgets as _widgets
import PySide.QtUiTools as ui_loader

class MainWindow(ui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setMinimumSize(600, 480)

        loader = ui_loader.QUiLoader(parent)
        self._ui = loader.load('gui/mainwindow.ui')
        self.setCentralWidget(self._ui)
        
        # init some widgets        
        self._ui.switch_bx.addItems(['Сотрудники', 'Должности'])

        # load person list view
        self.__persons_ls = _widgets.PersonListView(self)
        policy = ui.QSizePolicy()
        policy.setVerticalPolicy(ui.QSizePolicy.Fixed)
        policy.setHorizontalPolicy(ui.QSizePolicy.Expanding)
        self.__persons_ls.setSizePolicy(policy)
        central_layout = self._ui.layout()
        central_layout.insertWidget(1, self.__persons_ls)

        # set connection
        core.QObject.connect(self._ui.find_btn, core.SIGNAL('clicked()'),
            self, core.SLOT('send_query()'))
        core.QObject.connect(self.__persons_ls, core.SIGNAL('personSelected(int)'),
                             self, core.SLOT('fill_info(int)'))
        
        self.setWindowTitle("Кадровый учёт")
        
    @core.Slot()
    def send_query(self):
        """
        when <i>find_button</i> is clicked updates list with employees
        """
        self.__persons_ls.update(self._ui.search_bx.text())
        
    def keyPressEvent(self, event):
        if event.key() in (core.Qt.Key_Return, core.Qt.Key_Enter):
            self.send_query()
            
    @core.Slot('int')
    def fill_info(self, person_id):
        """
        fill info panel with data
        """
        full_info = _query.get_full_info(person_id)
        if full_info is None:
            return
        self._ui.fullname_lbl.setText('<b>{} {} {}</b>'.format(full_info[0][1], full_info[0][2], full_info[0][3]))
            