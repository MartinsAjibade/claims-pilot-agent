from claim_pilot_logging.context import (
    LogContext,
    bind_context,
    clear_context,
    get_context,
    get_correlation_id,
    new_correlation_id,
)


def test_correlation_id():
    cid = new_correlation_id()
    assert len(cid) == 36  # UUID format


def test_bind_and_get_context():
    clear_context()
    bind_context(claim_id="CLM-001")
    ctx = get_context()
    assert ctx["claim_id"] == "CLM-001"
    clear_context()


def test_log_context_manager():
    clear_context()
    with LogContext(policy_id="AUTO-123"):
        ctx = get_context()
        assert ctx["policy_id"] == "AUTO-123"
    ctx = get_context()
    assert "policy_id" not in ctx


def test_log_context_request():
    clear_context()
    with LogContext.request(claim_id="CLM-002"):
        cid = get_correlation_id()
        assert cid is not None
        assert len(cid) == 36
