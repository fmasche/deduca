from os import listdir, path
import numpy as np
import pandas
import preprocessing

DEFAULT_FILENAME = "files/training_data_1.xlsx"

def load_data(filename):
    xArr = []
    yArr = []
    excepCount = 0
    df = pandas.read_excel(open(filename,'rb'), sheet_name=0)
    for i in df.index:
        query = df['query'][i]
        role = df['role2'][i]
        if (query == "query"):  # only to ignore the first line, TODO should change this
            continue
        try:
            features = preprocessing.getFeaturesCombined(query)
            xArr.append(features)
            yArr.append(role)
        except Exception as error:
            excepCount = excepCount + 1
            

    xs = np.array(xArr)
    ys = np.array(yArr)
    print("xs shape: ", xs.shape)     
    return xs, ys


if __name__ == "__main__":
    print('Testing load functions..')
    load_data(DEFAULT_FILENAME)
