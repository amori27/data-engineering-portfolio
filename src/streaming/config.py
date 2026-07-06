import os
from dataclasses import dataclass, field


@dataclass
class StreamingConfig:
    kafka_broker: str = field(
        default_factory=lambda: os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    )
    topic: str = field(
        default_factory=lambda: os.getenv("KAFKA_TOPIC", "pageviews")
    )
    pg_host: str = field(default_factory=lambda: os.getenv("POSTGRES_HOST", "localhost"))
    pg_port: int = field(default_factory=lambda: int(os.getenv("POSTGRES_PORT", "5432")))
    pg_db: str = field(default_factory=lambda: os.getenv("POSTGRES_DB", "analytics"))
    pg_user: str = field(default_factory=lambda: os.getenv("POSTGRES_USER", "user"))
    pg_password: str = field(default_factory=lambda: os.getenv("POSTGRES_PASSWORD", "pass"))
    spark_master: str = field(
        default_factory=lambda: os.getenv("SPARK_MASTER", "local[*]")
    )
    app_name: str = field(
        default_factory=lambda: os.getenv("SPARK_APP_NAME", "clickstream-pipeline")
    )
    watermark_duration: str = "1 minute"
    window_duration: str = "1 minute"
    trigger_interval: str = "30 seconds"

    @property
    def pg_url(self) -> str:
        return f"jdbc:postgresql://{self.pg_host}:{self.pg_port}/{self.pg_db}"

    @property
    def pg_properties(self) -> dict:
        return {
            "user": self.pg_user,
            "password": self.pg_password,
            "driver": "org.postgresql.Driver",
        }


config = StreamingConfig()
