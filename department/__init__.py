from department.application import Application
import sys

def main():
    app = Application(sys.argv)
    app.exec_()

if __name__ == '__main__':
    main()