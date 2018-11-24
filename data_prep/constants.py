TABLES_INDEX = {
    "appointment" : 0,
    "billing": 1,
    "departments": 2,
    "dept_emp": 3,
    "employees": 4,
    "medication": 5,
    "patient": 6,
    "prescribes": 7,
    "procedures": 8,
    "salaries": 9,
    "titles": 10
}

APPOINTMENT_IDX = {
    "appointment_id": 0,
    "patient_no": 1,
    "nurse_no": 2,
    "physician_no": 3,
    "start_dt_time": 4,
    "end_dt_time": 5,
    "examination_room": 6
}

BILLING_IDX = {
    "billing_no": 0,
	"patient_no": 1,
	"payment_method": 2,
	"amount": 3,
	"cc_number": 4
}

DEPARTMENTS_IDX = {
    "dept_no": 0,
    "dept_name": 1
}

DEPT_EMP_IDX = {
    "emp_no": 0,
    "dept_no": 1,
    "from_date": 2,
    "to_date": 3
}

EMPLOYEES_IDX = {
    "emp_no": 0,
    "birth_date": 1,
    "first_name": 2,
    "last_name": 3,
    "gender": 4,
    "hire_date": 5
}

MEDICATION_IDX = {
    "med_code": 0,
    "name": 1,
	"brand": 2,
	"description": 3
}

PATIENT_IDX = {
    "patient_no": 0,
    "birth_date": 1,
    "first_name": 2,
    "last_name": 3,
    "gender": 4,
    "ssn": 5,
	"phone": 6,
	"address": 7,
	"insurance_id": 8
}

PRESCRIBES_IDX = {
    "prescription_no": 0,
    "physician_no": 1,
    "patient_no": 2,
	"date": 3,
	"appointment_id": 4,
	"dose": 5,
	"med_code": 6
}

PROCEDURES_IDX = {
    "proc_code": 0,
    "description": 1,
	"cost": 2
}

SALARIES_IDX = {
    "emp_no": 0,
    "salary": 1,
    "from_date": 2,
    "to_date": 3
}

TITLES_IDX = {
    "emp_no": 0,
    "title": 1,
    "from_date": 2,
    "to_date": 3
}

def getColumnIndex(tableName, columnName):
    tableName = tableName.upper()
    if (tableName == "APPOINTMENT"):
        return APPOINTMENT_IDX[columnName]
    if (tableName == "BILLING"):
        return BILLING_IDX[columnName]
    if (tableName == "DEPARTMENTS"):
        return DEPARTMENTS_IDX[columnName]
    if (tableName == "DEPT_EMP"):
        return DEPT_EMP_IDX[columnName]
    if (tableName == "EMPLOYEES"):
        return EMPLOYEES_IDX[columnName]
    if (tableName == "MEDICATION"):
        return MEDICATION_IDX[columnName]
    if (tableName == "PATIENT"):
        return PATIENT_IDX[columnName]
    if (tableName == "PRESCRIBES"):
        return PRESCRIBES_IDX[columnName]
    if (tableName == "PROCEDURES"):
        return PROCEDURES_IDX[columnName]
    if (tableName == "SALARIES"):
        return SALARIES_IDX[columnName]
    if (tableName == "TITLES"):
        return TITLES_IDX[columnName]
    else:
        print("Wrong tableName: ", tableName, " - columnName: ", columnName)