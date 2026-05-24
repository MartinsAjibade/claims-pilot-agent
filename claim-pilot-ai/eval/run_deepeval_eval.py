#!/usr/bin/env python3
"""
Run DeepEval metrics on golden samples using ``deepeval.models.LiteLLMModel`` (Bedrock).

Requires: ``pip install -e ".[eval]"`` and AWS credentials for Bedrock.

Usage::

    python eval/run_deepeval_eval.py
    EVAL_LLM_MODEL=bedrock/anthropic.claude-3-haiku-20240307-v1:0 python eval/run_deepeval_eval.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "eval" / "golden_samples.jsonl"


def main() -> int:
    try:
        from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
        from deepeval.models import LiteLLMModel
        from deepeval.test_case import LLMTestCase
    except ImportError:
        print("Install eval extras: pip install -e '.[eval]'", file=sys.stderr)
        return 1

    if not GOLDEN.is_file():
        print(f"Missing {GOLDEN}", file=sys.stderr)
        return 1

    sys.path.insert(0, str(ROOT / "src"))
    from claim_pilot_ai.config import settings

    model_id = os.environ.get(
        "EVAL_LLM_MODEL",
        f"bedrock/{settings.bedrock_model_id}",
    )
    os.environ.setdefault("AWS_DEFAULT_REGION", settings.aws_region)
    model = LiteLLMModel(model=model_id, temperature=0.0)

    faith = FaithfulnessMetric(model=model, include_reason=False)
    relevancy = AnswerRelevancyMetric(model=model, include_reason=False)

    with GOLDEN.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            case = LLMTestCase(
                input=row["question"],
                actual_output=row["answer"],
                retrieval_context=[str(c) for c in (row.get("contexts") or [])],
                expected_output=row.get("ground_truth") or None,
            )
            faith.measure(case)
            relevancy.measure(case)
            print(
                json.dumps(
                    {
                        "question": row["question"][:80],
                        "faithfulness": faith.score,
                        "answer_relevancy": relevancy.score,
                    }
                )
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
