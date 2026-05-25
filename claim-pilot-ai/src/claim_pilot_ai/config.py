from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "dev"
    debug: bool = Field(default=False, description="Verbose / development toggles")
    log_level: str = Field(default="INFO", description="Logging level (e.g. DEBUG, INFO)")
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    bedrock_embedding_model_id: str = "amazon.titan-embed-text-v2:0"
    bedrock_knowledge_base_id: str | None = None
    mcp_server_url: str = "http://localhost:8001"

    # Docling: parse local policy files (PDF/Office) into markdown for extra evidence
    docling_enabled: bool = Field(
        default=False,
        description="Run Docling when policy_document_path is set",
    )
    docling_max_chars: int = Field(
        default=12_000,
        description="Truncate Docling markdown merged into evidence",
    )

    # DSPy + Bedrock (via LiteLLM). When false, use keyword heuristics + existing policy_agent path
    dspy_bedrock_enabled: bool = Field(
        default=False,
        description="Use DSPy programs with Amazon Bedrock for final coverage reasoning",
    )
    dspy_max_tokens: int = Field(
        default=1_024,
        description="Max tokens for Bedrock generations in DSPy",
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
