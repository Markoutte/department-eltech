import PySide.QtGui as ui
import PySide.QtCore as core
import PySide.QtUiTools as ui_loader

class Form(ui.QMainWindow):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        loader = ui_loader.QUiLoader(parent)
        self._ui = loader.load('gui/form.ui')        
        self.setCentralWidget(self._ui)
        self.setWindowTitle('Новая запись')
        
    @core.Slot('map')
    def load(self, data):
        self._ui.secondname_le.setText(data['secondname'])
        self._ui.firstname_le.setText(data['firstname'])
        self._ui.middlename_le.setText(data['middlename'])
        self.show()