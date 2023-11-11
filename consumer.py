import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType
from cassandra.cluster import Cluster


# Initialize a Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkIntegration") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4,"
            "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0,"
            "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .config('spark.cassandra.connection.host', 'localhost') \
    .getOrCreate()

# Define the Kafka broker and topic to consume data from
kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "user_profiles"

# Define the Kafka consumer configuration
kafka_consumer_options = {
    "kafka.bootstrap.servers": kafka_bootstrap_servers,
    "subscribe": kafka_topic,
    "startingOffsets": "latest",
    "failOnDataLoss": "false"
}

# Define the Cassandra keyspace and table
cassandra_keyspace = "user_keyspace"
cassandra_table = "user_profiles"

cluster = Cluster(['localhost'])
session = cluster.connect()

# Create the keyspace
create_keyspace_query = f"CREATE KEYSPACE IF NOT EXISTS {cassandra_keyspace} WITH REPLICATION = {{ 'class' : 'SimpleStrategy', 'replication_factor' : 1 }}"
session.execute(create_keyspace_query)

# Use the keyspace
session.set_keyspace(cassandra_keyspace)

# Create the table with a generated UUID as the primary key
create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {cassandra_keyspace}.{cassandra_table} (
        id UUID PRIMARY KEY,
        gender TEXT,
        full_name TEXT,
        adresse TEXT,
        email TEXT,
        email_domain TEXT,
        username TEXT,
        date_of_birth TEXT,
        age TEXT,
        phone TEXT,
        cell TEXT,
        nationality TEXT
    )
"""

session.execute(create_table_query)

# Close the Cassandra session
session.shutdown()

# Create the schema to parse the JSON data
json_schema = StructType([
    StructField("gender", StringType(), True),
    StructField("name", StructType([
        StructField("title", StringType(), True),
        StructField("first", StringType(), True),
        StructField("last", StringType(), True)
    ]), True),
    StructField("location", StructType([
        StructField("country", StringType(), True),
        StructField("city", StringType(), True),
        StructField("postcode", StringType(), True)
    ]), True),
    StructField("email", StringType(), True),
    StructField("login", StructType([
        StructField("uuid", StringType(), True),
        StructField("username", StringType(), True)
    ]), True),
    StructField("dob", StructType([
        StructField("date", StringType(), True),
        StructField("age", StringType(), True)
    ]), True),
    StructField("phone", StringType(), True),
    StructField("cell", StringType(), True),
    StructField("nat", StringType(), True)
])

# Read data from Kafka
kafka_stream = spark.readStream.format("kafka") \
    .options(**kafka_consumer_options) \
    .load()

# Deserialize the value from Kafka as JSON and parse it using the defined schema
kafka_stream = kafka_stream.selectExpr("CAST(value AS STRING) as json_value") \
    .select(from_json("json_value", json_schema).alias("data"))



# Add a generated UUID column
kafka_stream = kafka_stream.withColumn("id", expr("uuid()"))


# cassandra

# Define a separate function to save data to Cassandra
def save_to_cassandra_collection(cassandra_keyspace, cassandra_table, kafka_stream):
    transformed_stream_cassandra = kafka_stream.select(
        col("id"),
        col("data.gender"),
        concat_ws(" ", col("data.name.first"), col("data.name.last")).alias("full_name"),
        concat_ws(" ", col("data.location.country"), col("data.location.city"), col("data.location.postcode")).alias("adresse"),
        col("data.email"),
        (substring_index(col("data.email"), "@", -1)).alias("email_domain"),
        col("data.login.username").alias("username"),
        col("data.dob.date").alias("date_of_birth"),
        col("data.dob.age").alias("age"),
        col("data.phone"),
        col("data.cell"),
        col("data.nat").alias("nationality")
    )

    # Chiffrez les données des colonnes avec SHA-256
    transformed_stream_cassandra = transformed_stream_cassandra.withColumn("phone", sha2(col("phone"), 256))
    transformed_stream_cassandra = transformed_stream_cassandra.withColumn("cell", sha2(col("cell"), 256))
    transformed_stream_cassandra = transformed_stream_cassandra.withColumn("email", sha2(col("email"), 256))

    # Write the data to Cassandra
    cassandra_write_options = {
        "keyspace": cassandra_keyspace,
        "table": cassandra_table,
    }

    try:
        # Start the Cassandra streaming query
        cassandra_query = transformed_stream_cassandra.writeStream \
            .outputMode("append") \
            .format("org.apache.spark.sql.cassandra") \
            .option("checkpointLocation", "./checkpoint/data_cassandra") \
            .options(**cassandra_write_options) \
            .start()

        # Wait for the query to terminate (optional)
        cassandra_query.awaitTermination()

    except Exception as e:
        print(f"An error occurred while writing to Cassandra: {e}")
        # Handle the exception as needed

# Call the function to save data to Cassandra
save_to_cassandra_collection(cassandra_keyspace, cassandra_table, kafka_stream)


# mongodb

mongo_uri = "mongodb://localhost:27017"
mongo_db_name = "users_informations"
collection_name = "user_profiles"

# Define a separate function to save data to MongoDB
def save_to_mongodb_collection(mongo_uri, mongo_db_name, collection_name, kafka_stream):
    transformed_stream_mongo = kafka_stream.select(
        col("data.gender"),
        concat_ws(" ", col("data.name.first"), col("data.name.last")).alias("full_name"),
        concat_ws(" ", col("data.location.country"), col("data.location.city"), col("data.location.postcode")).alias("adresse"),
        (substring_index(col("data.email"), "@", -1)).alias("email_domain"),
        col("data.login.username").alias("username"),
        col("data.dob.age").alias("age"),
        col("data.nat").alias("nationality")
    )

    # Start the MongoDB streaming query
    mongo_query = transformed_stream_mongo.writeStream \
        .foreachBatch(lambda batchDF, batchId: batchDF.write \
            .format("mongo") \
            .option("uri", mongo_uri) \
            .option("database", mongo_db_name) \
            .option("collection", collection_name) \
            .mode("append") \
            .save()
        ) \
        .outputMode("append") \
        .start()

    # Start the console streaming query for debugging (optional)
    console_query = kafka_stream.writeStream.outputMode("append").format("console").start()
    
    console_query.awaitTermination()

# Call the function to save data to MongoDB
save_to_mongodb_collection(mongo_uri, mongo_db_name, collection_name, kafka_stream)
