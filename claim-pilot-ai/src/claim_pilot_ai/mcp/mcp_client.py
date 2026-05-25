import httpx
from claim_pilot_ai.config import settings


async def search_policy_clauses(policy_id: str, query: str):
    async with httpx.AsyncClient(base_url=settings.mcp_server_url) as client:
        response = await client.post(
            "/tools/policy-search",
            params={"policy_id": policy_id, "query": query},
        )
        response.raise_for_status()
        return response.json()


async def calculate_fraud_score(claim_id: str):
    async with httpx.AsyncClient(base_url=settings.mcp_server_url) as client:
        response = await client.post(
            "/tools/fraud-score",
            params={"claim_id": claim_id},
        )
        response.raise_for_status()
        return response.json()
