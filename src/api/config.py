import os
from dataclasses import dataclass, field


@dataclass
class APIConfig:
    host: str = field(default_factory=lambda: os.getenv("API_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("API_PORT", "8000")))
    log_level: str = field(default_factory=lambda: os.getenv("API_LOG_LEVEL", "info"))
    pg_host: str = field(default_factory=lambda: os.getenv("POSTGRES_HOST", "localhost"))
    pg_port: int = field(default_factory=lambda: int(os.getenv("POSTGRES_PORT", "5432")))
    pg_db: str = field(default_factory=lambda: os.getenv("POSTGRES_DB", "analytics"))
    pg_user: str = field(default_factory=lambda: os.getenv("POSTGRES_USER", "user"))
    pg_password: str = field(default_factory=lambda: os.getenv("POSTGRES_PASSWORD", "pass"))

    @property
    def dsn(self) -> str:
        return (
            f"dbname={self.pg_db} user={self.pg_user} "
            f"password={self.pg_password} host={self.pg_host} port={self.pg_port}"
        )


config = APIConfig()
