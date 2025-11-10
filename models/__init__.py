"""
Data models for the research and email agent system.
"""

from .email_models import EmailDraft, EmailDraftResponse, ResearchEmailRequest
from .research_models import BraveSearchResult, ResearchQuery, ResearchResponse
from .agent_models import AgentResponse, ChatMessage, SessionState

__all__ = [
    "EmailDraft",
    "EmailDraftResponse", 
    "ResearchEmailRequest",
    "BraveSearchResult",
    "ResearchQuery",
    "ResearchResponse",
    "AgentResponse",
    "ChatMessage", 
    "SessionState"
]