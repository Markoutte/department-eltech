import department.database as _db

def _to_str_list(ls):
    """
    get from list of tuple a string list,
    where values are first in tuple;
    i.e. [(1, 2), (3, 4)] → ["1", "3"]
    """
    if len(ls) > 0:
        values = []
        for item in filter(lambda l : len(l) > 0, ls):
            values.append(str(item[0]))
        return values

def get_persons_list_of_id(search_string):
    """
    returns list of employees' ids are started with <i>search_string</i>
    """
    pers_ls = ("(SELECT ID FROM GET_PERSONS(INITCAP('{str}')) ) AS PERS_LS"
                        .format(str = search_string))
    cursor = _db.execute("SELECT * FROM {};".format(pers_ls)
    ) # TODO fix bug with capitalizing names (from db?)
    return _to_str_list(cursor.fetchall())
     

def get_persons_list(id_list=''):
    """
    get list of persons, i.e. ["McDon Ann Ber", "Carlo San Kole"]
    if <i>id_list</i> is defined return list with names starts with it
    """
    pers_ls = ("(SELECT FORMAT('%s %s %s', "
                       "SURNAME, "
                       "NAME, "
                       "MIDDLE_NAME"
                       ") AS FULLNAME "
                       "FROM EMPLOYEE WHERE ID IN ({})"
                ")"
                        .format(', '.join(id_list)))
    cursor = _db.execute(pers_ls)
    return _to_str_list(cursor.fetchall())

def get_person_id(index):
    """
    get couple — id & fullname of person by his number in list
    """
    cursor = _db.execute("SELECT ID FROM GET_PERSONS('') WHERE ROW={id};"
                         .format(id = index))
    return cursor.fetchone()[0]

def get_full_info(person_id):
    """
    get whole information about employee in list by his id 
    """
    cols = 'ID, SURNAME, NAME, MIDDLE_NAME'
    cursor = _db.execute("SELECT {} FROM EMPLOYEE WHERE ID = {}".format(cols, person_id))
    return cursor.fetchall()

def get_positions_list():
    cursor = _db.execute("SELECT CODE, NAME FROM POSITION")
    return cursor.fetchall()

CATEGORY = 0;
PROFESSION = 1;

def get_strlist_of(choose):
    if choose == CATEGORY:
        cursor = _db.execute("SELECT DISTINCT prof_cat FROM EMPLOYEE")
    elif choose == PROFESSION:
        cursor = _db.execute("SELECT DISTINCT prof_name FROM EMPLOYEE")
    return _to_str_list(cursor.fetchall())
    