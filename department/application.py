import PyQt4.QtGui as ui
import PyQt4.QtCore as core
import department.database as database

class Application(ui.QApplication):

    def __init__(self, args):
        super(Application, self).__init__(args)
        core.QObject.connect(self, core.SIGNAL('aboutToQuit()'), self.close)

    def close(self):
        database.close()
