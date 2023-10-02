# How to Setup the Infrastructure

Install Docker engine and docker-compose

## Airflow infrastructure
```bash
cd docker/docker-airflow
docker-compose -f docker-compose-LocalExecutor.yml up -d

#To check
docker-compose -f docker-compose-LocalExecutor.yml ps
```


## MySQL Database
```bash
cd docker/mysql
docker-compose up -d
# root password is in docker-compose.yml file
```

## Kafka infrastructure
```bash
cd docker/kafka_spark_structured_streaming
docker-compose up -d
# If any container stops, start only that one explicitly
# All containers should be running
```




