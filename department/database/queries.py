import department.database as _db

def _to_str_list(list):
    '''
        get from list of tuple a string list,
        where values are first in tuple;
        i.e. [(1, 2), (3, 4)] → ["1", "3"]
    '''
    if len(list) > 0:
        values = []
        for tuple in filter(lambda l : len(l) > 0, list):
            values.append(str(tuple[0]))
        return values

def get_persons_list():
    cursor = _db.execute("SELECT FORMAT('%s %s.%s.', " \
                            "SURNAME, " \
                            "SUBSTRING(NAME FROM '^.'), " \
                            "SUBSTRING(MIDDLE_NAME FROM '^.')" \
                          ") FROM PERSONS;")
    return _to_str_list(cursor.fetchall())

def get_person_by_id(person_id):
    cursor = _db.execute('ALTER SEQUENCE PERSONS_SEQ RESTART WITH 1;')
    cursor = _db.execute("SELECT ID, FORMAT('%s %s %s ', " \
                            "SURNAME, NAME, MIDDLE_NAME" \
                          ") FROM PERSONS WHERE ROW={id};"
                         .format(id = person_id))
    return cursor.fetchone()