# Contributing

Thank you for considering contributing to the Clickstream Pipeline. This document outlines the guidelines for contributing.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/amori27/data-engineering-portfolio.git
cd data-engineering-portfolio

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Start infrastructure
docker compose up -d

# Run tests
pytest
```

## Code Standards

- **Python**: 3.11+, type hints required, 100 char line limit
- **Formatting**: `ruff format` before committing
- **Linting**: `ruff check` must pass
- **Typing**: `mypy --strict src/` must pass

## Pull Request Process

1. Create a feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Open a pull request with a clear description

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add windowed aggregation
fix: handle null referrer in schema
docs: update architecture diagram
test: add producer edge cases
ci: add ruff lint step
```

## Project Structure

```
src/            Source code
tests/          Test suite
config/         Configuration files
docs/           Documentation
scripts/        Utility scripts
```
