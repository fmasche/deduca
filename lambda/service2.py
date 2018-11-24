# -*- coding: utf-8 -*-

import numpy
import sklearn
from sklearn.externals import joblib
from boto3.s3.key import Key
from boto3.s3.connection import S3Connection
import boto3 as boto

BUCKET_NAME = 'pjhudgins-iris'
MODEL_FILE_NAME = 'iris.joblib'
MODEL_LOCAL_PATH = 'tmp/' + MODEL_FILE_NAME


def load_model():
  #conn = S3Connection(host='s3.us-east-2.amazonaws.com') #old working
  #conn = boto.connect_s3()
  #bucket = conn.create_bucket(BUCKET_NAME)
  print("conn", conn)
  bucket = conn.get_bucket(BUCKET_NAME)
  key_obj = Key(bucket)
  key_obj.key = MODEL_FILE_NAME
  print("got key")
  contents = key_obj.get_contents_to_filename(MODEL_LOCAL_PATH)
  print("got contents")
  return joblib.load(MODEL_LOCAL_PATH)

def predict(data):
  # Process your data, create a dataframe/vector and make your predictions
  final_formatted_data = []
  model = load_model()
  print("predicting", model, data)
  preds = model.predict(data)
  return preds



def handler(event, context):
	#payload = event['prediction']
	payload = [7.0, 3.2, 4.7, 1.4]
	prediction = predict([payload])
	data = {}
	data['data'] = str(int(prediction[-1]))
	print("prediction data:", data)
	#return json.dumps(data)

	#result = {"data": "helloooo!!!!"}
	return data

if __name__ == "__main__":
	print(handler(None, None))