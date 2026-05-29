# Claim Pilot MCP Server

Insurance tools exposed via MCP (Model Context Protocol) and HTTP API.

## Architecture

![Claim Pilot platform architecture](docs/arch.png)

This service is the **MCP Server** tier: it exposes tools (policy search, claim lookup, fraud score, etc.) that the orchestrator agents call. The diagram shows integrations from MCP tools to operational systems and data stores.

## Tools

- **policy_search** - Search policy clauses by policy ID and query
- **claim_lookup** - Get claim details by claim ID
- **fraud_score** - Calculate fraud score for a claim

Tools are registered on a **[FastMCP](https://gofastmcp.com)** server (`claim_pilot_mcp_server.mcp_app:mcp`). The same implementations power both transports below.

## Local Development

```bash
pip install -e ".[dev]"
make run        # HTTP API on port 8001
make test       # Run tests
make lint       # Run linter
```

## HTTP API

`make run` starts **FastAPI** with:

- **Legacy REST helpers** (used by Claim Pilot AI today): `POST /tools/...` with query parameters
- **MCP over HTTP**: FastMCP’s ASGI app is mounted at **`/mcp`** (for example `http://localhost:8001/mcp` for MCP clients that support streamable HTTP)

```bash
# Policy search
curl -X POST "http://localhost:8001/tools/policy-search?policy_id=AUTO-12345&query=commercial+use"

# Fraud score
curl -X POST "http://localhost:8001/tools/fraud-score?claim_id=CLM-1001"

# Claim lookup
curl -X POST "http://localhost:8001/tools/claim-lookup?claim_id=CLM-1001"

# Health check
curl http://localhost:8001/health
```

## MCP Server (stdio)

```bash
python -m claim_pilot_mcp_server.server
```

Or with the FastMCP CLI (stdio transport):

```bash
fastmcp run claim_pilot_mcp_server.mcp_app:mcp
```

## Docker

Private `git+https` dependencies need a PAT as a build-arg (see `Makefile` / `.env`).

```bash
docker build --build-arg GITHUB_TOKEN="$GITHUB_TOKEN" -t claim-pilot-mcp-server .
docker run -p 8001:8001 --env-file .env claim-pilot-mcp-server
```

## Versioning

Calendar Versioning (CalVer): `YYYY.MM.PATCH`

```bash
# Release
git tag v2026.05.1
git push origin v2026.05.1
```

## Maintainer

**Justin Weber** — Blue Lambda Technologies  

This repository is maintained for the **Claim Pilot** platform (Blue Lambda University).

- **Email:** [justin.weber@bluelambdatechnologies.com](mailto:justin.weber@bluelambdatechnologies.com)

For professional inquiries, security-sensitive reports, or questions about this component, please reach out via the address above.
