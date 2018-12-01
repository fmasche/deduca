from os import listdir, path
import numpy as np
import pandas
import preprocessing

DEFAULT_FILENAME = "files/training_data_3.xlsx"

def load_data(filename):
    xArr = []
    yArr = []
    xTestArr = []
    yTestArr = []

    excepCount = 0
    data = dict()   
    df = pandas.read_excel(open(filename,'rb'), sheet_name=0)   # training
    for i in df.index:
        data["text"] = df['query'][i]
        data["rows_examined"] = df['rows'][i]
        role = df['role2'][i]
        if (data["text"] == "query"):  # only to ignore the first line, TODO should change this
            continue
        try:
            features = preprocessing.getFeaturesFromDBSAFE(data)
            #print(features)
            xArr.append(features[0])
            yArr.append(role)
        except Exception as error:
            print(error)
            excepCount = excepCount + 1

    df = pandas.read_excel(open(filename,'rb'), sheet_name=0)   # test
    for i in df.index:
        data["text"] = df['query'][i]
        data["rows_examined"] = df['rows'][i]
        role = df['role2'][i]
        if (data["text"] == "query"):  # only to ignore the first line, TODO should change this
            continue
        try:
            features = preprocessing.getFeaturesFromDBSAFE(data)
            #print(features)
            xTestArr.append(features[0])
            yTestArr.append(role)
        except Exception as error:
            print(error)
            excepCount = excepCount + 1

    return np.array(xArr), np.array(yArr), np.array(xTestArr), np.array(yTestArr)


def load_training_test_data(filename):
    xTraining = list()
    yTraining = list()
    bow = list()
    xTest = list()
    yTest = list()

    df = pandas.read_excel(open(filename,'rb'), sheet_name=0)       # training
    for i in df.index:
        if (df['query'][i] == "query"):  # only to ignore the first line, TODO should change this
            continue
        try:
            xTraining.append([df['query'][i], df['rows'][i]])
            yTraining.append(df['role'][i])

            bow.append(df['query'][i])
        except Exception as error:
            print(error)
            pass

    df = pandas.read_excel(open(filename,'rb'), sheet_name=2)       # test
    for i in df.index:
        if (df['query'][i] == "query"):  # only to ignore the first line, TODO should change this
            continue
        try:
            xTest.append([df['query'][i], df['rows'][i]])
            yTest.append(df['role2'][i])
        except Exception as error:
            print(error)
            pass            
            
    return np.array(xTraining), np.array(yTraining), np.array(xTest), np.array(yTest), np.array(bow)


if __name__ == "__main__":
    print('Testing load functions..')
    load_data(DEFAULT_FILENAME)
