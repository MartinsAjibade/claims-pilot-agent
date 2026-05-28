#!/usr/bin/env bash
curl -X POST http://localhost:9010/api/v1/agentic-rag/coverage-check \
  -H 'Content-Type: application/json' \
  -d '{
    "claim_description": "Customer had an accident while delivering food using a personal vehicle.",
    "policy_id": "AUTO-12345",
    "claim_id": "CLM-1001",
    "question": "Is this claim covered?"
  }'
