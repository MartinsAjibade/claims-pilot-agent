from claim_pilot_ai.config import Settings


def test_default_settings():
    s = Settings()
    assert s.environment == "dev"
    assert s.aws_region == "us-east-1"
    assert s.mcp_server_url == "http://localhost:8001"
    assert s.docling_enabled is False
    assert s.dspy_bedrock_enabled is False
