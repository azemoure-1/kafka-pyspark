

![1_IyFEpsA3qg_mxDHHLCoqEA](https://github.com/azemoure-1/kafka-pyspark/assets/113553607/1cc93298-b8db-495b-ab43-dbd61a388eda)





# Project Overview
In a world where data is considered the new gold, it is imperative for organizations to be able to process and analyze data in real-time to make informed decisions. This program is designed for data professionals looking to acquire practical skills in implementing real-time data pipelines.

# Configuration and Dependencies
Install the required libraries and dependencies for `Spark`, `pyspark`, `Kafka`, and use Docker images for `Cassandra` and `MongoDB`:

## Kafka Installation & Configuration
To install Kafka, follow the [link](https://kafka.apache.org/downloads). In my case, I'm using Kafka version 3.6.0 [link to binary](href="https://downloads.apache.org/kafka/3.6.0/kafka_2.12-3.6.0.tgz). 

command start zookeeper:
    ```
    zookeeper-server-start.bat ....\config\zookeeper.properties
    ```
command start kafka:
    ```
    kafka-server-start.bat ....\config\server.properties
    ```

## SPARK Installation & Configuration
To install spark, follow the [link](https://phoenixnap.com/kb/install-spark-on-windows-10). In my case, I'm using spark version 3.2.4 [link to binary](href="https://spark.apache.org/downloads.html).


## CASSANDRA Installation & Configuration
For Cassandra, we'll use a Docker image.


![5](https://github.com/azemoure-1/kafka-pyspark/assets/113553607/957f1b72-7168-4f8e-8e75-cb368b9cbf30)




![3](https://github.com/azemoure-1/kafka-pyspark/assets/113553607/532a7ecf-d832-4b46-a97c-78341def545e)





## MONGODB Installation & Configuration
For MongoDB, we'll use a Docker image as well. You can run MongoDB locally with the following Docker command:

![6](https://github.com/azemoure-1/kafka-pyspark/assets/113553607/6cd94a8b-4a12-4a49-b832-03bcc9f10f14)



![4](https://github.com/azemoure-1/kafka-pyspark/assets/113553607/9e3e63a7-931a-49eb-a8a2-be0ff2c38b70)



# Project
## Kafka Producer using confluent-kafka
Fetches random user data from the API (randomuser) and streams it to a Kafka topic, creating a data pipeline for further processing or analysis.

## PySpark Consumer using confluent-kafka
Utilize the provided code to extract data from the Kafka topic "jane__essadi__topic."
Implement data transformations, which encompass parsing, validation, and data enrichment.
Insert data into Cassandra.
Execute data aggregation to derive insights, such as the count of users by nationality and the average user age. Store these results in MongoDB through the save_to_mongodb_collection function.
Configure debugging and monitoring mechanisms to track the pipeline's performance and identify potential issues.
Develop data visualization dashboards with Python Dash to present aggregated data effectively.
## Data Visualization
Employ Python Dash to construct data visualization dashboards, enabling the presentation of aggregated data, such as user counts by nationality and average user age.

![1](https://github.com/azemoure-1/kafka-pyspark/assets/113553607/dc7e7f10-0536-40dd-8014-e61014eea9ce)



![2](https://github.com/azemoure-1/kafka-pyspark/assets/113553607/82988bcb-cddb-4011-93f2-b4066140a5c6)



GDPR Compliance In our professional context, our primary focus is protecting our clients from data-related risks. We strictly comply with the regulations of the General Data Protection Regulation (GDPR). Additionally, we prioritize securing sensitive customer information through encryption or deletion, ultimately ensuring the safety of our users.
