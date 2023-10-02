# Architecture Diagram
![alt text](https://github.com/AbdullahAshfaq/ML_TradeStation/tree/main/images/e2e_stream_pipeline.svg?raw=true)


# Flow 1

Finnhub -> Kafka (Topic = Symbol) -> Flink -> MySQL



# Flow 2 
Depends on Flow 1 i.e. consumes data from Kafka or MySQL

Kafka -> Spark ML -> Kafka




# Resources
## Flink
Need connecter to read from Kafka and write to mysql
Download from here
https://mvnrepository.com/artifact/org.apache.flink/flink-sql-connector-kafka/1.17.1

To solve error Could not found the Java class 'org.apache.flink.connector.jdbc.JdbcConnectionOptions.JdbcConnectionOptionsBuilder'
https://mvnrepository.com/artifact/org.apache.flink/flink-connector-jdbc/3.1.1-1.17


There is already a connector when you install pyflink. Its at path `.venv/lib/python3.10/site-packages/pyflink/lib`

FlinkKafkaConsumer in pyflink relies on Java's FlinkKafkaConsumer implementation

You need to download the kafka connector jar package to the lib directory of pyflink. Generally, the path of the lib directory is: /usr/local/lib/python3.8.2/site-packages/pyflink/lib



Airflow Container packages
```bash

docker exec -it docker-airflow_webserver_1 bash

# When inside the container
pip3 install kafka-python mysql.connector finnhub-python 

```