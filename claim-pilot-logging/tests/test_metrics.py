from claim_pilot_logging.metrics import MetricType, Timer


def test_metric_type_values():
    assert MetricType.COUNTER == "counter"
    assert MetricType.TIMER == "timer"


def test_timer():
    timer = Timer("test.operation", auto_log=False)
    timer.start()
    timer.stop()
    assert timer.duration_ms > 0
