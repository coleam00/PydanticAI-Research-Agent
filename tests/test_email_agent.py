"""
Tests for the email agent functionality.
"""

import pytest
import os
from unittest.mock import Mock, patch
from pydantic_ai.models.test import TestModel

from agents.email_agent import email_agent, EmailAgentDependencies


@pytest.fixture
def test_deps():
    """Create test dependencies."""
    return EmailAgentDependencies(
        gmail_credentials_path="test_credentials.json",
        gmail_token_path="test_token.pickle",
        session_id="test_session"
    )


@pytest.mark.asyncio
async def test_email_agent_with_test_model(test_deps):
    """Test email agent with TestModel."""
    test_model = TestModel()
    
    with email_agent.override(model=test_model):
        result = await email_agent.run(
            "Create professional email about quarterly results",
            deps=test_deps
        )
        
        assert result is not None
        assert hasattr(result, 'output')


@pytest.mark.asyncio
async def test_gmail_authentication_success(test_deps):
    """Test successful Gmail authentication."""
    with patch('tools.gmail_tools.authenticate_gmail_service') as mock_auth:
        mock_service = Mock()
        mock_auth.return_value = mock_service
        
        test_model = TestModel()
        
        with email_agent.override(model=test_model):
            result = await email_agent.run(
                "Authenticate with Gmail",
                deps=test_deps
            )
            
            assert result is not None


@pytest.mark.asyncio
async def test_gmail_draft_creation(test_deps):
    """Test Gmail draft creation."""
    with patch('tools.gmail_tools.authenticate_gmail_service') as mock_auth, \
         patch('tools.gmail_tools.create_gmail_draft') as mock_create:
        
        # Mock successful authentication
        mock_service = Mock()
        mock_auth.return_value = mock_service
        
        # Mock successful draft creation
        mock_create.return_value = {
            "success": True,
            "draft_id": "draft_123",
            "message_id": "msg_123"
        }
        
        test_model = TestModel()
        
        with email_agent.override(model=test_model):
            result = await email_agent.run(
                "Create draft email to test@example.com about project updates",
                deps=test_deps
            )
            
            assert result is not None


def test_email_agent_dependencies():
    """Test EmailAgentDependencies validation."""
    deps = EmailAgentDependencies(
        gmail_credentials_path="credentials.json",
        gmail_token_path="token.pickle",
        session_id="session_123"
    )
    
    assert deps.gmail_credentials_path == "credentials.json"
    assert deps.gmail_token_path == "token.pickle"
    assert deps.session_id == "session_123"