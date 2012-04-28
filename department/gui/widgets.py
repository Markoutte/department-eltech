from PyQt4.QtGui import QStringListModel
from PyQt4.QtGui import QListView
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QModelIndex
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from department.database import *
from department.utils import *

class PersonListView(QListView):
    def __init__(self, parent=None):
        super(PersonListView, self).__init__(parent)
        self.__model = QStringListModel(None)
        self.setModel(self.__model)

        # load data from db
        self.loadPersons()

        self.connect(self, SIGNAL('clicked(const QModelIndex&)'),
            self, SLOT('personClicked(const QModelIndex&)')
        )


    def loadPersons(self):
        con = Connection()
        if is_connected(con):
            self.__persons = con.exec(
                "SELECT id, format('%s %s %s', surname, name, middle_name)  AS fullname FROM employee "
            )
            if self.__persons != None:
                self.__model.setStringList(to_str_list(self.__persons))

    @pyqtSlot('const QModelIndex&')
    def personClicked(self, index):
        self.emit(SIGNAL('personSelected(int)'),
            self.__persons[index.row()][0])


class Information(QWidget):
    def __init__(self, parent=None):
        super(Information, self).__init__(parent)
        grid = QGridLayout()
        self.setLayout(grid)

        # init all fields
        self.__id_lbl = QLabel(None)
        self.__full_name_lbl = QLabel(None)

        # set fields into grid
        grid.addWidget(self.__id_lbl, 0, 0)
        grid.addWidget(self.__full_name_lbl, 0, 1)

    def updateEvent(self):
        self.updateInfo(1)

    @pyqtSlot('int')
    def updateInfo(self, index):
        response = Connection().exec(
            "SELECT id, surname, name, middle_name, sex, address, contract_id "
            "FROM employee WHERE id = {}"
                .format(index)
        )
        if response == None or len(response) == 0:
            return

        person = {
            'id' : response[0][0],
            'surname' : response[0][1],
            'name' : response[0][2],
            'middle' : response[0][3],
            'sex' : response[0][4]
        }

        self.__id_lbl.setText('Табельный номер: {}'.format(str(person['id'])))
        fullname = "<b>{surname} {name} {middle}</b>".format(
            surname = person['surname'],
            name = person['name'],
            middle = person['middle']
        )
        self.__full_name_lbl.setText(fullname)



