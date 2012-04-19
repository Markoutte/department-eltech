import sys
from department.gui.mainwindow import MainWindow
from PyQt4.QtGui import *
from PyQt4.QtCore import QSize

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.resize(QSize(600, 200))
    mw.setWindowTitle("Кадровый учёт")
    mw.show()
    app.exec_()

if __name__ == "__main__":
    main()