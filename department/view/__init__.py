from department.view import mainwindow, personnelschedule

TableEditor = personnelschedule.PersonnelSchedule.TableEditor
PositionManager = personnelschedule.PersonnelSchedule.PositionManager

def MainWindow(application, department, parent=None):
    return mainwindow.MainWindow(application, department, parent)

def PersonnelSchedule(application, department, parent=None):
    return  personnelschedule.PersonnelSchedule(application, department, parent)