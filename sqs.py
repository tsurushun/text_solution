import boto3 
from comprehend import process_document
import yaml
import json

# read config
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

BUCKET_NAME = cfg['AWS']['BUCKET_NAME']

s3_client_connection = boto3.client(
    's3'
)

def consume_from_sqs(message):
    body = json.loads(message.body)
    
    # Extract uploaded document details
    key = body['Records'][0]['s3']['object']['key']
    
    # download the document from S3
    local_path = "{}".format(key)
    s3_client_connection.download_file(BUCKET_NAME, key, local_path)

    # detect entities
    info = process_document(local_path)

    return info, local_path