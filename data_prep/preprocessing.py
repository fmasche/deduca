import numpy as np
import re
from os import listdir, path
import constants

TEST_QUERY = "select employees.first_name, employees.last_name, employees.gender, employees.birth_date, employees.hire_date, salaries.salary from employees inner join salaries on employees.emp_no = salaries.emp_no where employees.emp_no = @param;"
TEST_QUERY_ALL = "select * from employees;"

def getFeaturesFromQuery(query):
    command = ""                # The command being executed (SELECT, UPDATE, INSERT, DELETE)
    tablesAndColumns = set()    # The tables mentioned in the FROM clause with the columns returned from each table
    tablesAndAttributes = set() # The attributes referenced in the WHERE clause

    command = query.split(' ', 1)[0]    # get first word from query string
    print("command: " + command)

    if (command.upper() == "SELECT"):
        tablesAndColumns = getTablesAndColumns(query)
        tablesAndAttributes = getTablesAndAttributes(query)
        print(tablesAndColumns)
        print(tablesAndAttributes)

    return command, tablesAndColumns, tablesAndAttributes

def getTablesAndColumns(query):

    # split on blanks, parens and semicolons
    tokens = re.split(r"[\s)(;]+", query)

    while "inner" in tokens: tokens.remove("inner")

    # scan the tokens. if we see a FROM or JOIN, we set the get_next flag, and grab the next one (unless it's SELECT).
    tables = set()
    get_next = False
    for tok in tokens:
        if get_next:
            if tok.lower() not in ["", "select"]:
                tables.add(tok)
            get_next = False
        get_next = tok.lower() in ["from", "join"]

    # get columns returned for each table
    dictTables = dict()
    for table in tables:
        fields = []
        for token in tokens:
            if (token.lower() in ["from"]): # if we get to the FROM statement we can stop looping the tokens
                break
            if token.startswith(table):
                if token != table:
                    fields.append(token.replace(",", ""))
        if len(list(set(fields))) >= 1:
            dictTables[table] = list(set(fields))
    return dictTables

def getTablesAndAttributes(query):

    # split on blanks, parens and semicolons
    tokens = re.split(r"[\s)(;]+", query)

    while "inner" in tokens: tokens.remove("inner")

    # scan the tokens. if we see a FROM or JOIN, we set the get_next flag, and grab the next one (unless it's SELECT).
    tables = set()
    get_next = False
    for tok in tokens:
        if get_next:
            if tok.lower() not in ["", "select"]:
                tables.add(tok)
            get_next = False
        get_next = tok.lower() in ["from", "join"]

    dictTables = dict()
    # we only get the portion of string after the where statement
    if 'where' in tokens:
        query =  query.split(' where ', 1)[1]
        tokens = re.split(r"[\s)(;]+", query)
        
        for table in tables:
            fields = []
            for token in tokens:
                if token.startswith(table):
                    if token != table:
                        fields.append(token)
            if len(list(set(fields))) >= 1:
                dictTables[table] = list(set(fields))
    return dictTables

def getFeaturesFromCommand(command):
    command = command.lower()
    if (command == "select"):
        return np.array([1, 0, 0, 0])
    if (command == "update"):
        return np.array([0, 1, 0, 0])
    if (command == "insert"):
        return np.array([0, 0, 1, 0])
    else: # should be always "delete"
        return np.array([0, 0, 0, 1])

def getFeaturesFromTables(tablesDic):
    tables = [0] * 10
    #print('Inside getFeaturesFromTables: ')
    for x, y in tablesDic.items():
        table = x
        #print(table)
        index = constants.TABLES_INDEX[table]
        #print(index)
        tables.insert(index, 1)

    return np.array(tables)

def getFeaturesFromColumns(tablesDic):
    columns = np.zeros((11, 8))   ## 11 tables, 8 maximum amount of columns
    #print('Inside getFeaturesFromColumns: ')
    for x, y in tablesDic.items():
        table = x
        tableIdx = constants.TABLES_INDEX[table]

        for items in y:
            columnName = items.split(".", 1)[1]
            #print("table: ", table, " - columnName: ", columnName)
            columnNameIdx = constants.getColumnIndex(table, columnName)
            #print("tableIdx: ", tableIdx, " - columnNameIdx: ", columnNameIdx)
            columns[tableIdx][columnNameIdx] = 1

    #print(columns)
    return columns


def getFeaturesCombined(query):
    command, tablesAndColumns, tablesAndAttributes = getFeaturesFromQuery(query)

    if (command in ["insert", "update", "delete"]): # TODO for now I'm ignoring everything that is not select
        raise Exception('Commands not implemented!')

    arrayCommand = getFeaturesFromCommand(command)
    arrayTables = getFeaturesFromTables(tablesAndColumns)
    arrayColumns = getFeaturesFromColumns(tablesAndColumns)
    arrayAttributes = getFeaturesFromColumns(tablesAndAttributes)

    arrayColumns = arrayColumns.flatten()
    arrayAttributes = arrayAttributes.flatten()
    
    #print(arrayCommand)
    #print(arrayTables)
    return np.concatenate([arrayCommand, arrayTables, arrayColumns, arrayAttributes])


if __name__ == "__main__":
    print('Holi')
    #command, tablesAndColumns, tablesAndAttributes = getFeaturesFromQuery(TEST_QUERY)
    features = getFeaturesCombined(TEST_QUERY)
    print('FINAL FEATURES: ')
    print(features)
    #result = getTablesAndColumns(TEST_QUERY)
    #print(result)