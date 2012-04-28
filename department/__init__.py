import sys
from department.gui.mainwindow import MainWindow
from department.database import *
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QObject, SIGNAL, SLOT

class Application(QApplication):
    def load(self, db):
        con = Connection().init(dbname=db)
        if not is_connected(con):
            con = None
            return False
        return True

    def close(self):
        Connection().close()

def main():

    #show window
    app = Application(sys.argv)
    QObject.connect(app, SIGNAL('aboutToQuit()'), app.close)
    if (not app.load('department_db')):
        return

    mw = MainWindow()
    mw.resize(QSize(600, 200))
    mw.setWindowTitle("Кадровый учёт")
    mw.show()
    app.exec_()

if __name__ == "__main__":
    main()
