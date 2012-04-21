""" MainWindow contains general window which is entry point for user 
"""
import department.database as db
from functools import partial
from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL, QObject

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

        self.__person_ls = QListView()
        self.__person_ls.setModel(QStringListModel(["One", "Two", "Three"]))
        self.__grid.addWidget(self.__person_ls, 0, 0, 3, 1)

        # main table                
        self.__table = QTableWidget()
        self.__table.verticalHeader().setVisible(False)


    def closeEvent(self, event):
        db.close(self.__con())

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