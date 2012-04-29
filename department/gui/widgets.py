import PyQt4.QtGui as ui
import PyQt4.QtCore as core
import department.database as database
import department.database.queries as query
from PyQt4.QtCore import QModelIndex

class PersonListView(ui.QListView):
    def __init__(self, parent=None):
        super(PersonListView, self).__init__(parent)
        self.__model = ui.QStringListModel(None)
        self.setModel(self.__model)

        # load data from db
        self.update()

        self.connect(self, core.SIGNAL('clicked(const QModelIndex&)'),
            self, core.SLOT('personClicked(const QModelIndex&)')
        )

    def update(self):
        if database.is_connected():
            self.__model.setStringList(query.get_persons_list())

    @core.pyqtSlot('const QModelIndex&')
    def personClicked(self, index):
        self.emit(core.SIGNAL('personSelected(QString)'),
            query.get_person_by_id(index.row() + 1)[1])



