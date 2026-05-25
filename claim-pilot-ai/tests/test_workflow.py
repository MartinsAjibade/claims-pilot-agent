from claim_pilot_ai.agents.planner_agent import plan_next_steps
from claim_pilot_ai.agents.answer_agent import compose_final_answer


async def test_plan_next_steps(sample_state):
    plan = await plan_next_steps(sample_state)
    assert plan["needs_policy_search"] is True
    assert plan["needs_fraud_check"] is True
    assert plan["needs_claim_lookup"] is True
    assert "search_query" in plan


async def test_compose_final_answer(sample_state):
    policy_result = {
        "decision": "not_covered",
        "confidence": 0.82,
        "reasoning": "Commercial use excluded.",
        "clauses": [
            {
                "document": "policy.pdf",
                "page": 12,
                "clause_title": "Commercial Use",
                "clause_text": "Excluded.",
            }
        ],
    }
    fraud_result = {"fraud_score": 0.27}
    result = await compose_final_answer(sample_state, policy_result, fraud_result)
    assert result["decision"] == "not_covered"
    assert result["fraud_score"] == 0.27
    assert len(result["citations"]) == 1
