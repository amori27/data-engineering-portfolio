import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, to_timestamp, count, approx_count_distinct
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

KAFKA_BROKER = "localhost:9092"
TOPIC = "pageviews"
PG_URL = "jdbc:postgresql://localhost:5432/analytics"
PG_PROPS = {"user": "user", "password": "pass", "driver": "org.postgresql.Driver"}

SCHEMA = StructType([
    StructField("event_id", StringType()),
    StructField("user_id", StringType()),
    StructField("page_url", StringType()),
    StructField("page_title", StringType()),
    StructField("referrer", StringType()),
    StructField("user_agent", StringType()),
    StructField("ip_address", StringType()),
    StructField("country", StringType()),
    StructField("device_type", StringType()),
    StructField("browser", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("event_type", StringType()),
    StructField("session_id", StringType()),
])

def main():
    spark = (
        SparkSession.builder
        .appName("clickstream-pipeline")
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,org.postgresql:postgresql:42.7.3")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    raw = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BROKER)
        .option("subscribe", TOPIC)
        .option("startingOffsets", "latest")
        .load()
    )

    parsed = (
        raw
        .select(from_json(col("value").cast("string"), SCHEMA).alias("data"))
        .select("data.*")
    )

    agg = (
        parsed
        .withWatermark("timestamp", "1 minute")
        .groupBy(window(col("timestamp"), "1 minute"), col("page_url"))
        .agg(
            count("*").alias("view_count"),
            approx_count_distinct("user_id").alias("unique_users"),
        )
        .select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            "page_url",
            "view_count",
            "unique_users",
        )
    )

    def write_to_pg(df, epoch_id):
        df.write.jdbc(url=PG_URL, table="pageview_agg", mode="append", properties=PG_PROPS)

    query = (
        agg.writeStream
        .foreachBatch(write_to_pg)
        .outputMode("update")
        .trigger(processingTime="30 seconds")
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()
