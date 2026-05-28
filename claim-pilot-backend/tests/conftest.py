import pytest


@pytest.fixture
def sample_coverage_request():
    return {
        "claim_description": "Customer had an accident while delivering food using a personal vehicle.",
        "policy_id": "AUTO-12345",
        "claim_id": "CLM-1001",
        "question": "Is this claim covered?",
    }
