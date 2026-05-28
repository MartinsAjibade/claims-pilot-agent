# ═══════════════════════════════════════════════════════════════════════════════
# Claim Pilot Backend - Makefile
# ═══════════════════════════════════════════════════════════════════════════════

IMAGE_NAME ?= claim-pilot-backend
ENV_FILE   ?= $(shell test -f .env && echo .env || echo env.example)

.PHONY: help install test test-cov lint format build clean publish run docker docker-build docker-run

.DEFAULT_GOAL := help

-include .env
export

help:
	@echo ""
	@echo "Claim Pilot Backend - Development Commands"
	@echo "═══════════════════════════════════════════"
	@echo ""
	@echo "  make install      Install package in development mode"
	@echo "  make test         Run tests"
	@echo "  make test-cov     Run tests with coverage"
	@echo "  make lint         Run linter"
	@echo "  make format       Format code"
	@echo "  make build        Build Python package (wheel/sdist)"
	@echo "  make clean        Clean build artifacts"
	@echo "  make run          Run backend with uvicorn (dev, port 9010)"
	@echo ""
	@echo "  make docker-build Build image (GITHUB_TOKEN from .env for private claim-pilot-core)"
	@echo "  make docker-run   Run container (port 9010, env from .env or env.example)"
	@echo "  make docker       docker-build then docker-run"
	@echo ""
	@echo "  Docker: set AI_SERVICE_URL=http://host.docker.internal:9020 in .env when"
	@echo "  the AI service runs on your host machine (not inside the same compose stack)."
	@echo ""

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=claim_pilot_backend --cov-report=html
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

run:
	uvicorn claim_pilot_backend.app.main:app --reload --port 9010

docker-build:
	docker build --build-arg GITHUB_TOKEN=$(GITHUB_TOKEN) -t $(IMAGE_NAME) .

docker-run:
	docker run --rm --name claim-pilot-backend \
		-p 9010:9010 \
		--add-host=host.docker.internal:host-gateway \
		--env-file $(ENV_FILE) \
		$(IMAGE_NAME)

docker: docker-build docker-run
