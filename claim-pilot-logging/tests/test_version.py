from claim_pilot_logging import __version__


def test_version():
    assert __version__ == "2026.05.1"
    parts = __version__.split(".")
    assert len(parts) == 3
