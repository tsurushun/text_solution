import boto3 as boto3
import time
import json
import os
import base64
import yaml
from sqs import consume_from_sqs
from index_document import create_es_document, index_es_document

# read config
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

AWS_REGION = cfg['AWS']['AWS_REGION']
SQS_QUEUE_NAME = cfg['AWS']['SQS_QUEUE_NAME']
BUCKET_NAME = cfg['AWS']['BUCKET_NAME']

# sqs connection
sqs_resource_connection = boto3.resource(
    'sqs',
    region_name = AWS_REGION
)
 
queue = sqs_resource_connection.get_queue_by_name(QueueName = SQS_QUEUE_NAME)
 
while True:
    messages = queue.receive_messages(MaxNumberOfMessages = 1, WaitTimeSeconds  = 5)
    for message in messages:
        body = json.loads(message.body)

        if 'Records' not in body.keys():
            continue

        filename_key = body['Records'][0]['s3']['object']['key']
        ip = body['Records'][0]['requestParameters']['sourceIPAddress']

        # extract info from documents
        info, local_path = consume_from_sqs(message)

        # add data to elastic search
        # read document data
        base64data = base64.b64encode(open(local_path,"rb").read())

        # get s3 path
        s3_path = 'https://s3-' + AWS_REGION + '.amazonaws.com/' \
            + BUCKET_NAME + '/' + filename_key

        # create document object
        document = create_es_document(
            filename_key,
            base64data, 
            ip, 
            info['entities'], 
            info['key_phrases'], 
            info['sentiment'], 
            s3_path
        ) 

        # index document to es
        index_es_document(document)

        # clean up
        os.remove(local_path)
        message.delete()
 
    time.sleep(10)