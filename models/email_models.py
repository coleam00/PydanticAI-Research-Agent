"""
Email-related data models.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class EmailDraft(BaseModel):
    """Model for email draft creation."""
    to: List[str] = Field(..., min_length=1, description="List of recipient email addresses")
    subject: str = Field(..., min_length=1, description="Email subject line")
    body: str = Field(..., min_length=1, description="Email body content")
    cc: Optional[List[str]] = Field(None, description="List of CC recipients")
    bcc: Optional[List[str]] = Field(None, description="List of BCC recipients")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "to": ["john@example.com"],
                "subject": "AI Research Summary",
                "body": "Dear John,\n\nHere's the latest research on AI safety...",
                "cc": ["team@example.com"]
            }
        }
    )


class EmailDraftResponse(BaseModel):
    """Response model for email draft creation."""
    draft_id: str = Field(..., description="Gmail draft ID")
    message_id: str = Field(..., description="Message ID")
    thread_id: Optional[str] = Field(None, description="Thread ID if part of a thread")
    created_at: datetime = Field(default_factory=datetime.now, description="Draft creation timestamp")


class ResearchEmailRequest(BaseModel):
    """Model for research + email draft request."""
    research_query: str = Field(..., description="Topic to research")
    email_context: str = Field(..., description="Context for email generation")
    recipient_email: str = Field(..., description="Email recipient")
    email_subject: Optional[str] = Field(None, description="Optional email subject")