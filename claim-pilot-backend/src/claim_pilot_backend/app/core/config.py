from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Claim Pilot"
    environment: str = "dev"
    debug: bool = Field(default=False, description="Verbose / development toggles")
    log_level: str = Field(default="INFO", description="Logging level (e.g. DEBUG, INFO)")
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    bedrock_embedding_model_id: str = "amazon.titan-embed-text-v2:0"
    bedrock_knowledge_base_id: str | None = None
    database_url: str | None = None
    redis_url: str | None = None
    ai_service_url: str = "http://localhost:9020"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
