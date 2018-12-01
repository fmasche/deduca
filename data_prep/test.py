
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

from loaders import load_data
from loaders import load_training_test_data
from loaders import DEFAULT_FILENAME
import preprocessing
import utils
import pickle

def learn(filename):
    xs, ys, xTest, yTest = load_data(filename)

    # Train a classifier
    classifier = RandomForestClassifier()
    classifier.fit(xs, ys)

    with open('model.pkl', 'wb') as model_file:
        pickle.dump(classifier, model_file)

    features = preprocessing.getFeaturesFromQuery(preprocessing.TEST_DATA)

    pred = classifier.predict(features)
    print('Prediction: ', pred[0])

    pred_Y = classifier.predict(xs)
    metrics = utils.multi_classification_metrics(ys, pred_Y)
    print("Train Performance:")
    print("%s: %s" % ("RandomForestClassifier", str(metrics)))

    pred_Y_test = classifier.predict(xTest)
    test_metrics = utils.multi_classification_metrics(yTest, pred_Y_test)
    print("Test Performance:")
    print("%s: %s" % ("GradientBoostingClassifier", str(test_metrics)))


def learn_bag_of_words(filename):
    xTraining, yTraining, xTest, yTest, bow = load_training_test_data(filename)

    vectorizer = CountVectorizer(analyzer="word",
                           stop_words=None,
                           min_df=0)

    print("bow shape: ", bow.shape)
    cvec_X = vectorizer.fit_transform(bow).toarray()

    hola = np.array([i[0] for i in xTest])
    print("xTest shape: ", hola.shape)
    cvec_X_test = vectorizer.transform(hola).toarray()

    data = dict()
    xTraining_ = list()
    for idx in range(len(xTraining)):
        # print('idx: ', idx, ' - xTraining[idx]: ', xTraining[idx][0])
        # print(cvec_X[idx])
        data["text"] = xTraining[idx][0]
        data["rows_examined"] = xTraining[idx][1]
        
        d_features = preprocessing.getFeaturesFromQuery(data)
        # print("d_features[0]: ", d_features[0])
        d_features = d_features[0].flatten()
        diosmio = cvec_X[idx].flatten()

        # print("d_features: ", d_features)
        # print("diosmio: ", diosmio)
        mergedlist = []
        mergedlist.extend(d_features)
        mergedlist.extend(diosmio)
        # print('MERGED')
        # print(mergedlist)

        xTraining_.append(mergedlist)
    
    xTest_ = list()
    for idx in range(len(xTest)):
        data["text"] = xTraining[idx][0]
        data["rows_examined"] = xTraining[idx][1]

        d_features = preprocessing.getFeaturesFromQuery(data)
        d_features = d_features[0].flatten()
        diosmio = cvec_X_test[idx].flatten()
        
        mergedlist = []
        mergedlist.extend(d_features)
        mergedlist.extend(diosmio)

        xTest_.append(mergedlist)

    xTraining_ = np.array(xTraining_)
    xTest_ = np.array(xTest_)

    print('xTraining_ shape: ', xTraining_.shape)
    print('xTest_ shape: ', xTest_.shape)
    # Train a classifier
    classifier = GradientBoostingClassifier()
    classifier.fit(np.array(xTraining_), yTraining)
    
    pred_Y = classifier.predict(np.array(xTraining_))
    metrics = utils.multi_classification_metrics(yTraining, pred_Y)
    print("Train Performance:")
    print("%s: %s" % ("GradientBoostingClassifier", str(metrics)))

    pred_Y_test = classifier.predict(np.array(xTest_))
    test_metrics = utils.multi_classification_metrics(yTest, pred_Y_test)
    print("Test Performance:")
    print("%s: %s" % ("GradientBoostingClassifier", str(test_metrics)))
    
    print("%s: %s" % ("Rate HR", str(utils.confusion_matrix(yTest, pred_Y_test, "HR"))))
    print("%s: %s" % ("Rate DOC", str(utils.confusion_matrix(yTest, pred_Y_test, "DOC"))))
    print("%s: %s" % ("Rate ADM", str(utils.confusion_matrix(yTest, pred_Y_test, "ADM"))))
    print("%s: %s" % ("Rate PENT", str(utils.confusion_matrix(yTest, pred_Y_test, "PENT"))))

    # test_metrics = {"test_%s" % k: v for k, v in test_metrics.items()}
    # metrics.update(test_metrics)

    return cvec_X, yTraining, cvec_X_test, yTest


if __name__ == "__main__":
    print('Holi')
    #learn(DEFAULT_FILENAME)
    learn_bag_of_words(DEFAULT_FILENAME)
    #print(result)