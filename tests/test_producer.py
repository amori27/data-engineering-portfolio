import json
from producer.main import generate_event


def test_generate_event_structure():
    event = generate_event()
    assert "event_id" in event
    assert "user_id" in event
    assert "page_url" in event
    assert "timestamp" in event
    assert "event_type" in event
    assert event["event_type"] == "pageview"


def test_generate_event_valid_json():
    event = generate_event()
    dumped = json.dumps(event)
    loaded = json.loads(dumped)
    assert loaded == event


def test_generate_event_unique_ids():
    e1 = generate_event()
    e2 = generate_event()
    assert e1["event_id"] != e2["event_id"]
