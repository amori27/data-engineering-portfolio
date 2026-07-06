# Real-Time Clickstream Pipeline

End-to-end real-time data pipeline processing simulated web clickstream events through Kafka → Spark Structured Streaming → PostgreSQL, with a FastAPI serving layer.

## Architecture

```
Faker Producer → Kafka → Spark Streaming → PostgreSQL ← FastAPI API
```

- **Producer** — Generates realistic pageview events (Faker) and publishes to Kafka
- **Streaming** — Spark Structured Streaming reads from Kafka, aggregates pageviews in 1-minute windows, writes to PostgreSQL
- **API** — FastAPI endpoints to query raw events, top pages, and country breakdowns
- **Infrastructure** — All services run via Docker Compose

## Quick Start

```bash
# 1. Start infrastructure (Kafka + PostgreSQL)
make infra

# 2. Install Python dependencies
pip install -r producer/requirements.txt
pip install -r api/requirements.txt

# 3. Start the event producer
make producer

# 4. (In another terminal) Start Spark Streaming job
make streaming

# 5. (In another terminal) Start API server
make api
```

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /health` | Health check |
| `GET /api/pageviews/recent?limit=50` | Most recent pageviews |
| `GET /api/pageviews/top-pages?min_views=1` | Top pages by view count |
| `GET /api/pageviews/country-breakdown` | Views grouped by country |

## Project Structure

```
├── producer/          # Kafka event producer
│   └── main.py        # Generates and sends pageview events
├── streaming/         # Spark Structured Streaming
│   └── main.py        # Reads Kafka → aggregates → writes PostgreSQL
├── api/               # FastAPI serving layer
│   └── main.py        # REST API for querying analytics
├── config/            # Infrastructure config
│   ├── init.sql       # PostgreSQL schema
├── tests/             # Test suite
├── docker-compose.yml # Kafka, Zookeeper, PostgreSQL
└── Makefile           # Common commands
```

## Tech Stack

Python, Kafka, Spark Structured Streaming, PostgreSQL, FastAPI, Docker
