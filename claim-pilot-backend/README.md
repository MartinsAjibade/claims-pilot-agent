# Claim Pilot Backend

FastAPI gateway for insurance coverage analysis. Routes client requests to the AI service and returns structured coverage decisions.

## Architecture

![Claim Pilot platform architecture](docs/arch.png)

This service is the **FastAPI backend** in the application layer: REST APIs (including the agentic RAG coverage-check route), auth/session integration points, and the hop from clients to the AI orchestrator as shown in the diagram.

## API Endpoints

- `POST /api/v1/agentic-rag/coverage-check` — Submit a coverage check request
- `GET /health` — Health check

## Local Development

```bash
pip install -e ".[dev]"
make run        # Backend on port 9010
make test       # Run tests
make lint       # Run linter
```

Requires `claim-pilot-ai` running on port 9020.

## Configuration

Copy `env.example` to `.env`:

```
APP_NAME=Claim Pilot
ENVIRONMENT=dev
AI_SERVICE_URL=http://localhost:9020
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/claim_pilot
REDIS_URL=redis://localhost:6379/0
```

## Test Coverage Check

```bash
bash scripts/test_coverage_check.sh
```

## Docker

Build context is **this repository** (same pattern as [aims-api](https://github.com/aims-platform/aims-api)): `pip` resolves `claim-pilot-core` from GitHub. For **private** repos, set `GITHUB_TOKEN` in `.env` (loaded by the Makefile) or pass `--build-arg GITHUB_TOKEN=...`.

```bash
make docker-build
make docker-run
```

```bash
docker build --build-arg GITHUB_TOKEN="$GITHUB_TOKEN" -t claim-pilot-backend .
docker run -p 9010:9010 --env-file .env claim-pilot-backend
```

From the **INSURANCE-AUTOMATION** workspace, `docker compose up --build` uses each service directory as context and passes `GITHUB_TOKEN` from the workspace `.env`.

## Versioning

Calendar Versioning (CalVer): `YYYY.MM.PATCH`

## Maintainer

**Martins Ajibade**  

This repository is maintained for the **Claim Pilot Agent** platform.

- **Email:** [martinsajibade3@gmail.com]

For professional inquiries, security-sensitive reports, or questions about this component, please reach out via the address above.
