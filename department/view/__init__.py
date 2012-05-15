from department.view import mainwindow, personnelschedule

def MainWindow(application, department, parent=None):
    return mainwindow.MainWindow(application, department, parent)

def PersonnelSchedule(application, department, parent=None):
    return  personnelschedule.PersonnelSchedule(application, department, parent)

def PersonnelTable(department, parent=None):
    return  personnelschedule.PersonnelTable(department, parent)