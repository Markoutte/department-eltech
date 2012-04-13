""" MainWindow contains general window which is entry point for user 
""" 
from  db.database import DataBase
from PyQt4.QtGui import QMainWindow, QWidget, QGridLayout, QTableWidget, QTableWidgetItem


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        # set up main window
        super(MainWindow, self).__init__(parent)
        centralWidget = QWidget()
        centralLayout = QGridLayout();
        centralWidget.setLayout(centralLayout)
        self.setCentralWidget(centralWidget)

        # main table        
        db = DataBase("test_db", "postgres", "postgres")
        rows = db.selectAll("human")
        
        self.__table = QTableWidget(len(rows), 4)
        self.__table.verticalHeader().setVisible(False)
        self.__table.setHorizontalHeaderLabels(["Id", "Имя", "Фамилия", "Телефон"])
        centralLayout.addWidget(self.__table, 0, 0, 1, 1)
        
        if (rows != None):
            for (x, row) in enumerate(rows):
                for (y, item) in enumerate(row):
                    self.__table.setItem(x, y, QTableWidgetItem("%s" % item if (item != None) else None))

        # self.connect(self.__button, QtCore.SIGNAL("pressed()"), self.changeText)