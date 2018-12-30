from elasticsearch import Elasticsearch
import os
import yaml

# read config
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

esHost = cfg['elasticsearch']['HOST']
es_client = Elasticsearch(esHost)


def create_es_document(title, base64data, ip, entites, key_phrases,
 sentiment, s3_location):
    return {
        "title" : title,
        "data" : base64data.decode("utf-8"),
        "ip" : ip,
        "entities": entites,
        "keyPhrases": key_phrases,
        "sentiment": sentiment,
        "s3Location": s3_location
    }

def index_es_document(document):
    es_client.index(
        index='library',
        doc_type='document', 
        body=document,
        pipeline='documentpipeline' 
    ) 

