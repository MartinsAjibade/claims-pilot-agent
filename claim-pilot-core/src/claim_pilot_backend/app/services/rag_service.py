import httpx
from claim_pilot_backend.app.schemas.agentic_rag import CoverageCheckRequest, CoverageCheckResponse, Citation
from claim_pilot_backend.app.core.config import settings


async def run_coverage_check(payload: CoverageCheckRequest) -> CoverageCheckResponse:
    async with httpx.AsyncClient(base_url=settings.ai_service_url) as client:
        response = await client.post(
            "/api/v1/workflow/coverage-check",
            json=payload.model_dump(),
            timeout=30.0,
        )
        response.raise_for_status()
        result = response.json()
    return CoverageCheckResponse(
        decision=result.get("decision", "needs_review"),
        confidence=result.get("confidence", 0.5),
        reasoning=result.get("reasoning", "The system could not fully determine coverage."),
        citations=[Citation(**c) for c in result.get("citations", [])],
        fraud_score=result.get("fraud_score"),
        next_action=result.get("next_action", "Escalate to a human adjuster."),
    )
