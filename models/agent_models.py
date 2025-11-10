"""
Agent-related data models.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class AgentResponse(BaseModel):
    """Generic agent response model."""
    success: bool = Field(..., description="Whether the operation was successful")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if failed")
    tools_used: List[str] = Field(default_factory=list, description="List of tools used")


class ChatMessage(BaseModel):
    """Model for chat messages in the CLI."""
    role: str = Field(..., description="Message role (user/assistant)")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    tools_used: Optional[List[Dict[str, Any]]] = Field(None, description="Tools used in response")


class SessionState(BaseModel):
    """Model for maintaining session state."""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    messages: List[ChatMessage] = Field(default_factory=list, description="Conversation history")
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation time")
    last_activity: datetime = Field(default_factory=datetime.now, description="Last activity timestamp")