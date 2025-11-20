# Makefile for Flask Task Manager API

.PHONY: help install dev-install run test coverage clean seed format lint

help:
	@echo "Flask Task Manager API - Makefile Commands"
	@echo ""
	@echo "install        - Install production dependencies"
	@echo "dev-install    - Install development dependencies"
	@echo "run            - Run the Flask application"
	@echo "test           - Run tests"
	@echo "coverage       - Run tests with coverage report"
	@echo "clean          - Remove build artifacts and cache files"
	@echo "seed           - Seed the database with sample data"
	@echo "format         - Format code with Black"
	@echo "lint           - Lint code with Ruff"

install:
	uv pip install -e .

dev-install:
	uv pip install -e ".[dev]"

run:
	uv run python -m app.main

test:
	uv run pytest

coverage:
	uv run pytest --cov=app --cov-report=html --cov-report=term

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f tasks.db

seed:
	uv run python init_db.py seed

format:
	uv run black app/ tests/

lint:
	uv run ruff check app/ tests/
