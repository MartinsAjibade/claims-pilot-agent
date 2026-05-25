"""DSPy program for coverage judgment; uses Amazon Bedrock via LiteLLM when configured."""

from __future__ import annotations

import json
import re
import threading
from typing import Any

import dspy

from claim_pilot_ai.config import settings

_lock = threading.Lock()
_lm_configured = False

_program: Any = None


def _ensure_dspy_lm() -> None:
    global _lm_configured
    with _lock:
        if _lm_configured:
            return
        model = f"bedrock/{settings.bedrock_model_id}"
        lm = dspy.LM(
            model,
            max_tokens=settings.dspy_max_tokens,
            aws_region_name=settings.aws_region,
        )
        dspy.configure(lm=lm)
        _lm_configured = True


class CoverageReasoningSignature(dspy.Signature):
    """Insurance coverage analyst: conclude only from supplied policy evidence and risk context."""

    claim_description: str = dspy.InputField()
    question: str = dspy.InputField()
    policy_evidence: str = dspy.InputField()
    fraud_and_risk_context: str = dspy.InputField()

    decision: str = dspy.OutputField(
        desc="Exactly one of: covered, not_covered, needs_review, unknown",
    )
    confidence: str = dspy.OutputField(desc="Single number from 0 to 1, e.g. 0.78")
    reasoning: str = dspy.OutputField(desc="Brief explanation grounded in the evidence")


class CoverageReasoningProgram(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self._predict = dspy.ChainOfThought(CoverageReasoningSignature)

    def forward(
        self,
        claim_description: str,
        question: str,
        policy_evidence: str,
        fraud_and_risk_context: str,
    ):
        return self._predict(
            claim_description=claim_description,
            question=question,
            policy_evidence=policy_evidence,
            fraud_and_risk_context=fraud_and_risk_context,
        )


def _get_program() -> CoverageReasoningProgram:
    global _program
    if _program is None:
        _program = CoverageReasoningProgram()
    return _program


def _parse_confidence(raw: str) -> float:
    m = re.search(r"\b0?\.\d+\b|\b1\.0*\b|\b0\b|\b1\b", (raw or "").replace(",", "."))
    if not m:
        return 0.5
    try:
        return max(0.0, min(1.0, float(m.group(0))))
    except ValueError:
        return 0.5


def _normalize_decision(raw: str) -> str:
    s = (raw or "").lower()
    if "not_covered" in s or "not covered" in s or "excluded" in s or "denied" in s:
        return "not_covered"
    if "needs_review" in s or "need review" in s or "unclear" in s:
        return "needs_review"
    if "unknown" in s:
        return "unknown"
    if "covered" in s and "not" not in s.split("covered", 1)[0][-12:]:
        return "covered"
    return "needs_review"


def policy_evidence_from_results(policy_result: dict) -> str:
    parts: list[str] = []
    for c in policy_result.get("clauses") or []:
        title = c.get("clause_title") or ""
        text = c.get("clause_text") or ""
        parts.append(f"## {title}\n{text}")
    return "\n\n".join(parts) if parts else "(no clauses retrieved)"


def fraud_context_str(fraud_result: dict) -> str:
    try:
        return json.dumps(fraud_result, indent=2, default=str)
    except TypeError:
        return str(fraud_result)


def run_bedrock_coverage_judgment(
    claim_description: str,
    question: str,
    policy_result: dict,
    fraud_result: dict,
) -> dict[str, Any]:
    """
    Run the DSPy Chain-of-Thought program against Bedrock. Caller should catch errors
    and fall back to heuristics when credentials or the model are unavailable.
    """
    _ensure_dspy_lm()
    prog = _get_program()
    evidence = policy_evidence_from_results(policy_result)
    fraud_s = fraud_context_str(fraud_result)
    out = prog(
        claim_description=claim_description,
        question=question,
        policy_evidence=evidence,
        fraud_and_risk_context=fraud_s,
    )
    decision = _normalize_decision(str(getattr(out, "decision", "")))
    confidence = _parse_confidence(str(getattr(out, "confidence", "")))
    reasoning = str(getattr(out, "reasoning", "") or "").strip()
    if not reasoning:
        reasoning = "Model returned an empty reasoning string."
    return {"decision": decision, "confidence": confidence, "reasoning": reasoning}
