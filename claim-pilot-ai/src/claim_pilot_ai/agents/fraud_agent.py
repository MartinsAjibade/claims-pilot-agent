from claim_pilot_ai.mcp.mcp_client import calculate_fraud_score


async def analyze_fraud_risk(state: dict, policy_result: dict) -> dict:
    if not state.get("claim_id"):
        return {"fraud_score": 0.2, "signals": ["No historical claim ID provided for deeper analysis."]}
    return await calculate_fraud_score(state["claim_id"])
