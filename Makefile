.PHONY: infra up down producer streaming api test lint format clean install setup

## Infrastructure
infra:
	docker compose up -d

up: infra
	@echo "✓ Kafka, Zookeeper, PostgreSQL started"

down:
	docker compose down -v

## Application
producer:
	python -m src.producer.main

streaming:
	spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,org.postgresql:postgresql:42.7.3 src/streaming/main.py

api:
	python -m src.api.main

## Quality
test:
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	ruff check src/ tests/
	ruff format --check src/ tests/

format:
	ruff format src/ tests/

typecheck:
	mypy --strict src/ --ignore-missing-imports

## Setup
install:
	pip install -e ".[dev,streaming]"

setup: install infra
	@echo "✓ Setup complete"

## Cleanup
clean:
	docker compose down -v
	rm -rf __pycache__ src/**/__pycache__ tests/__pycache__ .pytest_cache
	rm -rf logs/*.log
	@echo "✓ Cleaned"
