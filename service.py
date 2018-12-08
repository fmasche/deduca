# -*- coding: utf-8 -*-
import sklearn
from sklearn.externals import joblib
import boto3
import io
import pickle
import data_prep.preprocessing
import query_log

BUCKET_NAME = 'pjhudgins-iris'
MODEL_KEY = 'model.pkl'
REPORT_KEY = 'report.txt'

def main():
    model = load_model()
    queries = get_queries()
    
    report_lines = []
    for query in queries:
        try:
            features = get_features_from_query(query)
        except:
            continue
        
        predicted_role = model.predict(features)
        predicted_role = str(predicted_role[0])
        #print predicted_role, query['text']

        
        report_line = generate_report_line(query, predicted_role)
        if report_line:
            report_lines.append(report_line)
    
    report_text = '\n'.join(report_lines)
    print "Report:\n", report_text
    upload_report(report_text)

def get_queries():
    queries = query_log.get_queries()
    #print queries[0]
    return queries
    
def get_features_from_query(query):
    return data_prep.preprocessing.getFeaturesFromQuery(query)
    #return [0.0] * 4

def generate_report_line(query, predicted_role):
    report = query['timestamp'] 
    if predicted_role == 'PENT':
        report += "  WARNING: Appears malicious: "
    elif query['role'] != predicted_role:
        report += "  WARNING: Unexpected role:   "
    else:
        report += "           Nominal query:     "
    report += query['role'].rjust(4) + '/' + predicted_role.ljust(4) + '  '
    report += query['text'][:100]
    report += '\n'
    return report
    
    # if predicted_role == 'PENT':
    #     return query['timestamp'] + " Query appears malicious: " + query['text']
    # elif query['role'] != predicted_role:
    #     return query['timestamp'] + " Unexpected role: " + query['text']
    # else:
    #     return None

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