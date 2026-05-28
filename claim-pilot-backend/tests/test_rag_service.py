from claim_pilot_backend.app.schemas.agentic_rag import CoverageCheckRequest, CoverageCheckResponse


def test_coverage_check_request_validation():
    req = CoverageCheckRequest(
        claim_description="Customer had an accident while delivering food.",
        policy_id="AUTO-12345",
    )
    assert req.policy_id == "AUTO-12345"
    assert req.question == "Is this claim covered?"


def test_coverage_check_response():
    resp = CoverageCheckResponse(
        decision="not_covered",
        confidence=0.82,
        reasoning="Commercial use excluded.",
        citations=[],
        fraud_score=0.27,
        next_action="Escalate to adjuster.",
    )
    assert resp.decision == "not_covered"
    assert resp.confidence == 0.82
