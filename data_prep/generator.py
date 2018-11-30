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
    originalPent = list()

    totalSamples = 12000
    maliciousSamples = (5*totalSamples) / 100
    trueSamples = totalSamples - maliciousSamples
    columns = ['query', 'role', 'valid', 'rows']

    sheet1 = pd.read_excel(open(original_queries_filename,'rb'), sheet_name=1)
    for i in sheet1.index:
        query = sheet1['query'][i]
        if (query == "query"):  # only to ignore the first line, TODO should change this
            continue
        role = sheet1['role'][i]
        valid = sheet1['valid'][i]

        if (valid == 'Y'):
            if (role == 'HR'):
                originalHR.append(query)
            elif (role == 'DOC'):
                originalDoc.append(query)
            elif (role == 'ADM'):
                originalAdm.append(query)
        else:
            originalPent.append(query)

    newRows = []
    for i in range(trueSamples):
        randomRole = random.choice(VALID_ROLES)
        if (randomRole == 'HR'):
            newRows.append((random.choice(originalHR), 'HR', 'Y', random.randint(1,21)))
        elif (randomRole == 'DOC'):
            newRows.append((random.choice(originalDoc), 'DOC', 'Y', random.randint(1,21)))
        elif (randomRole == 'ADM'):
            newRows.append((random.choice(originalAdm), 'ADM', 'Y', random.randint(1,21)))

    for i in range(maliciousSamples):
        newRows.append((random.choice(originalPent), 'PENT','N', random.randint(1,300024)))

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







if __name__ == "__main__":
    print('Testing generation functions..')
    generate_data(DEFAULT_FILENAME)
