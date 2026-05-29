from fastapi import FastAPI

from claim_pilot_mcp_server.mcp_app import mcp
from claim_pilot_mcp_server.tools.claim_tools import get_claim_details
from claim_pilot_mcp_server.tools.fraud_tools import calculate_fraud_score
from claim_pilot_mcp_server.tools.policy_tools import search_policy_clauses

_mcp_http = mcp.http_app(path="/")

app = FastAPI(
    title="Claim Pilot MCP HTTP API",
    version="0.1.0",
    lifespan=_mcp_http.lifespan,
)


@app.post("/tools/policy-search")
async def policy_search(policy_id: str, query: str):
    return await search_policy_clauses(policy_id, query)


@app.post("/tools/fraud-score")
async def fraud_score(claim_id: str):
    return await calculate_fraud_score(claim_id)


@app.post("/tools/claim-lookup")
async def claim_lookup(claim_id: str):
    return await get_claim_details(claim_id)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.mount("/mcp", _mcp_http)
