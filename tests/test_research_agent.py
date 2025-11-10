"""
Tests for the research agent functionality.
"""

import pytest
import os
from unittest.mock import Mock, patch
from pydantic_ai.models.test import TestModel

from agents.research_agent import research_agent, ResearchAgentDependencies


@pytest.fixture
def test_deps():
    """Create test dependencies."""
    return ResearchAgentDependencies(
        brave_api_key="test_brave_key",
        gmail_credentials_path="test_credentials.json",
        gmail_token_path="test_token.json",
        session_id="test_session"
    )


@pytest.mark.asyncio
async def test_research_agent_with_test_model(test_deps):
    """Test research agent with TestModel."""
    test_model = TestModel()
    
    with research_agent.override(model=test_model):
        result = await research_agent.run(
            "Research AI safety trends",
            deps=test_deps
        )
        
        assert result is not None
        assert hasattr(result, 'output')


@pytest.mark.asyncio
async def test_search_web_tool(test_deps):
    """Test web search functionality with mock."""
    with patch('tools.brave_search.search_web_tool') as mock_search:
        # Mock the search tool response
        mock_search.return_value = [
            {
                "title": "AI Safety Research",
                "url": "https://example.com/ai-safety",
                "description": "Latest developments in AI safety",
                "score": 0.95
            }
        ]
        
        test_model = TestModel()
        
        with research_agent.override(model=test_model):
            result = await research_agent.run(
                "Search for AI safety information",
                deps=test_deps
            )
            
            assert result is not None


@pytest.mark.asyncio 
async def test_email_delegation(test_deps):
    """Test email delegation to email agent."""
    test_model = TestModel()
    
    with research_agent.override(model=test_model):
        result = await research_agent.run(
            "Create email to test@example.com about AI research findings",
            deps=test_deps
        )
        
        assert result is not None


def test_research_agent_dependencies():
    """Test ResearchAgentDependencies validation."""
    deps = ResearchAgentDependencies(
        brave_api_key="test_key",
        gmail_credentials_path="credentials.json",
        gmail_token_path="token.json"
    )
    
    assert deps.brave_api_key == "test_key"
    assert deps.gmail_credentials_path == "credentials.json"
    assert deps.gmail_token_path == "token.json"
    assert deps.session_id is None


@pytest.mark.asyncio
async def test_search_web_error_handling(test_deps):
    """Test error handling in search functionality."""
    with patch('tools.brave_search.search_web_tool') as mock_search:
        # Mock an exception
        mock_search.side_effect = Exception("API Error")
        
        test_model = TestModel()
        
        with research_agent.override(model=test_model):
            result = await research_agent.run(
                "Search for information",
                deps=test_deps
            )
            
            assert result is not None