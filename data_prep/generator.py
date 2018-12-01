from os import listdir, path
import numpy as np
import pandas as pd
import preprocessing
import random

DEFAULT_FILENAME = "files/training_data_1.xlsx"
VALID_ROLES = ['DOC', 'HR', 'ADM']

APPOINTMENT_MAX = 1000
BILLING_MAX = 1193
EMPLOYEES_MAX = 300024
SALARIES_MAX = 2844047
DEPT_EMP = 331603
PATIENT_MAX = 1192
PRESCRIBES_MAX = 1192
MEDICATION_MAX = 1095
PROCEDURES_MAX = 14
TITLES_MAX = 443308


def load_data(filename):
    originalFile = dict()

    sheet1 = pd.read_excel(open(filename,'rb'), sheet_name=1)
    for i in sheet1.index:
        if (sheet1['query'][i] == "query"):  # only to ignore the first line, TODO should change this
            continue
        originalFile[sheet1['query'][i]] = sheet1['rows'][i]     
        

    f = open("demofile.txt", "w")
    sheet0 = pd.read_excel(open(filename,'rb'), sheet_name=0)
    for i in sheet0.index:
        row = originalFile[sheet0['query'][i]]
        #print(row)
        f.write(str(row) + "\n")

    print(originalFile)     

def generate_data(original_queries_filename):
    originalHR = list()
    originalDoc = list()
    originalAdm = list()
    originalPent = list()   # the key is the query, the value is the original role

    totalSamples = 12000
    maliciousSamples = (5*totalSamples) / 100       # 5% of our samples are maliciuos
    trueSamples = totalSamples - maliciousSamples
    columns = ['query', 'role1', 'valid', 'role2', 'rows']

    sheet1 = pd.read_excel(open(original_queries_filename,'rb'), sheet_name=1)  # 'Original' tab
    for i in sheet1.index:
        query = sheet1['query'][i]
        if (query == "query"):  # only to ignore the first line, TODO should change this
            continue
        role1 = sheet1['role1'][i]
        valid = sheet1['valid'][i]
        role2 = sheet1['role2'][i]
        rows = sheet1['rows'][i]

        if (valid == 'Y'):
            if (role2 == 'HR'):
                originalHR.append(query)
            elif (role2 == 'DOC'):
                originalDoc.append(query)
            elif (role2 == 'ADM'):
                originalAdm.append(query)
        else:
            data = { "query": query, "role1": role1, "rows": rows }
            originalPent.append(data)

    newRows = []
    for i in range(trueSamples):
        randomRole = random.choice(VALID_ROLES)
        if (randomRole == 'HR'):
            newRows.append((random.choice(originalHR), 'HR', 'Y', 'HR', random.randint(1,21)))
        elif (randomRole == 'DOC'):
            newRows.append((random.choice(originalDoc), 'DOC', 'Y', 'DOC', random.randint(1,21)))
        elif (randomRole == 'ADM'):
            newRows.append((random.choice(originalAdm), 'ADM', 'Y', 'ADM', random.randint(1,21)))

    for i in range(maliciousSamples):
        rdmPent = random.choice(originalPent)
        max_rows = rdmPent["rows"]
        newRows.append((rdmPent["query"], rdmPent["role1"],'N', 'PENT', random.randint(1,max_rows)))

    #print(newRows)
    # Create a Pandas dataframe from some data.
    df = pd.DataFrame(newRows, columns=columns)
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    newFilename = 'training_data_' + '3' + '.xlsx'
    writer = pd.ExcelWriter(newFilename, engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

def get_BOW(original_queries_filename):
    retVal = list()

    sheet1 = pd.read_excel(open(original_queries_filename,'rb'), sheet_name=1)  # 'Original' tab
    for i in sheet1.index:
        query = sheet1['query'][i]
        if (query == "query"):  # only to ignore the first line, TODO should change this
            continue
        
        query = query.replace("'", "")
        query = query.replace("\"", "")
        retVal.append(query)

    print(retVal)


if __name__ == "__main__":
    print('Testing generation functions..')
    #generate_data(DEFAULT_FILENAME)
    get_BOW(DEFAULT_FILENAME)
    print 'Generation done. [', DEFAULT_FILENAME, ']'
