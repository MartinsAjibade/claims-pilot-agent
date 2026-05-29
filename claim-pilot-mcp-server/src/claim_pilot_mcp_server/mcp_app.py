from fastmcp import FastMCP

from claim_pilot_mcp_server.tools.claim_tools import get_claim_details
from claim_pilot_mcp_server.tools.fraud_tools import calculate_fraud_score
from claim_pilot_mcp_server.tools.policy_tools import search_policy_clauses

mcp = FastMCP("insurance-mcp-server")


@mcp.tool
async def policy_search(policy_id: str, query: str):
    """Search policy clauses by policy ID and natural-language query."""
    return await search_policy_clauses(policy_id, query)


@mcp.tool
async def claim_lookup(claim_id: str):
    """Return structured claim details for a given claim ID."""
    return await get_claim_details(claim_id)


@mcp.tool
async def fraud_score(claim_id: str):
    """Compute a fraud risk score and supporting signals for a claim."""
    return await calculate_fraud_score(claim_id)
