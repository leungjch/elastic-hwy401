# elastic-hwy401

## How it works
The Ministry of Transportation of Ontario (MTO) places many cameras across parts of the provincial highway system, through [511on.ca](https://511on.ca/). I simply run the camera streams through a pretrained YOLOv5 model and get the counts of the vehicles (trucks, cars, motorcycles, buses), and stream it into Elasticsearch. 

Inspired by many frustrating experiences on the 401. 

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
