import data_prep.preprocessing
from data_prep.preprocessing import getFeaturesFromQuery
from data_prep.loaders import load_data
from data_prep.loaders import DEFAULT_FILENAME
import pandas
import sklearn.naive_bayes
import sklearn.ensemble
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
import random


def load_queries(filename):
    queries = []
    df = pandas.read_excel(open(filename,'rb'), sheet_name=0)    
    for i in df.index:
        data = dict() 
        data["text"] = df['query'][i]
        data["rows_examined"] = df['rows'][i]
        data["role"] = df['role1'][i]
        data["role2"] = df['role2'][i]
        data["valid"] = df['valid'][i]
        if (data["text"] == "query"):  # only to ignore the first line, TODO should change this
            continue
        queries.append(data)
    return queries

def predicted_valid(query, predicted_role):
    #I'll make this more meaningful later - Paul
    if predicted_role == 'PENT':
        return 'N'
    elif query['role'] != predicted_role:
        return 'N'
    else:
        return 'Y'

def score(train_queries, test_queries, classifier_constructor):
    train_xs = [getFeaturesFromQuery(query)[0] for query in train_queries]
    train_ys = [query['role2'] for query in train_queries]
    classifier = classifier_constructor()
    classifier.fit(train_xs, train_ys)

    test_xs = [getFeaturesFromQuery(query)[0] for query in test_queries]
    test_pred_roles = classifier.predict(test_xs)
    tp, tn, fp, fn = 0,0,0,0
    for i in range(len(test_queries)):
        query = test_queries[i]
        pred_valid = predicted_valid(query, test_pred_roles[i])
        #print query['role'], query['role2'], test_pred_roles[i], query['valid'], pred_valid
        if pred_valid == 'Y' and query['valid'] == 'Y':
            tn += 1
        elif pred_valid == 'Y' and query['valid'] == 'N':
            fn += 1
        elif pred_valid == 'N' and query['valid'] == 'Y':
            fp += 1
        elif pred_valid == 'N' and query['valid'] == 'N':
            tp += 1
        else:
            raise Exception()
    
    return tp, tn, fp, fn


def xval(queries, classifier_constructor):
    num_splits = 5
    random.shuffle(queries)
    size = len(queries) / 5
    tp, tn, fp, fn = 0, 0, 0, 0
    for i in range(num_splits):
        test_queries = queries[size*i:size*(i+1)]
        train_queries = queries[:size*i] + queries[size*(i+1):]
        tp_split, tn_split, fp_split, fn_split = score(train_queries, test_queries, classifier_constructor)
        print tp_split, tn_split, fp_split, fn_split

        tp += tp_split
        tn += tn_split
        fp += fp_split
        fn += fn_split
        #train_queries2 = queries[size*(i+1):]
        print len(test_queries), len(train_queries)#, len(train_queries2)
    return tp, tn, fp, fn

def analyze(tp, tn, fp, fn):
    n = tp+tn+fp+fn
    print tp, tn, fp, fn
    print 'n', n, 'accuracy', round(float(tp+tn)/n, 3), 'fp', round(float(fp)/n, 3), 'fn', round(float(fn)/n, 3)


qs = load_queries("files/training_data_1.xlsx")
print qs[1]

results = xval(qs, sklearn.naive_bayes.MultinomialNB)
analyze(*results)


