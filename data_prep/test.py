from sklearn import svm
from sklearn.ensemble import RandomForestClassifier

import loaders
from loaders import load_data
from loaders import DEFAULT_FILENAME
#from data_prep.preprocessing import getFeaturesCombined

import pickle

def learn(filename):
    xs, ys = load_data(filename)

    # Train a classifier
    classifier = RandomForestClassifier()
    classifier.fit(xs, ys)

    with open('model.pkl', 'wb') as model_file:
        pickle.dump(classifier, model_file)

    # query = "select employees.first_name, employees.last_name, employees.gender, employees.birth_date, employees.hire_date, salaries.salary from employees inner join salaries on employees.emp_no = salaries.emp_no where employees.emp_no = @param;"
    # features = getFeaturesCombined(query)

    # pred = classifier.predict(features)
    # print(pred)



if __name__ == "__main__":
    print('Holi')
    learn(DEFAULT_FILENAME)
    #print(result)