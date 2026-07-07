# Clickstream Analytics Pipeline

Real-time web analytics pipeline: Kafka producer generates 10+ pageview events/second, Spark Structured Streaming aggregates 1-minute windows, PostgreSQL stores raw + aggregated data, FastAPI serves paginated REST endpoints.

## Quick Start

```bash
make setup          # install deps + start Docker infra
make producer       # (terminal 1) event generator
make streaming      # (terminal 2) Spark streaming
make api            # (terminal 3) FastAPI
```

## API

```bash
curl http://localhost:8000/api/pageviews/recent?limit=10
curl http://localhost:8000/api/pageviews/top-pages
curl http://localhost:8000/api/pageviews/country-breakdown
curl http://localhost:8000/api/pageviews/country/US
```

## Architecture

```
Faker Producer → Kafka Broker → Spark Streaming → PostgreSQL → FastAPI → Client
```

| Component | Role |
|---|---|
| Python + confluent-kafka Producer | Generates realistic pageview events |
| Kafka 3.6 | Buffers and distributes events |
| Spark Structured Streaming | Windowed aggregation (1-min) |
| PostgreSQL 16 | Raw events + aggregated metrics |
| FastAPI | REST endpoints with pagination and country filtering |

## Configuration

All via environment variables (`.env.example` provided): Kafka broker, topic name, events per second, PostgreSQL host, API port.

## License

MIT
