#!/usr/bin/env bash
set -euo pipefail

echo "=== Clickstream Pipeline Setup ==="

# Check prerequisites
command -v python3 >/dev/null 2>&1 || { echo "Requires Python 3.11+"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "Requires Docker"; exit 1; }

# Create virtual environment
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi

source .venv/bin/activate

# Install dependencies
pip install -e ".[dev,streaming]" --quiet
echo "✓ Dependencies installed"

# Copy env file if missing
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ .env created from .env.example"
fi

# Start infrastructure
docker compose up -d
echo "✓ Infrastructure started (Kafka, Zookeeper, PostgreSQL)"

echo ""
echo "Setup complete. Run:"
echo "  source .venv/bin/activate"
echo "  make producer    # Start event generator"
echo "  make streaming   # Start Spark Streaming job"
echo "  make api         # Start API server"
