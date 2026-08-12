import uuid
from dataclasses import asdict, dataclass
from datetime import UTC, datetime

from faker import Faker

fake = Faker()

DEVICE_TYPES = ["mobile", "desktop", "tablet"]
BROWSERS = ["Chrome", "Firefox", "Safari", "Edge", "Opera"]


@dataclass
class PageviewEvent:
    event_id: str
    user_id: str
    page_url: str
    page_title: str | None
    referrer: str | None
    user_agent: str
    ip_address: str
    country: str
    device_type: str
    browser: str
    timestamp: str
    event_type: str
    session_id: str

    def to_dict(self) -> dict:
        return asdict(self)


def generate_event() -> PageviewEvent:
    return PageviewEvent(
        event_id=str(uuid.uuid4()),
        user_id=str(uuid.uuid4()),
        page_url=fake.uri(),
        page_title=fake.catch_phrase(),
        referrer=fake.uri() if fake.boolean(chance_of_getting_true=60) else None,
        user_agent=fake.user_agent(),
        ip_address=fake.ipv4(),
        country=fake.country_code(),
        device_type=fake.random_element(DEVICE_TYPES),
        browser=fake.random_element(BROWSERS),
        timestamp=datetime.now(UTC).isoformat(),
        event_type="pageview",
        session_id=str(uuid.uuid4()),
    )
