from fastapi import FastAPI
from claim_pilot_ai.api.schemas import CoverageCheckRequest, CoverageCheckResponse, Citation
from claim_pilot_ai.workflows.insurance_rag_graph import run_insurance_rag_workflow

app = FastAPI(title="Claim Pilot AI Service", version="0.1.0")


@app.post("/api/v1/workflow/coverage-check", response_model=CoverageCheckResponse)
async def coverage_check(payload: CoverageCheckRequest):
    result = await run_insurance_rag_workflow(payload.model_dump())
    return CoverageCheckResponse(
        decision=result.get("decision", "needs_review"),
        confidence=result.get("confidence", 0.5),
        reasoning=result.get("reasoning", "The system could not fully determine coverage."),
        citations=[Citation(**c) for c in result.get("citations", [])],
        fraud_score=result.get("fraud_score"),
        next_action=result.get("next_action", "Escalate to a human adjuster."),
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
