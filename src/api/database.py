import logging
from contextlib import contextmanager
from typing import Generator, Optional

import psycopg2
import psycopg2.extras

from src.api.config import config

logger = logging.getLogger("api")


@contextmanager
def get_connection() -> Generator:
    conn = None
    try:
        conn = psycopg2.connect(config.dsn)
        yield conn
    except psycopg2.OperationalError as e:
        logger.error("Database connection failed: %s", e)
        raise
    finally:
        if conn:
            conn.close()


def fetch_all(query: str, params: Optional[tuple] = None) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params or ())
            return [dict(row) for row in cur.fetchall()]
