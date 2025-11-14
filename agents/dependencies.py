"""Dependency injection for external services."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ResearchAgentDependencies:
    """Dependencies for the research agent - only configuration, no tool instances."""
    brave_api_key: str
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: Optional[str] = None


@dataclass
class EmailAgentDependencies:
    """Dependencies for email agent execution."""
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: Optional[str] = None