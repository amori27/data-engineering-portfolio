import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.config import config
from src.api.routes import router

app = FastAPI(
    title="Clickstream Analytics API",
    version="1.0.0",
    description="Real-time clickstream analytics powered by Kafka, Spark Streaming, and PostgreSQL",
    contact={"name": "Ameer Asaad", "url": "https://github.com/amori27"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    logging.basicConfig(
        level=getattr(logging, config.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    uvicorn.run(
        "src.api.main:app",
        host=config.host,
        port=config.port,
        log_level=config.log_level,
        reload=True,
    )
