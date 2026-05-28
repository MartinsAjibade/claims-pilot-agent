from fastapi import FastAPI
from claim_pilot_backend.app.api.v1.agentic_rag import router as agentic_rag_router
from claim_pilot_backend.app.core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(agentic_rag_router, prefix="/api/v1/agentic-rag", tags=["agentic-rag"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": settings.environment}
