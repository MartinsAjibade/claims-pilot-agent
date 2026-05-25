from pathlib import Path

from claim_pilot_ai.agents.heuristics import coverage_from_clause_keywords
from claim_pilot_ai.config import settings
from claim_pilot_ai.mcp.mcp_client import search_policy_clauses


async def analyze_policy_coverage(state: dict, plan: dict) -> dict:
    clauses = await search_policy_clauses(
        policy_id=state["policy_id"],
        query=plan["search_query"],
    )
    clauses_list = list(clauses)

    doc_path = state.get("policy_document_path")
    if doc_path and settings.docling_enabled:
        from claim_pilot_ai.ingestion.docling_parse import parse_document_to_markdown

        try:
            md = parse_document_to_markdown(doc_path)
            snippet = md[: settings.docling_max_chars]
            clauses_list.insert(
                0,
                {
                    "policy_id": state["policy_id"],
                    "document": Path(doc_path).name,
                    "page": None,
                    "clause_title": "Policy document (Docling)",
                    "clause_text": snippet,
                    "confidence": 1.0,
                },
            )
        except Exception:
            pass

    if settings.dspy_bedrock_enabled:
        return {
            "decision": "needs_review",
            "confidence": 0.5,
            "reasoning": "Pending DSPy/Bedrock judgment during answer composition.",
            "clauses": clauses_list,
        }

    h = coverage_from_clause_keywords(clauses_list)
    return {
        "decision": h["decision"],
        "confidence": h["confidence"],
        "reasoning": h["reasoning"],
        "clauses": clauses_list,
    }
