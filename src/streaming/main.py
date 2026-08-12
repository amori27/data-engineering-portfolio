import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    approx_count_distinct,
    col,
    count,
    from_json,
    to_timestamp,
    window,
)
from pyspark.sql.types import (
    StringType,
    StructField,
    StructType,
    TimestampType,
)

from src.streaming.config import config

logger = logging.getLogger("streamer")

PAGEVIEW_SCHEMA = StructType(
    [
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
    ]
)


def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder.appName(config.app_name)
        .master(config.spark_master)
        .config(
            "spark.jars.packages",
            ",".join(
                [
                    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2",
                    "org.postgresql:postgresql:42.7.3",
                ]
            ),
        )
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.sql.streaming.schemaInference", "true")
        .getOrCreate()
    )


def write_to_postgres(df, epoch_id: int) -> None:
    df.write.jdbc(
        url=config.pg_url,
        table="pageview_agg",
        mode="append",
        properties=config.pg_properties,
    )


def run() -> None:
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", config.kafka_broker)
        .option("subscribe", config.topic)
        .option("startingOffsets", "latest")
        .option("failOnDataLoss", "false")
        .load()
    )

    parsed = (
        raw.select(from_json(col("value").cast("string"), PAGEVIEW_SCHEMA).alias("data"))
        .select("data.*")
        .withColumn("event_timestamp", to_timestamp(col("timestamp")))
    )

    aggregated = (
        parsed.withWatermark("event_timestamp", config.watermark_duration)
        .groupBy(window(col("event_timestamp"), config.window_duration), col("page_url"))
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

    query = (
        aggregated.writeStream.foreachBatch(write_to_postgres)
        .outputMode("update")
        .trigger(processingTime=config.trigger_interval)
        .start()
    )

    logger.info(
        "Spark Streaming started: topic=%s, window=%s, trigger=%s",
        config.topic,
        config.window_duration,
        config.trigger_interval,
    )

    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        logger.info("Stopping streaming query...")
        query.stop()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    run()
