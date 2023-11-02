# Project Overview
In a world where data is considered the new gold, it is imperative for organizations to be able to process and analyze data in real-time to make informed decisions. This program is designed for data professionals looking to acquire practical skills in implementing real-time data pipelines.

# Configuration and Dependencies
Install the required libraries and dependencies for `Spark`, `pyspark`, `Kafka`, `Cassandra`, and `MongoDB`:

## Kafka Installation & Configuration
To install Kafka, follow the [link](https://kafka.apache.org/downloads). In my case, I'm using Kafka version 3.6.0 [link to binary](href="https://downloads.apache.org/kafka/3.6.0/kafka_2.12-3.6.0.tgz).

## SPARK Installation & Configuration
Later.

## CASSANDRA Installation & Configuration
Later.

## MONGODB Installation & Configuration
Later.

# Project
## Kafka Producer using `confluent-kafka`
Fetches random user data from the API (randomuser) and streams it to a Kafka topic, creating a data pipeline for further processing or analysis.

## PySpark Consumer using `confluent-kafka`
- Utilize the provided code to extract data from the Kafka topic "jane__essadi__topic."
- Implement data transformations, which encompass parsing, validation, and data enrichment.
- Insert data into Cassandra.
- Execute data aggregation to derive insights, such as the count of users by nationality and the average user age. Store these results in MongoDB through the `save_to_mongodb_collection` function.
- Configure debugging and monitoring mechanisms to track the pipeline's performance and identify potential issues.
- Develop data visualization dashboards with Python Dash to present aggregated data effectively.

## Data Visualization
Employ Python Dash to construct data visualization dashboards, enabling the presentation of aggregated data, such as user counts by nationality and average user age.

# GDPR Compliance
In our professional context, our primary focus is on safeguarding our clients from data-related risks. We meticulously adhere to GDPR regulations, including refraining from collecting data on individuals below the age of 18. Additionally, we prioritize securing sensitive client information through encryption or deletion, ultimately ensuring the safety of our users.

