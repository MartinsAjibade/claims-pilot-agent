from fastapi import APIRouter
from claim_pilot_backend.app.schemas.agentic_rag import CoverageCheckRequest, CoverageCheckResponse
from claim_pilot_backend.app.services.rag_service import run_coverage_check

router = APIRouter()


@router.post("/coverage-check", response_model=CoverageCheckResponse)
async def coverage_check(payload: CoverageCheckRequest):
    return await run_coverage_check(payload)
