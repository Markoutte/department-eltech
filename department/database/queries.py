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
    pers_ls = ("SELECT ID FROM GET_PERSONS(INITCAP('{str}'))"
                        .format(str = search_string))
    cursor = _db.execute(pers_ls)
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

def get_full_info(person_id):
    """
    get whole information about employee in list by his id in map
    """
    cursor = _db.execute("SELECT * FROM v_fullinfo WHERE id = {}".format(person_id))
    response = cursor.fetchall()
    info_map = {}
    info_map['part'] = []
    info_map['parts'] = []
    info_map['parts_busy'] = []
    info_map['employees'] = []
    info_map['salary'] = []
    info_map['position'] = []
    info_map['rank'] = []
    for (surname, name, middlename, sex, diploma,
         marital, experience, birth_date, passport,
         address, phone, category, profession,
         part, parts, parts_busy, employees, salary,
         position, rank, contract_type, accept, expires, contract, idx) in response:
        info_map['surname'] = surname
        info_map['name'] = name
        info_map['middlename'] = middlename
        info_map['sex'] = sex
        info_map['diploma'] = diploma
        info_map['marital'] = marital
        info_map['experience'] = experience
        info_map['birth_date'] = birth_date
        info_map['passport'] = passport
        info_map['address'] = address
        info_map['phone'] = phone
        info_map['category'] = category
        info_map['profession'] = profession
        info_map['part'].append(part)
        info_map['parts'].append(parts)
        info_map['parts_busy'].append(parts_busy)
        info_map['employees'].append(employees)
        info_map['salary'].append(salary)
        info_map['position'].append(position)
        info_map['rank'].append(rank)
        info_map['contract_type'] = contract_type
        info_map['accept'] = accept
        info_map['expires'] = expires
        info_map['contract'] = contract
        info_map['id'] = idx
    return info_map

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
    