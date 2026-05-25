from claim_pilot_ai.agents.planner_agent import plan_next_steps
from claim_pilot_ai.agents.policy_agent import analyze_policy_coverage
from claim_pilot_ai.agents.fraud_agent import analyze_fraud_risk
from claim_pilot_ai.agents.answer_agent import compose_final_answer


async def run_insurance_rag_workflow(state: dict) -> dict:
    """Minimal async workflow. Replace with LangGraph StateGraph when ready."""
    plan = await plan_next_steps(state)
    policy_result = await analyze_policy_coverage(state, plan)
    fraud_result = await analyze_fraud_risk(state, policy_result)
    return await compose_final_answer(state, policy_result, fraud_result)
