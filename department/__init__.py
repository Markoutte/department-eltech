import sys
import department.database as database
from department.gui.mainwindow import MainWindow
from department.application import Application

def main():
    app = Application(sys.argv)

    # load configuration
    database.open(dbname='department_db')

    # load main window
    mw = MainWindow()
    mw.show()

    app.exec_()

if __name__ == "__main__":
    main()
