from claim_pilot_ai.agents.heuristics import coverage_from_clause_keywords


def test_heuristic_commercial_exclusion():
    clauses = [
        {
            "clause_title": "Commercial",
            "clause_text": "Coverage does not apply for paid delivery services.",
        }
    ]
    out = coverage_from_clause_keywords(clauses)
    assert out["decision"] == "not_covered"
    assert out["confidence"] >= 0.8


def test_heuristic_needs_review():
    clauses = [{"clause_title": "General", "clause_text": "Standard personal auto coverage."}]
    out = coverage_from_clause_keywords(clauses)
    assert out["decision"] == "needs_review"
