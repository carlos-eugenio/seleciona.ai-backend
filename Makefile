# Seleciona AI Backend - Makefile

.PHONY: help install dev prod test lint format clean setup

# Default target
help:
	@echo "Seleciona AI Backend - Available Commands:"
	@echo ""
	@echo "  setup     - Initial project setup"
	@echo "  install   - Install dependencies"
	@echo "  dev       - Run development server"
	@echo "  prod      - Run production server"
	@echo "  test      - Run tests"
	@echo "  lint      - Run linting"
	@echo "  format    - Format code"
	@echo "  clean     - Clean temporary files"
	@echo "  migrate   - Run database migrations"
	@echo "  shell     - Open Python shell"
	@echo "  logs      - Show application logs"

# Initial setup
setup:
	@echo "Setting up project..."
	python -m venv venv
	@echo "Virtual environment created. Please activate it and run 'make install'"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "Dependencies installed successfully"

# Development server
dev:
	@echo "Starting development server..."
	python main.py

# Production server
prod:
	@echo "Starting production server..."
	uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Run tests
test:
	@echo "Running tests..."
	python test_api.py

# Linting
lint:
	@echo "Running linting..."
	flake8 app/ main.py test_api.py
	black --check app/ main.py test_api.py
	isort --check-only app/ main.py test_api.py

# Format code
format:
	@echo "Formatting code..."
	black app/ main.py test_api.py
	isort app/ main.py test_api.py

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".mypy_cache" -delete
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

# Database migrations
migrate:
	@echo "Running database migrations..."
	alembic upgrade head

# Create new migration
migration:
	@echo "Creating new migration..."
	alembic revision --autogenerate -m "$(msg)"

# Python shell
shell:
	@echo "Opening Python shell..."
	python -c "from app.database import SessionLocal; from app.models import *; db = SessionLocal(); print('Database session ready as db')"

# Show logs
logs:
	@echo "Showing application logs..."
	tail -f logs/app.log 2>/dev/null || echo "No log file found"

# Database commands
db-reset:
	@echo "Resetting database..."
	alembic downgrade base
	alembic upgrade head

# Security check
security:
	@echo "Running security checks..."
	safety check
	bandit -r app/ -f json -o bandit-report.json

# Pre-commit hooks
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install

pre-commit-run:
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files
