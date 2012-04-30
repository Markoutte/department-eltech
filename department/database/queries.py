import department.database as _db

def _to_str_list(list):
    """
        get from list of tuple a string list,
        where values are first in tuple;
        i.e. [(1, 2), (3, 4)] → ["1", "3"]
    """
    if len(list) > 0:
        values = []
        for tuple in filter(lambda l : len(l) > 0, list):
            values.append(str(tuple[0]))
        return values

def get_persons_list(cut=''):
    """
    get list of persons, i.e. ["McDon A.B.", "Carlo S.B."]
    if <i>cut</i> is defined return list with names starts with it
    """
    pers_ls = "(SELECT FORMAT('%s %s.%s.', " \
                       "SURNAME, " \
                       "SUBSTRING(NAME FROM '^.'), " \
                       "SUBSTRING(MIDDLE_NAME FROM '^.')" \
                       ") AS FULLNAME " \
                       "FROM PERSONS('{str}') ) AS PERS_LS" \
                        .format(str = str.capitalize(cut))
    cursor = _db.execute("SELECT * FROM {};".format(pers_ls)
    ) # TODO fix bug with capitalizing names (from db?)
    return _to_str_list(cursor.fetchall())

def get_person_by_id(person_id):
    """
    get couple — id & fullname of person by his number in list
    """
    cursor = _db.execute("SELECT ID, FORMAT('%s %s %s ', " \
                            "SURNAME, NAME, MIDDLE_NAME" \
                          ") FROM PERSONS('') WHERE ROW={id};"
                         .format(id = person_id))
    return cursor.fetchone()