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
        
        # set sex & marital
        self._sex = ui.QButtonGroup()
        self._sex.addButton(self._ui.male_rb, 1)
        self._sex.addButton(self._ui.female_rb, 2)
        self._ui.marital_cmb.addItems(['Холост', 'Женат', 'Разведён'])
        
        # load list of positions
        for code, name in _query.get_positions_list():
            self._ui.position.addItem(name)
            
        # set current date
        self._ui.sign_date_edit.setDate(core.QDate.currentDate())
        self.set_exp_date(self._ui.add_exp_date.currentText())
            
        # load completer of category and profession
        cat = ui.QCompleter(_query.get_strlist_of(_query.CATEGORY), self)
        cat.setCaseSensitivity(core.Qt.CaseInsensitive)
        self._ui.cat_le.setCompleter(cat)
        prof = ui.QCompleter(_query.get_strlist_of(_query.PROFESSION), self)
        prof.setCaseSensitivity(core.Qt.CaseInsensitive)
        self._ui.prof_le.setCompleter(prof)
        
        # buttons
        self._ui.save_btn.setVisible(False)
        
        # connections        
        core.QObject.connect(self._sex, core.SIGNAL('buttonClicked (int)'),
                             self, core.SLOT('sexChanged(int)'))
        core.QObject.connect(self._ui.add_exp_date, core.SIGNAL('currentIndexChanged(const QString &)'),
                             self, core.SLOT('set_exp_date(const QString &)'))
        core.QObject.connect(self._ui.add_position_btn, core.SIGNAL('clicked()'),
                             self, core.SLOT('add_position()'))
        core.QObject.connect(self._ui.remove_position_btn, core.SIGNAL('clicked()'),
                             self, core.SLOT('remove_position()'))
        core.QObject.connect(self._ui.cancel_btn, core.SIGNAL('clicked()'),
                             self, core.SLOT('close()'))
        
    @core.Slot('map')
    def load(self, data):
        gui = self._ui
        gui.secondname_le.setText(data['surname'])
        gui.firstname_le.setText(data['name'])
        gui.middlename_le.setText(data['middlename'])
        gui.birth_date_edit.setDate(core.QDate.fromString(data['birth_date'], 'yyyy.M.d'))
        if data['sex'] == 'm':
            gui.male_rb.setChecked(True)
        elif data['sex'] == 'f':
            gui.female_rb.setChecked(True)
            self.sexChanged(2)
        gui.diploma_cmb.setEditText(data['diploma'])
        gui.marital_cmb.setCurrentIndex(int(data['marital']))
        gui.expa_date_edit.setDate(core.QDate.fromString(data['experience'], 'yyyy.M.d'))
        gui.address_te.setPlainText(data['address'])
        gui.phone_le.setText(data['phone'])
        gui.cat_le.setText(data['category'])
        gui.prof_le.setText(data['profession'])        
        # complete table
        for i, part in enumerate(data['part']):
            gui.position_table.insertRow(i)
            print(part)
            gui.position_table.setItem(i, 0, ui.QTableWidgetItem(str(part)))
            gui.position_table.setItem(i, 1, ui.QTableWidgetItem(data['position'][i]))
        passport = data['passport'].split(' ', 1) # split to serial (4000) and number (XXXXXX)
        gui.ser_pass_le.setText(passport[0])
        gui.no_pass_le.setText(passport[1])
        gui.contract_id.setText(str(data['contract']))
        gui.sign_date_edit.setDate(core.QDate.fromString(data['accept'], 'yyyy.M.d'))
        gui.exp_date_edit.setDate(core.QDate.fromString(data['expires'], 'yyyy.M.d'))
            
        self._ui.ok_btn.setVisible(False)
        self._ui.save_btn.setVisible(True)
        
        self.show()
        
    @core.Slot('int')
    def sexChanged(self, checked_id):
        current_index = self._ui.marital_cmb.currentIndex()
        self._ui.marital_cmb.clear()
        if checked_id == 1:
            self._ui.marital_cmb.addItems(['Холост', 'Женат', 'Разведён'])
        elif checked_id == 2:
            self._ui.marital_cmb.addItems(['Не замужем', 'Замужем', 'Разведёна'])
        self._ui.marital_cmb.setCurrentIndex(current_index)
        
    @core.Slot('const QString &')
    def set_exp_date(self, string):
        date = self._ui.sign_date_edit.date()
        date = date.addMonths(12 * float(string))
        self._ui.exp_date_edit.setDate(date)
        
    @core.Slot()
    def add_position(self):
        table = self._ui.position_table
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 1, ui.QTableWidgetItem(self._ui.position.currentText()))
        table.setItem(row, 0, ui.QTableWidgetItem(self._ui.part_cmb.currentText()))
    
    @core.Slot()    
    def remove_position(self):
        table = self._ui.position_table
        row = table.currentRow()
        table.removeRow(row)