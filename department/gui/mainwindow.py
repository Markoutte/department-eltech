
""" MainWindow contains general window which is entry point for user
"""
#from department.database import Connection, close
from department.gui.widgets import PersonListView
from department.gui.widgets import Information
from functools import partial
from PyQt4.QtGui import *
import PyQt4.QtCore as core

class MainWindow(QMainWindow):

    __db_name_le = None
    __user_le = None
    __pass_le = None
    __host_le = None
    __grid= None

    def __init__(self, parent=None):
        # set up main window
        super(MainWindow, self).__init__(parent)
        centralWidget = QWidget()
        self.__grid = QGridLayout();
        centralWidget.setLayout(self.__grid)
        self.setCentralWidget(centralWidget)

        # Set a list view of persons
        person_ls = PersonListView()
        self.__grid.addWidget(person_ls, 0, 0, 1, 1)
        self.__grid.setColumnStretch(0, 1)

        # Set full info about person
        info_tb = Information()
        self.__grid.addWidget(info_tb, 0, 1, 1, 1, core.Qt.AlignTop)
        self.__grid.setColumnStretch(1, 3)

        core.QObject.connect(person_ls, core.SIGNAL('personSelected(int)'),
                        info_tb, core.SLOT('updateInfo(int)'))


    def closeEvent(self, event):
        pass

    ### SLOTS

    def connect(self):
        self.__conn = db.connect(dbname=self.__db_name_le.text()
                                #user = self.__user_le.text(),
                                #password = self.__pass_le.text(),
                                #host self.__host_le.text()
        )

        if (not db.is_connected(self.__conn())):
            return

        do_query = partial(db.do_query(self.__conn()))

        columns = do_query("select column_name from information_schema.columns where table_name='{0}';".format("human"))
        col_names = []
        for col in columns:
            col_names.insert(0, col[0])

        rows = do_query("SELECT * FROM human")
        self.__table.setColumnCount(len(col_names))
        self.__table.setRowCount(len(rows))
        self.__table.setHorizontalHeaderLabels(col_names)

        if (rows != None):
            for (x, row) in enumerate(rows):
                for (y, item) in enumerate(row):
                    self.__table.setItem(x, y, QTableWidgetItem("%s" % item if (item != None) else None))

                ### PRIVATE FUNCTION

    def __add_top_panel(self):
        self.__db_name_le = QLineEdit()
        db_layout = QHBoxLayout()
        db_layout.addWidget(QLabel("База данных"))
        db_layout.addWidget(self.__db_name_le)
        self.__grid.addLayout(db_layout, 0, 0)

        self.__user_le = QLineEdit()
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Пользователь"))
        user_layout.addWidget(self.__user_le)
        self.__grid.addLayout(user_layout, 0, 1)

        self.__pass_le = QLineEdit()
        self.__pass_le.setEchoMode(QLineEdit.Password)
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(QLabel("Пароль"))
        pass_layout.addWidget(self.__pass_le)
        self.__grid.addLayout(pass_layout, 0, 2)

        self.__host_le = QLineEdit()
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("Хост"))
        host_layout.addWidget(self.__host_le)
        self.__grid.addLayout(host_layout, 0, 3)

        connect_btn = QPushButton("Подключить")
        self.__grid.addWidget(connect_btn, 0, 4)

        QObject.connect(connect_btn, SIGNAL("pressed()"), self.connect)