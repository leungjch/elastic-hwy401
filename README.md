# elastic-hwy401

# Setup
## Install ElasticSearch and Kibana
```
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.14.1
docker run --name es01-test --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.14.1
```
Open a new terminal session to install Kibana connect it to the ElasticSearch container:
```
docker pull docker.elastic.co/kibana/kibana:7.14.1
docker run --name kib01-test --net elastic -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://es01-test:9200" docker.elastic.co/kibana/kibana:7.14.1
```
Kibana is now running on `http//localhost:5601`
