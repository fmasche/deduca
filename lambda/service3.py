# -*- coding: utf-8 -*-
import sklearn
from sklearn.externals import joblib
import boto3
import io
import pickle

BUCKET_NAME = 'pjhudgins-iris'
MODEL_KEY = 'iris.pkl'
REPORT_KEY = 'report.txt'


def load_model():
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET_NAME, MODEL_KEY)
    #model_data = obj.get()['Body'].read()
    s = obj.get()['Body'].read().decode('utf-8')
    model = pickle.loads(s)
    
    #return joblib.load(MODEL_LOCAL_PATH)
    return model
        

def predict(data):
  model = load_model()
  print("predicting", model, data)
  preds = model.predict(data)
  return preds

def upload_report():
    report = "The sky is falling!"
    data = report.encode()
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET_NAME, REPORT_KEY)
    obj.put(Body=data)
    print "uploaded"

def handler(event, context):
    payload = [7.0, 3.2, 4.7, 1.4]
    prediction = predict([payload])
    data = {}
    data['data'] = str(int(prediction[-1]))
    print "prediction data:", data 
    upload_report()
    return data

if __name__ == "__main__":
	print(handler(None, None))