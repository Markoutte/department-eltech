import sys
import logging as log
import department.database as database
from department.gui.mainwindow import MainWindow
from department.application import Application

def main():
    app = Application(sys.argv)

    # load configuration
    log.basicConfig(
        #filename='LOG',
        stream=sys.stdout,
        format='%(levelname)s(%(asctime)s): %(message)s', level=log.INFO
    )
    database.open(dbname='department_db')

    # load main window
    mw = MainWindow()
    mw.show()

    app.exec_()

if __name__ == "__main__":
    main()
