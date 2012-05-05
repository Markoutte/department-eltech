import PySide.QtGui as ui
import PySide.QtCore as core
import department.database as database
import department.database.queries as query
import department.gui.form as _form

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
        self.setSelectionMode(self.SingleSelection)
        self.setEditTriggers(self.NoEditTriggers)

        self.connect(self, core.SIGNAL('clicked(const QModelIndex&)'),
            self, core.SLOT('personClicked(const QModelIndex&)')
        )
        
        self._form = _form.Form(self.parent())

    @core.Slot('const QString&')
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
            self.__ids = query.get_persons_list_of_id(begin)
            if self.__ids is not None:
                response = query.get_persons_list(self.__ids)
                self.__model.setStringList(response)
            else:
                self.__model.setStringList([])

    @core.Slot('const QModelIndex&')
    def personClicked(self, index):
        """
        retransmit signal with chosen id from widget with
        argument of fullname
        """
        self.emit(core.SIGNAL('personSelected(int)'),
            query.get_person_id(self.__ids[index.row()]))
        
    def contextMenuEvent(self, event):
        menu = ui.QMenu()
        menu.addAction('Добавить запись', self._form, core.SLOT('show()'))
        if self.selectedIndexes() != []:
            menu.addAction('Редактировать', self, core.SLOT('edit_record()'))            
        menu.exec_(event.globalPos())
        
    @core.Slot()
    def edit_record(self):
        response = query.get_full_info(query.get_person_id((self.selectedIndexes()[0].row() + 1)))[0]
        data = {}
        data['secondname'] = response[1]
        data['firstname'] = response[2]
        data['middlename'] = response[3]
        self._form.load(data)
    
        
        