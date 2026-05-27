
# ═══════════════════════════════════════════════════════════════════════════════
# Claim Pilot AI - Makefile
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help install install-eval test test-cov lint format build clean publish run eval-ragas eval-deepeval \
	docker docker-build docker-run

.DEFAULT_GOAL := help

-include .env
export

IMAGE_NAME ?= claim-pilot-ai
ENV_FILE   ?= $(shell test -f .env && echo .env || echo env.example)

help:
	@echo ""
	@echo "Claim Pilot AI - Development Commands"
	@echo "═══════════════════════════════════════════"
	@echo ""
	@echo "  make install      Install package in development mode"
	@echo "  make install-eval Install with Ragas + DeepEval extras"
	@echo "  make test         Run tests"
	@echo "  make test-cov   Run tests with coverage"
	@echo "  make lint       Run linter"
	@echo "  make format     Format code"
	@echo "  make build      Build package"
	@echo "  make clean      Clean build artifacts"
	@echo "  make run          Run AI service"
	@echo "  make eval-ragas   Run Ragas on eval/golden_samples.jsonl"
	@echo "  make eval-deepeval Run DeepEval on eval/golden_samples.jsonl"
	@echo "  make docker-build Build image (GITHUB_TOKEN from .env for private deps)"
	@echo "  make docker-run   Run container on port 9020"
	@echo "  make docker       docker-build then docker-run"
	@echo ""

install:
	pip install -e ".[dev]"

install-eval:
	pip install -e ".[dev,eval]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=claim_pilot_ai --cov-report=html
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
	uvicorn claim_pilot_ai.api.main:app --reload --port 9020

eval-ragas:
	python eval/run_ragas_eval.py

eval-deepeval:
	python eval/run_deepeval_eval.py

docker-build:
	docker build --build-arg GITHUB_TOKEN=$(GITHUB_TOKEN) -t $(IMAGE_NAME) .

docker-run:
	docker run --rm --name claim-pilot-ai \
		-p 9020:9020 \
		--add-host=host.docker.internal:host-gateway \
		--env-file $(ENV_FILE) \
		$(IMAGE_NAME)

docker: docker-build docker-run
