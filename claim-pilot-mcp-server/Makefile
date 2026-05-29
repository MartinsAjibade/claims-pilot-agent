# ═══════════════════════════════════════════════════════════════════════════════
# Claim Pilot MCP Server - Makefile
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help install test test-cov lint format build clean publish run docker docker-build docker-run

.DEFAULT_GOAL := help

-include .env
export

IMAGE_NAME ?= claim-pilot-mcp-server
ENV_FILE   ?= $(shell test -f .env && echo .env || echo env.example)

help:
	@echo ""
	@echo "Claim Pilot MCP Server - Development Commands"
	@echo "═══════════════════════════════════════════════"
	@echo ""
	@echo "  make install    Install package in development mode"
	@echo "  make test       Run tests"
	@echo "  make test-cov   Run tests with coverage"
	@echo "  make lint       Run linter"
	@echo "  make format     Format code"
	@echo "  make build      Build package"
	@echo "  make clean      Clean build artifacts"
	@echo "  make run        Run HTTP API server (port 8001)"
	@echo "  make docker-build Build image (GITHUB_TOKEN from .env for private deps)"
	@echo "  make docker-run   Run container on port 8001"
	@echo "  make docker       docker-build then docker-run"
	@echo ""

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=claim_pilot_mcp_server --cov-report=html
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
	uvicorn claim_pilot_mcp_server.http_api:app --reload --port 8001

docker-build:
	docker build --build-arg GITHUB_TOKEN=$(GITHUB_TOKEN) -t $(IMAGE_NAME) .

docker-run:
	docker run --rm --name claim-pilot-mcp \
		-p 9030:8001 \
		--env-file $(ENV_FILE) \
		$(IMAGE_NAME)

docker: docker-build docker-run
