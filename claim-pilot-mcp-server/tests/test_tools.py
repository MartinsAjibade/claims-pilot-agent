from claim_pilot_mcp_server.tools.policy_tools import search_policy_clauses
from claim_pilot_mcp_server.tools.claim_tools import get_claim_details
from claim_pilot_mcp_server.tools.fraud_tools import calculate_fraud_score


async def test_search_policy_clauses(sample_policy_id):
    result = await search_policy_clauses(sample_policy_id, "commercial use")
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["policy_id"] == sample_policy_id


async def test_get_claim_details(sample_claim_id):
    result = await get_claim_details(sample_claim_id)
    assert result["claim_id"] == sample_claim_id
    assert "claim_type" in result
    assert "amount" in result


async def test_calculate_fraud_score(sample_claim_id):
    result = await calculate_fraud_score(sample_claim_id)
    assert result["claim_id"] == sample_claim_id
    assert "fraud_score" in result
    assert 0 <= result["fraud_score"] <= 1
