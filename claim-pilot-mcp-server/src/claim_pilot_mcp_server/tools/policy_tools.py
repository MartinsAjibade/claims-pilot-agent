async def search_policy_clauses(policy_id: str, query: str):
    # Replace with Bedrock Knowledge Base retrieval.
    return [
        {
            "policy_id": policy_id,
            "document": "sample_auto_policy.pdf",
            "page": 12,
            "clause_title": "Commercial Use Exclusion",
            "clause_text": "Coverage does not apply when the vehicle is used for paid delivery services or other commercial use.",
            "confidence": 0.91,
        }
    ]
