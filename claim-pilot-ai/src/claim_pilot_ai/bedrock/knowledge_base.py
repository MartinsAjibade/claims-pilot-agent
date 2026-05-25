import boto3
from claim_pilot_ai.config import settings


async def retrieve_from_knowledge_base(query: str, knowledge_base_id: str | None = None):
    kb_id = knowledge_base_id or settings.bedrock_knowledge_base_id
    if not kb_id:
        return []
    client = boto3.client("bedrock-agent-runtime", region_name=settings.aws_region)
    response = client.retrieve(
        knowledgeBaseId=kb_id,
        retrievalQuery={"text": query},
        retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 5}},
    )
    return response.get("retrievalResults", [])
