"""Shared LiteLLM entrypoint for Bedrock and other providers (eval + optional app use)."""

from __future__ import annotations

import os
from typing import Any

import litellm

from claim_pilot_ai.config import settings


def get_litellm_model_id() -> str:
    """LiteLLM model id, e.g. ``bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0``."""
    return os.environ.get("LITELLM_MODEL_ID", f"bedrock/{settings.bedrock_model_id}")


def chat_completion(
    messages: list[dict[str, str]],
    *,
    temperature: float = 0.0,
    max_tokens: int | None = None,
    **kwargs: Any,
) -> str:
    """
    Single-turn style completion: pass OpenAI-style ``messages`` (role/content).

    Uses default AWS credential chain for Bedrock when model id starts with ``bedrock/``.
    """
    model = get_litellm_model_id()
    mt = max_tokens if max_tokens is not None else settings.dspy_max_tokens
    resp = litellm.completion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=mt,
        aws_region_name=settings.aws_region,
        **kwargs,
    )
    choice = resp.choices[0]
    if isinstance(choice, dict):
        msg = choice.get("message") or {}
        content = msg.get("content")
    else:
        content = getattr(choice.message, "content", None)
    if isinstance(content, list):
        parts = [p.get("text", "") for p in content if isinstance(p, dict)]
        return "".join(parts).strip()
    return (content or "").strip()
