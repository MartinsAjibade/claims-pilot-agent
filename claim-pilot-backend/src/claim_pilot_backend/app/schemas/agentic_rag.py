from pydantic import BaseModel, Field
from typing import Literal


class CoverageCheckRequest(BaseModel):
    claim_description: str = Field(..., min_length=10)
    policy_id: str
    customer_id: str | None = None
    claim_id: str | None = None
    question: str = "Is this claim covered?"
    policy_document_path: str | None = None


class Citation(BaseModel):
    document: str
    page: int | None = None
    clause_title: str | None = None
    text: str | None = None


class CoverageCheckResponse(BaseModel):
    decision: Literal["covered", "not_covered", "needs_review", "unknown"]
    confidence: float
    reasoning: str
    citations: list[Citation] = []
    fraud_score: float | None = None
    next_action: str
