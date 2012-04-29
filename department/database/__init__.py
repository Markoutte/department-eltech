import psycopg2 as database

def execute(query):
    cursor = Connection()._get_cursor()
    try:
        cursor.execute(query)
    except database.ProgrammingError as e:
        print('Cannot execute, because of ', e)
    return cursor

def open(**kwargs):
    con = None
    try:
        con = database.connect(
            "dbname='{dbname}' user='{user}' host='{host}' password='{password}' port='{port}'"
            .format(
                dbname = kwargs.get('dbname', 'default'),
                user = kwargs.get('user', 'postgres'),
                host = kwargs.get('host', 'localhost'),
                password = kwargs.get('password', 'postgres'),
                port = kwargs.get('port', '5432')
            )
        )
    except database.Error as e:
        print('Cannot connect, ', e)
        return False

    Connection().set(con)
    print('Connection established')
    return True

def is_connected():
    return Connection().get() is not None

def close():
    if not is_connected():
        return
    Connection().get().close()
    Connection()._clear()
    print('Connection closed')

class Connection:
    __con = None
    def get(self):
        return self.__con
    def set(self, connection):
        self.__con = connection

    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Connection, cls).__new__(cls, *args, **kwargs)
        return  cls._instance

    __cursor = None
    def _get_cursor(self):
        if self.__cursor is None:
            self.__cursor = self.__con.cursor()
        return self.__cursor

    def _clear(self):
        self.__con = None
        self.__cursor = None
