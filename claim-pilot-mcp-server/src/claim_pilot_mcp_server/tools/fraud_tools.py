async def calculate_fraud_score(claim_id: str):
    return {
        "claim_id": claim_id,
        "fraud_score": 0.27,
        "signals": ["No duplicate claim found", "Claim amount within expected range"],
    }
