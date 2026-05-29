from claim_pilot_logging.logger import Logger, get_logger


def test_get_logger():
    logger = get_logger("test")
    assert isinstance(logger, Logger)
    assert logger.name == "test"


def test_get_logger_cached():
    logger1 = get_logger("cached_test")
    logger2 = get_logger("cached_test")
    assert logger1 is logger2
