# ═══════════════════════════════════════════════════════════════════════════════
# Claim Pilot Frontend - Makefile
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help install dev build start lint format clean

.DEFAULT_GOAL := help

help:
	@echo ""
	@echo "Claim Pilot Frontend - Development Commands"
	@echo "═══════════════════════════════════════════"
	@echo ""
	@echo "  make install    Install dependencies"
	@echo "  make dev        Run development server"
	@echo "  make build      Production build"
	@echo "  make start      Start production server"
	@echo "  make lint       Run ESLint"
	@echo "  make format     Format code with Prettier"
	@echo "  make clean      Clean build artifacts"
	@echo ""

install:
	npm ci

dev:
	npm run dev

build:
	npm run build

start:
	npm run start

lint:
	npm run lint

format:
	npx prettier --write "src/**/*.{ts,tsx,css}"

clean:
	rm -rf .next node_modules
