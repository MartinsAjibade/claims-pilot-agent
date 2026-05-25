"""Optional DeepEval smoke: requires ``.[eval]`` and ``RUN_EVAL_TESTS=1`` (calls Bedrock)."""

from __future__ import annotations

import os

import pytest

pytest.importorskip("deepeval")


@pytest.mark.eval
@pytest.mark.skipif(not os.environ.get("RUN_EVAL_TESTS"), reason="set RUN_EVAL_TESTS=1 to call Bedrock")
def test_deepeval_litellm_model_instantiates():
    from deepeval.models import LiteLLMModel

    from claim_pilot_ai.config import settings

    mid = os.environ.get(
        "EVAL_LLM_MODEL",
        f"bedrock/{settings.bedrock_model_id}",
    )
    m = LiteLLMModel(model=mid, temperature=0.0)
    assert mid in (getattr(m, "model_name", None) or str(getattr(m, "model", mid)))
