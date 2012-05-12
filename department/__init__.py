import sys
from department.application import Application

def main():
    app = Application(sys.argv)
    app.exec_()

if __name__ == '__main__':
    main()