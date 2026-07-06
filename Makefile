.PHONY: infra up down producer streaming api test clean

infra:
	docker compose up -d

up: infra
	@echo "Kafka, Zookeeper, PostgreSQL started."

down:
	docker compose down

producer:
	python -m producer.main

streaming:
	spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,org.postgresql:postgresql:42.7.3 streaming/main.py

api:
	uvicorn api.main:app --reload --port 8000

test:
	python -m pytest tests/ -v

clean:
	docker compose down -v
	rm -rf __pycache__ */__pycache__ .pytest_cache
