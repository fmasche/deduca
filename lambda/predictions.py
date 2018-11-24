from sklearn.externals import joblib
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import boto
from flask import Flask
from flask import request
from flask import json

BUCKET_NAME = 'pjhudgins-iris'
MODEL_FILE_NAME = 'iris.joblib'
MODEL_LOCAL_PATH = MODEL_FILE_NAME #'/tmp/' + MODEL_FILE_NAME

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
  req_data = request.get_data().decode('utf-8')
  print("req_data:", req_data)
  payload = json.loads(req_data)
  #prediction = predict(payload['payload'])
  prediction = predict([payload])
  data = {}
  data['data'] = str(int(prediction[-1]))
  print("prediction data:", data)
  return json.dumps(data)

def load_model():
  #conn = S3Connection("AKIAIDEGUSVRDU7KN62Q", "nQXdEYs02PIql+Yym3ItSVf4x36rS8v8RJPJTdAH", host='us-east-2')
  conn = S3Connection("AKIAIDEGUSVRDU7KN62Q", "nQXdEYs02PIql+Yym3ItSVf4x36rS8v8RJPJTdAH", host='s3.us-east-2.amazonaws.com')
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

