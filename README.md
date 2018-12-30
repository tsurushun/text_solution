# text_solution
Extracts entities, sentiment and key phrases from texts, then stores them in a searchable format using elasticsearch

## Architecture

Documents (pdf, Word, txt) -> Amazon S3 -> SQS -> Consumer (Python) on EC2 -> Amazon Comprehend -> Elasticsearch -> Kibana
                                                                        
## Reference

- https://www.skedler.com/blog/combine-text-analytics-search-aws-comprehend-elasticsearch-6-0/ (Most of the initial source codes were copied from this blog. Big thank you to Skedler!)  

## ToDo

- Try Lambda instead of SQS
- Try text analytic services from Google and Microsoft
- Add CERMINE to extract metadata from scientific papers in pdf format (https://github.com/CeON/CERMINE)
- Add translate for non-English languages
