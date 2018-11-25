from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets
import pickle
import numpy
#clf = svm.SVC(gamma='scale')
print "hello"
clf = RandomForestClassifier()
iris = datasets.load_iris()
#X, y = iris.data, iris.target

X = [[0.0]*4]*100
X = numpy.array(X)
#print X
#print iris.data
y = ['HR']*100

clf.fit(X, y)  
pickle.dump(clf, open('query_model.pkl', 'wb'))


#
#from sklearn.externals import joblib
## s = pickle.dumps(clf)
## clf2 = pickle.loads(s)
#
#s = open('iris.pkl').read()
#clf2 = pickle.loads(s)
##joblib.dump(clf, 'iris.joblib') 
##clf2 = joblib.load('iris.joblib')
#i=50
#print clf2.predict(X[i:i+1]), y[i]
#print X[i:i+1] 
## [[7.  3.2 4.7 1.4]] [7.0,3.2,4.7,1.4]
## [7.0,3.2,4.7,1.4]
## curl -d "[7.0,3.2,4.7,1.4]" http://127.0.0.1:5000/


