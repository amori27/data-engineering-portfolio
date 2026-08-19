import os
import sys
from pathlib import Path

import pytest
import psycopg2

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.api.config import config  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def create_schema() -> None:
    init_sql = Path(__file__).resolve().parent.parent / "config" / "init.sql"
    with psycopg2.connect(config.dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(init_sql.read_text())
        conn.commit()