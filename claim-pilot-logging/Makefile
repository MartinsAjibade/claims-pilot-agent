# ═══════════════════════════════════════════════════════════════════════════════
# Claim Pilot Logging - Makefile
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help install test test-cov lint format build clean publish

.DEFAULT_GOAL := help

help:
	@echo ""
	@echo "Claim Pilot Logging - Development Commands"
	@echo "═══════════════════════════════════════════"
	@echo ""
	@echo "  make install    Install package in development mode"
	@echo "  make test       Run tests"
	@echo "  make test-cov   Run tests with coverage"
	@echo "  make lint       Run linter"
	@echo "  make format     Format code"
	@echo "  make build      Build package"
	@echo "  make clean      Clean build artifacts"
	@echo ""

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=claim_pilot_logging --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/
	ruff check --fix src/ tests/

build: clean
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true

publish: build
	@echo ""
	@echo "Package built! To publish:"
	@echo "  1. Create a git tag: git tag v2026.05.x"
	@echo "  2. Push the tag: git push origin v2026.05.x"
	@echo "  3. GitHub Actions will create a release"
	@echo ""
