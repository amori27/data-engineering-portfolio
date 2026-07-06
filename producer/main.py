import json
import uuid
import time
from datetime import datetime, timezone
from confluent_kafka import Producer
from faker import Faker

fake = Faker()
BROKER = "localhost:9092"
TOPIC = "pageviews"

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")

def generate_event():
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": fake.uuid4(),
        "page_url": fake.uri(),
        "page_title": fake.catch_phrase(),
        "referrer": fake.uri() if fake.boolean(chance_of_getting_true=60) else None,
        "user_agent": fake.user_agent(),
        "ip_address": fake.ipv4(),
        "country": fake.country_code(),
        "device_type": fake.random_element(["mobile", "desktop", "tablet"]),
        "browser": fake.random_element(["Chrome", "Firefox", "Safari", "Edge"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "pageview",
        "session_id": str(uuid.uuid4()),
    }

def main():
    conf = {"bootstrap.servers": BROKER, "client.id": "clickstream-producer"}
    producer = Producer(conf)

    print(f"Producing events to {TOPIC}...")
    try:
        while True:
            event = generate_event()
            producer.produce(
                TOPIC,
                key=event["session_id"],
                value=json.dumps(event).encode(),
                callback=delivery_report,
            )
            producer.poll(0)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping producer.")
    finally:
        producer.flush()

if __name__ == "__main__":
    main()
