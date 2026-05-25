async def plan_next_steps(state: dict) -> dict:
    return {
        "needs_policy_search": True,
        "needs_claim_lookup": bool(state.get("claim_id")),
        "needs_fraud_check": True,
        "search_query": f"{state.get('question')} {state.get('claim_description')}",
    }
