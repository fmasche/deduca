import numpy as np
import re
from os import listdir, path
import constants
from sklearn.feature_extraction.text import CountVectorizer

TEST_QUERY_SELECT = "select employees.first_name, employees.last_name, employees.gender, employees.birth_date, employees.hire_date, salaries.salary from employees inner join salaries on employees.emp_no = salaries.emp_no where employees.emp_no = @param;"
TEST_QUERY_SELECT_ALL = "select * from salaries where salary > @param;"
TEST_DATA = {
    "role" : "HR",
    "user": "bob",
    "rows_examined": 4,
    "timestamp": "11-24-18 19:44:57",
    "text": TEST_QUERY_SELECT
}
TEST_QUERY_INSERT = "insert into departments values ();"
TEST_QUERY_UPDATE = "update billing set amount = @param where billing_no = @param;"
TEST_QUERY_UPDATE_WO_WHERE = "update billing set amount = @param;"
TEST_QUERY_DELETE = "delete from patient where patient_no = @param;"
TEST_QUERY_DELETE_WO_WHERE = "delete from billing;"

BOW = "select employees.emp_no from employees where employees.first_name like @param%; select employees.emp_no from employees where employees.last_name like @param%; select employees.first_name employees.last_name employees.gender employees.birth_date employees.hire_date salaries.salary from employees inner join salaries on employees.emp_no = salaries.emp_no where employees.emp_no = @param; select departments.dept_no departments.dept_name from departments; select employees.emp_no employees.first_name employees.last_name dept_emp.dept_no dept_emp.from_date dept_emp.to_date from employees inner join dept_emp on employees.emp_no = dept_emp.emp_no where employees.emp_no = @param; select employees.emp_no employees.first_name employees.last_name titles.title titles.from_date titles.to_date from employees inner join titles on employees.emp_no = titles.emp_no where employees.emp_no = @param; insert into departments values (); insert into employees values (); insert into salaries values (); insert into dept_emp values (); select * from employees; select * from employees where birth_date between  and ; select * from employees where hire_date between  and ; select * from employees where gender = @param; select * from salaries; select * from salaries where salary > @param; select * from salaries where salary < @param; select * from salaries where salary = @param; select * from dept_emp; delete from employees; delete from salaries; delete from dept_emp; select patient.patient_no patient.birth_date patient.first_name patient.last_name patient.gender patient.phone patient.address patient.insurance_id from patient where patient.last_name like @param; select patient.patient_no patient.birth_date patient.first_name patient.last_name patient.gender patient.phone patient.address patient.insurance_id from patient where patient.first_name like @param; select patient.patient_no patient.birth_date patient.first_name patient.last_name patient.gender patient.phone patient.address patient.insurance_id from patient where patient.patient_no = @param; select patient.patient_no patient.first_name patient.last_name patient.birth_date prescribes.prescription_no prescribes.physician_no prescribes.dose prescribes.med_code from patient inner join prescribes on patient.patient_no = prescribes.patient_no where patient.patient_no = @param; select medication.med_code medication.name medication.brand medication.description from medication where medication.name like %param; select medication.med_code medication.name medication.brand medication.description from medication where medication.brand like %param; select appointment.appointment_id appointment.patient_no patient.first_name patient.last_name patient.birth_date appointment.nurse_no appointment.physician_no appointment.start_dt_time appointment.end_dt_time from appointment inner join patient on appointment.patient_no = patient.patient_no where appointment.patient_no = @param; select appointment.appointment_id appointment.patient_no patient.first_name patient.last_name patient.birth_date appointment.nurse_no appointment.physician_no appointment.start_dt_time appointment.end_dt_time from appointment inner join patient on appointment.patient_no = patient.patient_no where appointment.physician_no = @param; select appointment.appointment_id appointment.patient_no patient.first_name patient.last_name patient.birth_date appointment.nurse_no appointment.physician_no appointment.start_dt_time appointment.end_dt_time from appointment inner join patient on appointment.patient_no = patient.patient_no where appointment.nurse_no = @param; select appointment.appointment_id appointment.patient_no patient.first_name patient.last_name patient.birth_date appointment.nurse_no appointment.physician_no appointment.start_dt_time appointment.end_dt_time from appointment inner join patient on appointment.patient_no = patient.patient_no where appointment.start_dt_time = @param; select appointment.appointment_id appointment.patient_no patient.first_name patient.last_name patient.birth_date appointment.nurse_no appointment.physician_no appointment.start_dt_time appointment.end_dt_time from appointment inner join patient p on appointment.patient_no = patient.patient_no where appointment.examination_room = @param; select procedures.proc_code procedures.description procedures.cost from procedures where procedures.proc_code = @param; select procedures.proc_code procedures.description procedures.cost from procedures where procedures.description like %@param; insert into prescribes values (); insert into patient values (); insert into medication values (); insert into appointment values (); delete from prescribes where prescription_no = @param; delete from medication where med_code = @param; delete from patient where patient_no = @param; delete from appointment where appointment_id = @param; select * from patient; select * from patient where birth_date = @param; select first_name last_name ssn phone address birth_date from patient; select first_name last_name ssn birth_date from patient; select * from prescribes; select * from medication; select * from appointment; delete from patient; delete from prescribes; delete from medication; delete from appointment; select billing.billing_no billing.payment_method billing.amount billing.cc_number patient.patient_no patient.first_name patient.last_name patient.gender patient.insurance_id patient.phone patient.address from billing inner join patient on billing.patient_no = patient.patient_no where patient.patient_no = @param; select appointment.appointment_id appointment.patient_no patient.first_name patient.last_name patient.birth_date appointment.nurse_no appointment.physician_no appointment.start_dt_time appointment.end_dt_time from appointment inner join patient on appointment.patient_no = patient.patient_no where appointment.patient_no = @param; select appointment.appointment_id appointment.patient_no patient.first_name patient.last_name patient.birth_date appointment.nurse_no appointment.physician_no appointment.start_dt_time appointment.end_dt_time from appointment inner join patient on appointment.patient_no = patient.patient_no where appointment.physician_no = @param; select appointment.appointment_id appointment.patient_no patient.first_name patient.last_name patient.birth_date appointment.nurse_no appointment.physician_no appointment.start_dt_time appointment.end_dt_time from appointment inner join patient on appointment.patient_no = patient.patient_no where appointment.nurse_no = @param; select appointment.appointment_id appointment.patient_no patient.first_name patient.last_name patient.birth_date appointment.nurse_no appointment.physician_no appointment.start_dt_time appointment.end_dt_time from appointment inner join patient on appointment.patient_no = patient.patient_no where appointment.start_dt_time = @param; select appointment.appointment_id appointment.patient_no patient.first_name patient.last_name patient.birth_date appointment.nurse_no appointment.physician_no appointment.start_dt_time appointment.end_dt_time from appointment inner join patient on appointment.patient_no = patient.patient_no where appointment.examination_room = @param; select procedures.proc_code procedures.description procedures.cost from procedures where procedures.proc_code = @param; select procedures.proc_code procedures.description procedures.cost from procedures where procedures.description like %@param; insert into billing values (); insert into appointment values (); insert into procedures values (); update billing set amount = @param where billing_no = @param; update billing set payment_method = @param cc_number = @param where billing_no = @param; update procedures set cost = @param where proc_code = @param; delete from billing where billing_no = @param; delete from billing where patient_no = @param; delete from procedures where proc_code = @param; select * from appointment; select * from billing; select * from billing where amount = @param; delete from billing; delete from appointment; delete from procedures; select employees.emp_no from employees where employees.first_name like @param%; select employees.emp_no from employees where employees.last_name like @param%; select departments.dept_no departments.dept_name from departments; select employees.emp_no employees.first_name employees.last_name dept_emp.dept_no dept_emp.from_date dept_emp.to_date from employees inner join dept_emp on employees.emp_no = dept_emp.emp_no where employees.emp_no = @param; select employees.emp_no employees.first_name employees.last_name titles.title titles.from_date titles.to_date from employees inner join titles on employees.emp_no = titles.emp_no where employees.emp_no = @param; select patient.patient_no patient.birth_date patient.first_name patient.last_name patient.gender patient.phone patient.address patient.insurance_id from patient where patient.last_name like @param; select patient.patient_no patient.birth_date patient.first_name patient.last_name patient.gender patient.phone patient.address patient.insurance_id from patient where patient.first_name like @param; select patient.patient_no patient.birth_date patient.first_name patient.last_name patient.gender patient.phone patient.address patient.insurance_id from patient where patient.patient_no = @param; select medication.med_code medication.name medication.brand medication.description from medication where medication.name like %param; select medication.med_code medication.name medication.brand medication.description from medication where medication.brand like %param;"

def getQueryParts(query):
    query = query.lower()
    command = ""                # The command being executed (SELECT, UPDATE, INSERT, DELETE)
    tablesAndColumns = set()    # The tables mentioned in the FROM clause with the columns returned from each table
    tablesAndAttributes = set() # The attributes referenced in the WHERE clause

    command = query.split(' ', 1)[0]    # get first word from query string
    # print("command: " + command)

    tablesAndColumns = getTablesAndColumns(command, query)
    tablesAndAttributes = getTablesAndAttributes(command, query)
    # print('Tables and columns: ', tablesAndColumns)
    # print('Attributes WHERE clause:', tablesAndAttributes)

    return command, tablesAndColumns, tablesAndAttributes

def getTablesAndColumns(command, query):

    # split on blanks, parens and semicolons
    tokens = re.split(r"[\s)(;]+", query)
    dictTables = dict()
    if (command in ["insert", "delete"]):
        if (command == "insert"): tokens.remove("into")
        if (command == "delete"): tokens.remove("from")
        # scan the tokens. if we see a FROM or JOIN, we set the get_next flag, and grab the next one (unless it's SELECT).
        table = ""
        get_next = False
        for tok in tokens:
            if get_next:
                if tok.lower() not in ["", "values"]:
                    table = tok
                get_next = False
            get_next = tok.lower() in ["insert", "delete"]
        
        # we don't have columns to look for when is an insert, and we are expecting to have only one table
        dictTables[table] = list(set())
    else:
        while "inner" in tokens: tokens.remove("inner")
        # scan the tokens. if we see a FROM or JOIN, we set the get_next flag, and grab the next one (unless it's SELECT).
        tables = set()
        get_next = False
        for tok in tokens:
            if get_next:
                if tok.lower() not in ["", "select", "set"]:
                    tables.add(tok)
                get_next = False
            get_next = tok.lower() in ["from", "join", "update"]

        if (command == "update"): 
            tokens.remove("update")
            tokens.remove("set")

        # get columns returned for each table        
        for table in tables:
            fields = []
            for token in tokens:
                if ((command == 'select' and token == 'from') or (command == 'update' and token == '=')):
                    # if we get to one of these tokens, depending on the command we can stop looping the tokens
                    break
                if ((token.startswith(table) or token == "*") or command in ["update"]):
                    if (token != table or token == "*"):
                        fields.append(token.replace(",", ""))
            if len(list(set(fields))) >= 1:
                dictTables[table] = list(set(fields))
    return dictTables

def getTablesAndAttributes(command, query):
    dictTables = dict()

    if (command == "insert"):   # we don't have where attributes with a insert statement
        return dictTables

    # split on blanks, parens and semicolons
    tokens = re.split(r"[\s)(;]+", query)

    while "inner" in tokens: tokens.remove("inner")

    # scan the tokens. if we see a FROM or JOIN, we set the get_next flag, and grab the next one (unless it's SELECT).
    tables = set()
    get_next = False
    for tok in tokens:
        if get_next:
            if tok.lower() not in ["", "select", "set"]:
                tables.add(tok)
            get_next = False
        get_next = tok.lower() in ["from", "join", "update"]

    # we only get the portion of string after the where statement
    if 'where' in tokens:
        query =  query.split(' where ', 1)[1]
        tokens = re.split(r"[\s)(;]+", query)
        for table in tables:
            fields = []
            for token in tokens:
                if (token.lower() in ["from"]): # if we get to the FROM statement we can stop looping the tokens
                    break
                if (token.startswith(table) or len(tables) == 1):    # if the attribute corresponds to the table or if there is only one table
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
    tables = [0] * 11
    for x, y in tablesDic.items():
        table = x
        index = constants.TABLES_INDEX[table]
        tables[index] = 1

    return np.array(tables)

def getFeaturesFromColumns(tablesDic):
    columns = np.zeros((11, 9))   ## 11 tables, 9 maximum amount of columns
    for x, y in tablesDic.items():
        table = x
        tableIdx = constants.TABLES_INDEX[table]
        if ("*" in y):      # get all the columns of the table
            size = constants.getTableSize(table)
            for idx in range(size):
                columns[tableIdx][idx] = 1
        else:
            for items in y:
                try:
                    columnName = items
                    if ("." in columnName):
                        columnName = items.split(".", 1)[1]
                    #print("table: ", table, " - columnName: ", columnName)
                    columnNameIdx = constants.getColumnIndex(table, columnName)
                    #print("tableIdx: ", tableIdx, " - columnNameIdx: ", columnNameIdx)
                    columns[tableIdx][columnNameIdx] = 1
                except Exception as error:
                    # only the tokens from the WHERE filter condition are going to come here, and it doesn't really matter,
                    # we don't need them (like, @param, >, <) The attribute being conditioned should not get here.
                    pass
                    #print('Exception error: ', error, ' - table: ', table)                    
    #print(columns)
    return columns


# data expected to be a dictionary with the format:
# {'role': 'HR', 'user': 'bob', 'rows_examined': 4, 'timestamp': '11-24-18 19:44:57', 'text': 'select * from patient'}
# add_BOW = boolean
def getFeaturesFromQuery(data, add_BOW=False):
    query = data.get("text")
    #query = "select employees.emp_no from employees where employees.first_name like @param%"
    rows_examined = data.get("rows_examined")

    command, tablesAndColumns, tablesAndAttributes = getQueryParts(query)

    arrayCommand = getFeaturesFromCommand(command)
    arrayTables = getFeaturesFromTables(tablesAndColumns)
    arrayColumns = getFeaturesFromColumns(tablesAndColumns)
    arrayAttributes = getFeaturesFromColumns(tablesAndAttributes)

    arrayColumns = arrayColumns.flatten()
    arrayAttributes = arrayAttributes.flatten()
    
    arrayBow = []
    if (add_BOW):
        vectorizer = CountVectorizer(stop_words=None, min_df=0) # ngram_range=(1, 2)
        bow_ = BOW.split("; ")        
        bow_ = np.array(bow_)
        x = vectorizer.fit_transform(bow_).toarray()
        #print(bow_)        
        param = []
        param.append(query)
        arrayBow = vectorizer.transform(param).toarray()[0]
        #print('arrayBow: ', arrayBow.shape)

    retval = np.concatenate([arrayCommand, arrayTables, arrayColumns, arrayAttributes, np.array([rows_examined]), np.array(arrayBow)])
    retval = retval.reshape(1, -1)  #only one sample here
    #print('retval ', retval.shape)
    return retval

# we exclude the features from the WHERE statemnt
def getFeaturesFromDBSAFE(data):
    query = data.get("text")
    rows_examined = data.get("rows_examined")

    command, tablesAndColumns, _ = getQueryParts(query)

    arrayCommand = getFeaturesFromCommand(command)
    arrayTables = getFeaturesFromTables(tablesAndColumns)
    arrayColumns = getFeaturesFromColumns(tablesAndColumns)

    arrayColumns = arrayColumns.flatten()
    
    retval = np.concatenate([arrayCommand, arrayTables, arrayColumns, np.array([rows_examined])])
    retval = retval.reshape(1, -1)  #only one sample here

    return retval    


if __name__ == "__main__":
    print('Holi - ', TEST_QUERY_SELECT_ALL)
    features = getFeaturesFromQuery(TEST_DATA, True)
    print('FINAL FEATURES: ')
    print(features)
    # result = getQueryParts(TEST_QUERY_SELECT_ALL)
    # print(result)