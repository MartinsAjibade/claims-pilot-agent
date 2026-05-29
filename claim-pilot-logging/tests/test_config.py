from claim_pilot_logging.config import LogConfig, LogLevel, OutputFormat


def test_default_config():
    config = LogConfig()
    assert config.service_name == "claim-pilot-service"
    assert config.log_level == LogLevel.INFO
    assert config.output_format == OutputFormat.JSON


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("SERVICE_NAME", "test-service")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    config = LogConfig.from_env()
    assert config.service_name == "test-service"
    assert config.log_level == LogLevel.DEBUG
