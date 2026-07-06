import json

from src.producer.generator import DEVICE_TYPES, BROWSERS, generate_event


class TestPageviewEvent:
    def test_event_has_required_fields(self):
        event = generate_event()
        assert event.event_id
        assert event.user_id
        assert event.page_url
        assert event.timestamp
        assert event.event_type == "pageview"
        assert event.session_id

    def test_event_serializes_to_json(self):
        event = generate_event()
        dumped = json.dumps(event.to_dict())
        loaded = json.loads(dumped)
        assert loaded["event_id"] == event.event_id
        assert loaded["session_id"] == event.session_id

    def test_events_are_unique(self):
        e1 = generate_event()
        e2 = generate_event()
        assert e1.event_id != e2.event_id
        assert e1.session_id != e2.session_id

    def test_device_type_is_valid(self):
        for _ in range(100):
            event = generate_event()
            assert event.device_type in DEVICE_TYPES

    def test_browser_is_valid(self):
        for _ in range(100):
            event = generate_event()
            assert event.browser in BROWSERS

    def test_country_code_is_two_letters(self):
        event = generate_event()
        assert len(event.country) == 2
        assert event.country.isalpha()

    def test_referrer_can_be_none(self):
        has_referrer = any(generate_event().referrer for _ in range(100))
        has_none = any(not generate_event().referrer for _ in range(100))
        assert has_referrer and has_none, "referrer should sometimes be None"

    def test_timestamp_is_iso_format(self):
        event = generate_event()
        assert "T" in event.timestamp
        assert event.timestamp.endswith("+00:00") or "+" in event.timestamp
