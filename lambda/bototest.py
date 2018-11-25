# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 17:34:51 2018

@author: pjhud
"""

import boto3
#import botocore

BUCKET_NAME = 'pjhudgins-iris' # replace with your bucket name
KEY = 'iris.joblib' # replace with your object key

s3 = boto3.resource('s3')

try:
    bucket = s3.Bucket(BUCKET_NAME)
#    print dir(bucket)
    for key in bucket.objects.all():
        print key.key
    
    bucket.download_file(KEY, 'tmp/test.joblib')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print "The object does not exist."
    else:
        raise

import os
print(os.environ['aws_access_key_id'])
