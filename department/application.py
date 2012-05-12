import psycopg2
import department.sql as sql
import department.view as view
import PySide.QtCore as core
import PySide.QtGui as gui

class Application(gui.QApplication):
    
    def __init__(self, argv):
        super(Application, self).__init__(argv)        
        self.conn = psycopg2.connect(dbname='department', user='postgres', password='postgres')
        self.department = sql.Department(self.conn)
        
        self.mw = view.MainWindow(self.department)
        self.mw.set_employees_list(self.department.get_employees_list())  
        self.mw.show()
        
        ## connections
        self.connect(self.department, core.SIGNAL('dataChanged(bool)'), self, core.SLOT('acceptChanges(bool)'))
        
    @core.Slot('bool')
    def acceptChanges(self, ok):
        if ok:
            self.conn.commit()
        else:
            self.conn.rollback()