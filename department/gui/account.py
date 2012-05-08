import PySide.QtGui as gui
import PySide.QtCore as core
import PySide.QtUiTools as ui_loader

class Account(gui.QMainWindow):
    def __init__(self, data, parent=None):
        super(Account, self).__init__(parent)
        loader = ui_loader.QUiLoader(parent)
        ui = loader.load('gui/account.ui')
        ui.fullname.setText('<b>{} {} {}</b>'.format(data['surname'], data['name'], data['middlename']))
        ui.birthday.setText(data['birth_date'])
        ui.passport.setText(data['passport'])
        ui.phone.setText(data['phone'])
        ui.address.setText(data['address'])
        ui.diploma.setText(data['diploma'])
        ui.category.setText(data['category'])
        ui.profession.setText(data['profession'])
        salary = 0
        for i, part in enumerate(data['part']):
            if part is None:
                break
            ui.positions.insertRow(i)
            ui.positions.setItem(i, 0, gui.QTableWidgetItem(str(part)))
            ui.positions.setItem(i, 1, gui.QTableWidgetItem(data['position'][i]))
            ui.positions.setItem(i, 2, gui.QTableWidgetItem(str(data['salary'][i])))
            salary += part * data['salary'][i]
        ui.salary.setText(str(salary))
        ui.contract.setText('Контракт № {} от {} по {}'.format(data['contract'], data['accept'], data['expires']))
        
        core.QObject.connect(ui.close_btn, core.SIGNAL('clicked()'), self, core.SLOT('close()'))
        self.setWindowTitle('{} {} {}'.format(data['surname'], data['name'], data['middlename']))
        self.setCentralWidget(ui)