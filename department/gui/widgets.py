import PySide.QtGui as ui
import PySide.QtCore as core
import department.database as database
import department.database.queries as query
import department.gui.form as _formview

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
        
        core.QObject.connect(self, core.SIGNAL('doubleClicked(const QModelIndex &)'),
                             self, core.SLOT('show_full_info(const QModelIndex &)'))

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

    def contextMenuEvent(self, event):
        menu = ui.QMenu()
        if self.selectedIndexes() != []:
            menu.addAction('Редактировать', self, core.SLOT('edit_record()'))
            menu.addAction('Подробней', self, core.SLOT('show_full_info()'))      
        menu.exec_(event.globalPos())
        
    @core.Slot()
    def add_record(self):
        self._form = _formview.Form(self.parent())
        self._form.show()
        
    @core.Slot()
    def edit_record(self):
        self._form = _formview.Form(self.parent())
        selected= self.selectedIndexes()[0].row()
        response = query.get_full_info(self.__ids[selected])
        self._form.load(response)
        self._form.show()
        
    @core.Slot()
    @core.Slot('const QModelIndex &')
    def show_full_info(self, index=None):
        if index is None:
            index = self.selectedIndexes()[0]
        print(query.get_full_info(self.__ids[index.row()]))
        
        