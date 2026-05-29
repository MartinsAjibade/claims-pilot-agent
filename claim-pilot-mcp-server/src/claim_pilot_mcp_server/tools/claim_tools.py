async def get_claim_details(claim_id: str):
    return {
        "claim_id": claim_id,
        "claim_type": "auto",
        "amount": 4200,
        "status": "submitted",
    }
