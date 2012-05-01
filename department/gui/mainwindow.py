
""" MainWindow contains general window which is entry point for user
"""
import PySide.QtGui as ui
import PySide.QtCore as core
from PyQt4 import uic
from department.gui.widgets import PersonListView

from PySide.QtUiTools import QUiLoader

class MainWindow(ui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        loader = QUiLoader(parent)
        self._ui = loader.load("gui/mainwindow.ui")
        self._ui.central_layout.setStretch(0, 1)
        self._ui.central_layout.setStretch(1, 3)
        self.setCentralWidget(self._ui)

        # load person list view
        self.persons_ls = PersonListView()
        self._ui.left_panel.insertWidget(1, self.persons_ls)

        # set connection

        core.QObject.connect(self._ui.search_bx, core.SIGNAL('textChanged (const QString&)'),
            self.persons_ls, core.SLOT('update(const QString&)'))
        core.QObject.connect(self._ui.add_new_person_btn, core.SIGNAL('clicked()'), self, core.SIGNAL('addNewPerson()'))
        core.QObject.connect(self.persons_ls, core.SIGNAL('personSelected(const QString&)'),
            self, core.SLOT('set_full_name(const QString&)'))

        self.setWindowTitle("Кадровый учёт")

    @core.Slot('const QString&')
    def set_full_name(self, fullname):
        '''This slot sets full name into label when signal arrives'''
        self._ui.fullname_lbl.setText('<font size=18>{}</font>'.format(fullname))