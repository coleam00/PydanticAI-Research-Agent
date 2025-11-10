"""
PydanticAI agents for research and email functionality.
"""

from .research_agent import research_agent, ResearchAgentDependencies
from .email_agent import email_agent, EmailAgentDependencies

__all__ = [
    "research_agent",
    "ResearchAgentDependencies", 
    "email_agent",
    "EmailAgentDependencies"
]