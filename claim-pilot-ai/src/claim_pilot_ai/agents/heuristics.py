"""Keyword fallbacks when DSPy/Bedrock is unavailable or returns no usable signal."""


def coverage_from_clause_keywords(clauses: list[dict]) -> dict:
    text = " ".join([c.get("clause_text", "") for c in clauses]).lower()
    if "commercial use" in text or "paid delivery" in text:
        return {
            "decision": "not_covered",
            "confidence": 0.82,
            "reasoning": (
                "Relevant policy clauses indicate commercial or paid delivery use may be excluded."
            ),
        }
    return {
        "decision": "needs_review",
        "confidence": 0.55,
        "reasoning": "Policy clauses were retrieved, but coverage requires human review.",
    }
