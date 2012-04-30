
""" MainWindow contains general window which is entry point for user
"""
import PyQt4.QtGui as ui
import PyQt4.QtCore as core
from department.gui.widgets import PersonListView

class MainWindow(ui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.__compose()
        self.setWindowTitle("Кадровый учёт")

    def __compose(self):
        """Compose all widgets into one window"""
        # create two panels
        left_panel = ui.QVBoxLayout()
        right_panel = ui.QVBoxLayout()

        # compose left panel
        search_bx = ui.QLineEdit()
        left_panel.addWidget(search_bx)
        self.__persons_ls = PersonListView()
        left_panel.addWidget(self.__persons_ls)
        add_new_person_btn = ui.QPushButton('+ сотрудник') # TODO connect it
        left_panel.addWidget(add_new_person_btn)
        set_position_btn = ui.QPushButton('+ должность') # TODO connect it

        #compose right panel
        self.__full_name_lbl = ui.QLabel()
        right_panel.addWidget(self.__full_name_lbl)
        self.__pos_tbl = ui.QTableView() # TODO create corresponding widget
        right_panel.addWidget(self.__pos_tbl)
        self.__full_info_panel = ui.QGridLayout() # TODO corresponding layout
        right_panel.addLayout(self.__full_info_panel)

        # connect signals
        core.QObject.connect(search_bx, core.SIGNAL('textChanged (const QString&)'),
                             self.__persons_ls, core.SLOT('update(const QString&)'))
        core.QObject.connect(add_new_person_btn, core.SIGNAL('clicked()'), self, core.SIGNAL('addNewPerson()'))
        core.QObject.connect(set_position_btn, core.SIGNAL('clicked()'), self, core.SIGNAL('setPosition()'))
        core.QObject.connect(self.__persons_ls, core.SIGNAL('personSelected(const QString&)'),
                             self, core.SLOT('set_full_name(const QString&)'))

        # compose all in one
        main_layout = ui.QHBoxLayout()
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 3)
        main_widget = ui.QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # customize panels
        left_panel.setMargin(5)
        right_panel.setMargin(5)

    @core.pyqtSlot('const QString&')
    def set_full_name(self, fullname):
        '''This slot sets full name into label when signal arrives'''
        self.__full_name_lbl.setText('<font size=18>{}</font>'.format(fullname))