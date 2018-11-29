from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
import numpy as np

import loaders
from loaders import load_data
from loaders import DEFAULT_FILENAME
import preprocessing
#from data_prep.preprocessing import getFeaturesCombined

import pickle

def learn(filename):
    xs, ys = load_data(filename)

    #print(xs)
    # Train a classifier
    classifier = RandomForestClassifier()
    classifier.fit(xs, ys)

    with open('model.pkl', 'wb') as model_file:
        pickle.dump(classifier, model_file)

    features = preprocessing.getFeaturesFromQuery(preprocessing.TEST_DATA)

    pred = classifier.predict(features)
    print('Prediction: ', pred[0])



if __name__ == "__main__":
    print('Holi')
    learn(DEFAULT_FILENAME)
    #print(result)