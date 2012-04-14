""" MainWindow contains general window which is entry point for user 
""" 
from  db.database import DB
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

        # add top panel
        self.__add_top_panel()

        # main table                
        self.__table = QTableWidget()
        self.__table.verticalHeader().setVisible(False)
        self.__grid.addWidget(self.__table, 1, 0, 1, 5)

        
    def closeEvent(self, event):
        DB().close()
        
### SLOTS

    def connect(self):
        db = DB()
        db.connect(self.__db_name_le.text(),
                   #self.__user_le.text(),
                   #self.__pass_le.text(),
                   #self.__host_le.text()
                   )
        
        if (not db.is_connected()):
            return
                
        columns = db.get_columns_name("human")
        col_names = []
        for col in columns:
            col_names.insert(0, col[0])
        
        rows = db.select_all("human")
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
        