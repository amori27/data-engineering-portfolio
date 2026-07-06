import json
import logging
import signal
import sys
import time
from typing import Optional

from confluent_kafka import Producer

from src.producer.config import config
from src.producer.generator import generate_event

logger = logging.getLogger("producer")
running = True


def delivery_report(err: Optional[str], msg) -> None:
    if err is not None:
        logger.error("Delivery failed for %s: %s", msg.key(), err)


def handle_shutdown(signum, frame) -> None:
    global running
    logger.info("Shutdown signal received. Flushing pending messages...")
    running = False


def create_producer() -> Producer:
    conf = {
        "bootstrap.servers": config.bootstrap_servers,
        "client.id": config.client_id,
        "acks": "1",
        "retries": 3,
        "enable.idempotence": True,
    }
    return Producer(conf)


def run(producer: Optional[Producer] = None) -> None:
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    producer = producer or create_producer()
    delay = 1.0 / config.events_per_second
    sent = 0

    logger.info(
        "Starting producer: %s events/s on topic '%s'",
        config.events_per_second,
        config.topic,
    )

    try:
        while running:
            event = generate_event()
            producer.produce(
                config.topic,
                key=event.session_id,
                value=json.dumps(event.to_dict()).encode(),
                callback=delivery_report,
            )
            producer.poll(0)
            sent += 1

            if config.max_events and sent >= config.max_events:
                logger.info("Reached max_events=%d. Stopping.", config.max_events)
                break

            time.sleep(delay)

    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Flushing producer...")
        producer.flush(timeout=10)
        logger.info("Producer stopped. %d events sent.", sent)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    run()
