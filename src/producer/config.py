import os
from dataclasses import dataclass, field


@dataclass
class ProducerConfig:
    bootstrap_servers: str = field(
        default_factory=lambda: os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    )
    topic: str = field(
        default_factory=lambda: os.getenv("KAFKA_TOPIC", "pageviews")
    )
    events_per_second: int = field(
        default_factory=lambda: int(os.getenv("PRODUCER_EVENTS_PER_SECOND", "10"))
    )
    max_events: int = field(
        default_factory=lambda: int(os.getenv("PRODUCER_MAX_EVENTS", "0"))
    )
    client_id: str = "clickstream-producer"


config = ProducerConfig()
