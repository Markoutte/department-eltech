import sys
from department.gui.mainwindow import MainWindow
from PyQt4.QtGui import QApplication

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.set_full_name('Пелевин Максим Сергеевич')
    mw.show()
    app.exec_()

if __name__ == '__main__':
    main()
