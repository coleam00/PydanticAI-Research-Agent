"""
Research-related data models.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class ResearchQuery(BaseModel):
    """Model for research query requests."""
    query: str = Field(..., description="Research topic to investigate")
    max_results: int = Field(10, ge=1, le=50, description="Maximum number of results to return")
    include_summary: bool = Field(True, description="Whether to include AI-generated summary")


class BraveSearchResult(BaseModel):
    """Model for individual Brave search results."""
    title: str = Field(..., description="Title of the search result")
    url: str = Field(..., description="URL of the search result")
    description: str = Field(..., description="Description/snippet from the search result")
    score: float = Field(0.0, ge=0.0, le=1.0, description="Relevance score")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Understanding AI Safety",
                "url": "https://example.com/ai-safety",
                "description": "A comprehensive guide to AI safety principles...",
                "score": 0.95
            }
        }
    )


class ResearchResponse(BaseModel):
    """Response model for research queries."""
    query: str = Field(..., description="Original research query")
    results: List[BraveSearchResult] = Field(..., description="Search results")
    summary: Optional[str] = Field(None, description="AI-generated summary of results")
    total_results: int = Field(..., description="Total number of results found")
    timestamp: datetime = Field(default_factory=datetime.now, description="Query timestamp")