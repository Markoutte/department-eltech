def to_str_list(column):
    if (len(column) > 0):
        values = []
        f = lambda l : len(l) > 1
        for t in filter(f, column):
            values.append(str(t[1]))
        return values

def gen_select(table, *args):
    """Generate String for query of selecting columns *args in table"""
    values = list(args)
    for i in range(0, len(args) - 1):
        values.insert(2 * i + 1, ", ")
    return "SELECT {} FROM {}".format("".join(values), table)

def gen_select_all(table):
    """Generate String for query of selecting all rows from table"""
    return "SELECT * FROM {}".format(table)