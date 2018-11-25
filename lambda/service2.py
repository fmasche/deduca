# -*- coding: utf-8 -*-
import sklearn
from sklearn.externals import joblib
import boto3
import io

BUCKET_NAME = 'pjhudgins-iris'
MODEL_KEY = 'iris.joblib'
MODEL_LOCAL_PATH = 'tmp/' + MODEL_KEY


def load_model():
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET_NAME, MODEL_KEY)
    model_data = obj.get()['Body'].read()
    file_obj = io.BytesIO(model_data)
    model = joblib.load(file_obj)
    
    #return joblib.load(MODEL_LOCAL_PATH)
    return model
        

def predict(data):
  model = load_model()
  print("predicting", model, data)
  preds = model.predict(data)
  return preds

def handler(event, context):
	payload = [7.0, 3.2, 4.7, 1.4]
	prediction = predict([payload])
	data = {}
	data['data'] = str(int(prediction[-1]))
	print "prediction data:", data
	return data

if __name__ == "__main__":
	print(handler(None, None))