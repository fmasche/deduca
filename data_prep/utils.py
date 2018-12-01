from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import sklearn

def classification_metrics(y_true, y_pred, average):
    res = dict(
        acc=accuracy_score(y_true, y_pred),
        f1=f1_score(y_true, y_pred, average=average),

        precision=precision_score(y_true, y_pred, average=average),
        recall=recall_score(y_true, y_pred, average=average)
        )
    return res

def binary_classification_metrics(y_true, y_pred):
    return classification_metrics(y_true, y_pred, 'binary')


def multi_classification_metrics(y_true, y_pred):
    return classification_metrics(y_true, y_pred, 'weighted')    

def confusion_matrix(y_true, y_pred, cclass):
    #matrix = sklearn.metrics.confusion_matrix(y_true, y_pred)
    #print('Confusion matrix: ')
    #print(matrix)
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(len(y_pred)): 
        if y_true[i] == cclass and y_pred[i] == cclass:
           TP += 1
        if y_pred[i] != cclass and y_true[i] == cclass:
           FP += 1
        if y_true[i] != cclass and y_pred[i] != cclass:
           TN += 1
        if y_pred[i] == cclass and y_true[i] != cclass:
           FN += 1

    res = dict(
        TP = TP,
        FP = FP,
        TN = TN,
        FN = FN
    )
    return res

# def calculate_rate(yTest, pred_Y_test):
#     hrMetrics = confusion_matrix(yTest, pred_Y_test, "HR")
#     docMetrics = confusion_matrix(yTest, pred_Y_test, "DOC")
#     admMetrics = confusion_matrix(yTest, pred_Y_test, "ADM")
#     pentMetrics = confusion_matrix(yTest, pred_Y_test, "PENT")
    

