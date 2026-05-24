#!/usr/bin/env python3
"""
Run Ragas metrics on ``eval/golden_samples.jsonl`` using LiteLLM via LangChain.

Requires: ``pip install -e ".[eval]"`` and AWS credentials with ``bedrock:InvokeModel``.

Each JSON line maps to Ragas fields: ``user_input``, ``retrieved_contexts``,
``response``, and ``reference``.

Usage::

    python eval/run_ragas_eval.py
    EVAL_LLM_MODEL=bedrock/anthropic.claude-3-haiku-20240307-v1:0 python eval/run_ragas_eval.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "eval" / "golden_samples.jsonl"


def _load_evaluation_rows() -> list[dict]:
    rows: list[dict] = []
    with GOLDEN.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            rows.append(
                {
                    "user_input": row["question"],
                    "retrieved_contexts": [str(c) for c in (row.get("contexts") or [])],
                    "response": row["answer"],
                    "reference": row.get("ground_truth") or "",
                }
            )
    return rows


def main() -> int:
    try:
        from langchain_community.chat_models import ChatLiteLLM
        from ragas import EvaluationDataset, evaluate
        from ragas.llms import LangchainLLMWrapper
        from ragas.metrics.collections import ContextRecall, FactualCorrectness, Faithfulness
    except ImportError:
        print("Install eval extras: pip install -e '.[eval]'", file=sys.stderr)
        return 1

    if not GOLDEN.is_file():
        print(f"Missing {GOLDEN}", file=sys.stderr)
        return 1

    sys.path.insert(0, str(ROOT / "src"))
    from claim_pilot_ai.config import settings

    os.environ.setdefault("AWS_DEFAULT_REGION", settings.aws_region)
    model_id = os.environ.get(
        "EVAL_LLM_MODEL",
        f"bedrock/{settings.bedrock_model_id}",
    )
    chat = ChatLiteLLM(model=model_id, temperature=0)
    evaluator_llm = LangchainLLMWrapper(chat)

    evaluation_dataset = EvaluationDataset.from_list(_load_evaluation_rows())
    result = evaluate(
        dataset=evaluation_dataset,
        metrics=[
            ContextRecall(),
            Faithfulness(),
            FactualCorrectness(),
        ],
        llm=evaluator_llm,
    )
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
