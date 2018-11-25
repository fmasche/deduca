# -*- coding: utf-8 -*-
import sklearn
from sklearn.externals import joblib
import boto3
import io
import pickle

BUCKET_NAME = 'pjhudgins-iris'
MODEL_KEY = 'query_model.pkl'
REPORT_KEY = 'report.txt'

def main():
    model = load_model()
    queries = get_queries()
    
    report_lines = []
    for query in queries:
        features = get_features_from_query(query)
        predicted_role = model.predict([features])
        
        report_line = generate_report_line(query, predicted_role)
        if report_line:
            report_lines.append(report_line)
    
    report_text = '\n'.join(report_lines)
    upload_report(report_text)

def get_queries():
    """Stub, this will use Nikki's code"""
    return [{'role': 'HR', 'user': 'bob', 'rows_examined': 4, 'timestamp': '11-24-18 19:44:57', 'text': 'select * from patient'},
            {'role': 'DOC', 'user': 'alice', 'rows_examined': 2, 'timestamp': '11-24-18 19:45:00', 'text': 'select * from billing'}
            ]
    
def get_features_from_query(query):
    """Stub, this will use Fatima's preprocessing code"""
    return [0.0] * 4

def generate_report_line(query, predicted_role):
    #I'll make this more meaningful later - Paul
    if predicted_role == 'PENT':
        return query['timestamp'] + " Query appears malicious: " + query['text']
    elif query['role'] != predicted_role:
        return query['timestamp'] + " Unexpected role: " + query['text']
    else:
        return None

def load_model():
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET_NAME, MODEL_KEY)
    s = obj.get()['Body'].read().decode('utf-8')
    model = pickle.loads(s)
    return model
        
def upload_report(report_text):
    report = "The sky is falling!"
    data = report_text.encode()
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET_NAME, REPORT_KEY)
    obj.put(Body=data)
    print "Uploaded report"

def handler(event, context):
    main()
    return "Success!"

if __name__ == "__main__":
	print(handler(None, None))