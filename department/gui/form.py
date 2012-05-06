import PySide.QtGui as ui
import PySide.QtCore as core
import PySide.QtUiTools as ui_loader
import department.database.queries as _query

class Form(ui.QMainWindow):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        loader = ui_loader.QUiLoader(parent)
        self._ui = loader.load('gui/form.ui')        
        self.setCentralWidget(self._ui)
        self.setWindowTitle('Новая запись')
        
        self._sex = ui.QButtonGroup()
        self._sex.addButton(self._ui.male_rb)
        self._sex.addButton(self._ui.female_rb)
        
        # load list of positions
        for code, name in _query.get_positions_list():
            self._ui.position_cmb.addItem(name)
            
        # load completer of category and profession
        cat = ui.QCompleter(_query.get_strlist_of(_query.CATEGORY), self)
        cat.setCaseSensitivity(core.Qt.CaseInsensitive)
        self._ui.cat_le.setCompleter(cat)
        prof = ui.QCompleter(_query.get_strlist_of(_query.PROFESSION), self)
        prof.setCaseSensitivity(core.Qt.CaseInsensitive)
        self._ui.prof_le.setCompleter(prof)
        
    @core.Slot('map')
    def load(self, data):
        self._ui.secondname_le.setText(data['secondname'])
        self._ui.firstname_le.setText(data['firstname'])
        self._ui.middlename_le.setText(data['middlename'])
        self.show()
        