import boto3
from claim_pilot_ai.config import settings


class BedrockClient:
    def __init__(self):
        self.runtime = boto3.client("bedrock-runtime", region_name=settings.aws_region)
        self.agent_runtime = boto3.client("bedrock-agent-runtime", region_name=settings.aws_region)

    async def invoke_model(self, prompt: str) -> str:
        # Implement provider-specific request body for Claude, Nova, or Llama.
        raise NotImplementedError("Add Bedrock model invocation here.")
