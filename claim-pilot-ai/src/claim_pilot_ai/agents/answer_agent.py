import asyncio

from claim_pilot_ai.agents.heuristics import coverage_from_clause_keywords
from claim_pilot_ai.config import settings


async def compose_final_answer(
    state: dict,
    policy_result: dict,
    fraud_result: dict,
) -> dict:
    clauses = policy_result.get("clauses", [])
    citations = [
        {
            "document": c.get("document", "policy_document"),
            "page": c.get("page"),
            "clause_title": c.get("clause_title"),
            "text": c.get("clause_text"),
        }
        for c in clauses
    ]

    decision = policy_result.get("decision", "needs_review")
    confidence = float(policy_result.get("confidence", 0.5))
    reasoning = policy_result.get("reasoning", "Insufficient evidence.")

    if settings.dspy_bedrock_enabled:
        try:
            from claim_pilot_ai.dspy_modules.coverage import run_bedrock_coverage_judgment

            dspy_out = await asyncio.to_thread(
                run_bedrock_coverage_judgment,
                state.get("claim_description", ""),
                state.get("question", ""),
                policy_result,
                fraud_result,
            )
            decision = dspy_out["decision"]
            confidence = float(dspy_out["confidence"])
            reasoning = dspy_out["reasoning"]
        except Exception:
            fb = coverage_from_clause_keywords(clauses)
            decision = fb["decision"]
            confidence = float(fb["confidence"])
            reasoning = fb["reasoning"] + " (DSPy/Bedrock unavailable; heuristic fallback.)"

    return {
        "decision": decision,
        "confidence": confidence,
        "reasoning": reasoning,
        "citations": citations,
        "fraud_score": fraud_result.get("fraud_score"),
        "next_action": "Escalate to a human adjuster before issuing a final coverage decision.",
    }
