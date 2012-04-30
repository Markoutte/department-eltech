import PyQt4.QtGui as ui
import PyQt4.QtCore as core
import department.database as database
import department.database.queries as query
from PyQt4.QtCore import QModelIndex

class PersonListView(ui.QListView):
    """
    A list view of persons in left panel. Every list looks like:
        ----------------------
        | Family N.M.        |
        ----------------------
        | AnotherFamily O.P. |
        ----------------------
    """
    def __init__(self, parent=None):
        super(PersonListView, self).__init__(parent)
        self.__model = ui.QStringListModel(None)
        self.setModel(self.__model)

        self.connect(self, core.SIGNAL('clicked(const QModelIndex&)'),
            self, core.SLOT('personClicked(const QModelIndex&)')
        )

    @core.pyqtSlot('const QString&')
    def update(self, begin):
        """
        update widget with list of persons from db,
        where representation of person starts with <i>begin</i>,
        i.e. if begin = 'Mc' all persons with family like
        McDon will be returned
        """
        if begin == '':
            self.__model.setStringList([])
        elif database.is_connected():
            response = query.get_persons_list(begin)
            if response is not None:
                self.__model.setStringList(response)
            else:
                self.__model.setStringList([])

    @core.pyqtSlot('const QModelIndex&')
    def personClicked(self, index):
        """
        retransmit signal with chosen id from widget with
        argument of fullname
        """
        self.emit(core.SIGNAL('personSelected(QString)'),
            query.get_person_by_id(index.row() + 1)[1])