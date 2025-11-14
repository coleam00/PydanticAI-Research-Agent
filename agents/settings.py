"""Environment-based configuration following PydanticAI best practices."""

import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Allow extra fields from .env to be ignored
    )

    # LLM Configuration
    llm_provider: str = Field(default="openai", alias="LLM_PROVIDER")
    llm_api_key: str = Field(alias="LLM_API_KEY")
    llm_model: str = Field(default="gpt-4o", alias="LLM_MODEL")
    llm_base_url: str = Field(default="https://api.openai.com/v1", alias="LLM_BASE_URL")

    # External API Keys
    brave_api_key: str = Field(alias="BRAVE_API_KEY")

    # Gmail Configuration
    gmail_credentials_path: str = Field(default="credentials/credentials.json", alias="GMAIL_CREDENTIALS_PATH")
    gmail_token_path: str = Field(default="credentials/token.json", alias="GMAIL_TOKEN_PATH")
    gmail_scopes: list[str] = ["https://www.googleapis.com/auth/gmail.modify"]

    # Application Settings
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    max_search_results: int = Field(default=10, alias="MAX_SEARCH_RESULTS")
    request_timeout: int = Field(default=30, alias="REQUEST_TIMEOUT")


# Global settings instance - only instantiate when needed
def get_settings():
    return Settings()

# For backwards compatibility
try:
    settings = Settings()
except Exception:
    # Use defaults if env vars not available (for testing)
    settings = Settings(
        llm_api_key="test_key", 
        brave_api_key="test_key"
    )