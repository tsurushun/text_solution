# yaml parser
function parse_yaml {
   local prefix=$2
   local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
   sed -ne "s|^\($s\):|\1|" \
        -e "s|^\($s\)\($w\)$s:$s[\"']\(.*\)[\"']$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p"  $1 |
   awk -F$fs '{
      indent = length($1)/2;
      vname[indent] = $2;
      for (i in vname) {if (i > indent) {delete vname[i]}}
      if (length($3) > 0) {
         vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
         printf("%s%s%s=\"%s\"\n", "'$prefix'",vn, $2, $3);
      }
   }'
}

# parse config.yaml
eval $(parse_yaml config.yml)

# create new index
curl -XPUT "$elasticsearch_HOST:9200/library/" -H 'Content-Type: application/json' -d '{
    "settings" : {
        "index" : {
            "number_of_shards" : 1, 
            "number_of_replicas" : 0
        }
    }
}'

# create a new mapping
curl -X PUT "$elasticsearch_HOST:9200/library/document/_mapping" -H 'Content-Type: application/json' -d '{
    "document" : {
        "properties" : {
            "title" : { "type" : "text"},
            "data" : { "type" : "binary", "doc_values": false, "store": false },
            "ip" : { "type" : "keyword" },
            "entities" : { "type" : "text" },
            "keyPhrases" : { "type" : "text" },
            "sentiment" : { "type" : "text" },
            "s3Location" : { "type" : "text"}
        }
    }
}'

# attachment processer
curl -X PUT "$elasticsearch_HOST:9200/_ingest/pipeline/documentpipeline" -H 'Content-Type: application/json' -d '
{
  "description" : "Pipeline description",
  "processors" : [
    {
      "attachment" : {
        "field" : "data",
        "properties": ["content", "content_type", "language", "content_length"]
      }
    }
  ]
}'