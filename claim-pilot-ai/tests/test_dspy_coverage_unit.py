from types import SimpleNamespace

from claim_pilot_ai.dspy_modules import coverage as coverage_mod


def test_policy_evidence_from_results_formats_clauses():
    text = coverage_mod.policy_evidence_from_results(
        {
            "clauses": [
                {"clause_title": "A", "clause_text": "alpha"},
                {"clause_title": "B", "clause_text": "beta"},
            ]
        }
    )
    assert "## A" in text and "alpha" in text
    assert "## B" in text


def test_run_bedrock_coverage_judgment_uses_program(monkeypatch):
    monkeypatch.setattr(coverage_mod, "_ensure_dspy_lm", lambda: None)

    class FakeProg:
        def __call__(self, **kwargs):
            return SimpleNamespace(
                decision="covered",
                confidence="0.92",
                reasoning="Policy text supports coverage.",
            )

    monkeypatch.setattr(coverage_mod, "_get_program", lambda: FakeProg())

    out = coverage_mod.run_bedrock_coverage_judgment(
        "Minor fender bender in a parking lot.",
        "Is it covered?",
        {"clauses": [{"clause_title": "Collision", "clause_text": "Covers collision damage."}]},
        {"fraud_score": 0.1},
    )
    assert out["decision"] == "covered"
    assert out["confidence"] == 0.92
    assert "supports" in out["reasoning"]
