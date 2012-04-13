import sys
from gui.mainwindow import MainWindow
from PyQt4.QtGui import *
from PyQt4.QtCore import QSize

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.resize(QSize(460, 200))
    mw.setWindowTitle("Department tool")
    mw.show()
    app.exec_()

if __name__ == "__main__":
    main()