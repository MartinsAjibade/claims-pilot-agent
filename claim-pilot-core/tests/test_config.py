from claim_pilot_backend.app.core.config import Settings


def test_default_settings():
    s = Settings()
    assert s.app_name == "Claim Pilot"
    assert s.environment == "dev"
    assert s.debug is False
    assert s.log_level == "INFO"
    assert s.ai_service_url == "http://localhost:9020"
