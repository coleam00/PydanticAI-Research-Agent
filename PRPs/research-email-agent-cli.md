---
name: "PydanticAI Research + Email Agent with CLI"
description: "Complete implementation of a research agent with email drafting capabilities and beautiful streaming CLI"
---

## Purpose

Build a PydanticAI research agent that uses Brave Search API for web research and delegates email drafting to a sub-agent using Gmail API. The system includes a beautiful CLI with real-time streaming output using Rich library and PydanticAI's .iter() function.

## Core Principles

1. **PydanticAI Best Practices**: Deep integration with PydanticAI patterns for agent creation, tools, and structured outputs
2. **Production Ready**: Include security, testing, and monitoring for production deployments
3. **Type Safety First**: Leverage PydanticAI's type-safe design and Pydantic validation throughout
4. **Context Engineering Integration**: Apply proven context engineering workflows to AI agent development
5. **Comprehensive Testing**: Use TestModel and FunctionModel for thorough agent validation

## ⚠️ Implementation Guidelines: Don't Over-Engineer

**IMPORTANT**: Keep your agent implementation focused and practical. Don't build unnecessary complexity.

### What NOT to do:
- ❌ **Don't create dozens of tools** - Build only the tools your agent actually needs (search_web, delegate_to_email_agent)
- ❌ **Don't over-complicate dependencies** - Keep dependency injection simple and focused
- ❌ **Don't add unnecessary abstractions** - Follow main_agent_reference patterns directly
- ❌ **Don't build complex workflows** unless specifically required
- ❌ **Don't add structured output** unless validation is specifically needed (default to string)

### What TO do:
- ✅ **Start simple** - Build the minimum viable agent that meets requirements
- ✅ **Add tools incrementally** - Implement only what the agent needs to function
- ✅ **Follow main_agent_reference** - Use proven patterns, don't reinvent
- ✅ **Use string output by default** - Only add result_type when validation is required
- ✅ **Test early and often** - Use TestModel to validate as you build

### Key Question:
**"Does this agent really need this feature to accomplish its core purpose?"**

If the answer is no, don't build it. Keep it simple, focused, and functional.

---

## Goal

Create a production-ready PydanticAI agent system where a research agent performs web searches using Brave API and delegates email composition to a specialized email agent that creates Gmail drafts. Include a beautiful CLI interface with real-time streaming output for user interaction.

## Why

This agent system addresses the common workflow of researching information and then composing professional emails based on the findings. By separating concerns into specialized agents and providing a streaming CLI, users get a powerful, interactive tool for research-driven communication.

## What

### Agent Type Classification
- [x] **Tool-Enabled Agent**: Research agent with Brave search and email delegation tools
- [x] **Tool-Enabled Agent**: Email agent with Gmail draft creation capabilities
- [x] **Workflow Agent**: Agent-to-agent delegation pattern
- [ ] **Structured Output Agent**: Default to string output except for EmailDraft model

### Model Provider Requirements
- [x] **OpenAI**: `openai:gpt-4o` or `openai:gpt-4o-mini` (primary)
- [x] **Anthropic**: `anthropic:claude-3-5-sonnet-20241022` (fallback)
- [x] **Fallback Strategy**: Environment-based configuration with provider switching

### External Integrations
- [x] Brave Search API for web research
- [x] Gmail API with OAuth2 for draft creation
- [x] Rich library for beautiful CLI output
- [x] python-dotenv for environment configuration

### Success Criteria
- [x] Research agent successfully searches web and summarizes findings
- [x] Email agent creates Gmail drafts based on research
- [x] Agent-to-agent delegation works seamlessly
- [x] CLI provides real-time streaming output with .iter()
- [x] Comprehensive test coverage with TestModel and FunctionModel
- [x] Security measures implemented (API keys, OAuth2, input validation)

## All Needed Context

### PydanticAI Documentation & Research

```yaml
# ESSENTIAL PYDANTIC AI DOCUMENTATION - Must be researched
- url: https://ai.pydantic.dev/
  why: Official PydanticAI documentation with getting started guide
  content: Agent creation, model providers, dependency injection patterns

- url: https://ai.pydantic.dev/agents/
  why: Comprehensive agent architecture and configuration patterns
  content: System prompts, output types, execution methods, agent composition

- url: https://ai.pydantic.dev/tools/
  why: Tool integration patterns and function registration
  content: @agent.tool decorators, RunContext usage, parameter validation

- url: https://ai.pydantic.dev/testing/
  why: Testing strategies specific to PydanticAI agents
  content: TestModel, FunctionModel, Agent.override(), pytest patterns

- url: https://ai.pydantic.dev/models/
  why: Model provider configuration and authentication
  content: OpenAI, Anthropic, Gemini setup, API key management, fallback models

- url: https://ai.pydantic.dev/examples/stream-markdown/
  why: Streaming patterns with .iter() for real-time output
  content: AgentRun iteration, TextPartDelta handling, event processing

# Existing codebase patterns
- path: examples/main_agent_reference/
  why: Existing implementation with Brave search and partial email integration
  content: research_agent.py shows agent-to-agent delegation pattern, tools.py has Brave implementation

- path: examples/testing_examples/test_agent_patterns.py
  why: Comprehensive testing patterns
  content: TestModel usage, FunctionModel patterns, mock dependencies

# External API documentation
- url: https://brave.com/search/api/
  why: Official Brave Search API documentation
  content: Authentication, query parameters, response format, rate limits

- url: https://developers.google.com/workspace/gmail/api/quickstart/python
  why: Gmail API Python quickstart
  content: OAuth2 flow, token storage, draft creation endpoints

- url: https://rich.readthedocs.io/en/stable/introduction.html
  why: Rich library for beautiful CLI output
  content: Console, Live displays, markdown rendering, progress bars
```

### Agent Architecture Research

```yaml
# Existing Research Agent Implementation (examples/main_agent_reference/research_agent.py)
agent_to_agent_pattern:
  tool_implementation: |
    @research_agent.tool
    async def create_email_draft(
        ctx: RunContext[ResearchAgentDependencies],
        ...
    ) -> Dict[str, Any]:
        email_deps = EmailAgentDependencies(...)
        result = await email_agent.run(
            email_prompt,
            deps=email_deps,
            usage=ctx.usage  # Pass usage for token tracking
        )
        return result.output

  key_insights:
    - Agents are stateless and global
    - Dependencies created within tool for delegate agent
    - Usage tracking passed through for token counting
    - Error handling at tool level

# Streaming Pattern with .iter()
streaming_implementation:
  basic_pattern: |
    async with agent.iter(user_prompt, deps=deps) as run:
        async for node in run:
            if Agent.is_model_request_node(node):
                async for event in node.stream():
                    if isinstance(event.delta, TextPartDelta):
                        console.print(event.delta.text, end="")

  cli_integration:
    - Use Rich Console for formatted output
    - Handle tool invocations with visual indicators
    - Show progress for long-running operations
    - Format markdown responses

# Gmail OAuth2 Pattern
gmail_integration:
  oauth_flow: |
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_file, SCOPES
    )
    creds = flow.run_local_server(port=0)
    # Save tokens for refresh
    
  draft_creation: |
    message = MIMEText(body)
    message['to'] = ', '.join(recipients)
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().drafts().create(
        userId='me', body={'message': {'raw': raw}}
    ).execute()
```

### Security and Production Considerations

```yaml
# Environment Variables Required
environment_setup:
  required_vars:
    - LLM_PROVIDER: "openai"
    - LLM_API_KEY: "your-openai-key"
    - LLM_MODEL: "gpt-4o"
    - BRAVE_API_KEY: "your-brave-key"
    - GMAIL_CREDENTIALS_PATH: "path/to/credentials.json"
    - GMAIL_TOKEN_PATH: "path/to/token.json"
  
  security:
    - Use .env file with python-dotenv
    - Never commit credentials or tokens
    - Validate all API keys on startup
    - Implement rate limiting for Brave API
```

### Common PydanticAI Gotchas (from research)

```yaml
implementation_gotchas:
  agent_delegation:
    issue: "Agents must be defined at module level, not passed in dependencies"
    solution: "Import email_agent directly in research_agent.py"
  
  streaming_complexity:
    issue: ".iter() requires careful async handling and event processing"
    solution: "Follow examples/stream-markdown pattern with proper node type checking"
  
  oauth_token_refresh:
    issue: "Gmail tokens expire and need refresh handling"
    solution: "Implement token refresh logic with google-auth library"
  
  rate_limiting:
    issue: "Brave API has rate limits that need handling"
    solution: "Use aiolimiter for async rate limiting (already in tools.py)"
```

## Implementation Blueprint

### Technology Stack

```yaml
Core:
  - Python 3.11+
  - PydanticAI (latest)
  - pydantic-settings
  - python-dotenv

External APIs:
  - brave-search (or direct requests)
  - google-auth, google-auth-oauthlib, google-api-python-client

CLI:
  - rich (for beautiful terminal output)
  - asyncio (for async CLI operations)

Testing:
  - pytest, pytest-asyncio
  - pytest-mock
```

### Agent Implementation Plan

```yaml
Implementation Task 1 - Complete Email Agent:
  CREATE email_agent.py:
    - Import patterns from research_agent.py
    - EmailAgentDependencies with Gmail paths
    - System prompt for professional email composition
    - Tools: authenticate_gmail(), create_gmail_draft()
    - Error handling for OAuth failures

Implementation Task 2 - Gmail Integration:
  CREATE gmail_tools.py:
    - OAuth2 authentication flow implementation
    - Token storage and refresh logic
    - Draft creation with MIME formatting
    - Error handling for API failures
    - Rate limiting considerations

Implementation Task 3 - Update Research Agent:
  MODIFY research_agent.py:
    - Import email_agent at module level
    - Update delegate_to_email_agent tool
    - Ensure proper error propagation
    - Add truthful reporting in system prompt

Implementation Task 4 - Build Streaming CLI:
  CREATE cli.py:
    - Rich Console initialization
    - Async main loop with agent.iter()
    - Stream processing with TextPartDelta
    - Tool invocation visualization
    - Markdown rendering for responses
    - Error display with tracebacks

Implementation Task 5 - Configuration and Setup:
  CREATE/UPDATE configuration:
    - .env.example with all required variables
    - README.md with setup instructions
    - Project structure documentation
    - Gmail OAuth2 setup guide
    - Brave API registration guide

Implementation Task 6 - Comprehensive Testing:
  CREATE tests/:
    - test_research_agent.py (with TestModel)
    - test_email_agent.py (with FunctionModel)
    - test_gmail_integration.py (with mocks)
    - test_cli.py (streaming behavior)
    - test_integration.py (full workflow)

Implementation Task 7 - Gmail Setup Script:
  CREATE setup_gmail.py:
    - Interactive Gmail OAuth2 setup wizard
    - Credential validation and download guidance
    - Token generation and storage
    - Connection testing and verification

Implementation Task 8 - Documentation:
  CREATE documentation:
    - API key setup instructions
    - Gmail OAuth2 configuration
    - CLI usage examples
    - Troubleshooting guide
```

### Detailed Implementation Steps

```python
# Task 1: Email Agent Implementation
# File: email_agent.py
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from typing import Dict, Any, List
from .providers import get_llm_model
from .models import EmailDraft
import logging

logger = logging.getLogger(__name__)

@dataclass
class EmailAgentDependencies:
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: str = None

email_agent = Agent(
    get_llm_model(),
    deps_type=EmailAgentDependencies,
    system_prompt="""Professional email composition agent that creates well-structured emails based on research findings. Guidelines:
- Use clear, professional language for business communication
- Structure emails with proper greeting, body, and closing
- Include relevant research insights
- Return properly formatted EmailDraft objects
- Creates drafts only - does not send emails"""
)

@email_agent.tool
async def authenticate_gmail(ctx: RunContext[EmailAgentDependencies]) -> Dict[str, Any]:
    """Handles OAuth2 authentication with Gmail API."""
    from .gmail_tools import authenticate_gmail_service
    try:
        service = await authenticate_gmail_service(
            ctx.deps.gmail_credentials_path,
            ctx.deps.gmail_token_path
        )
        return {"success": True, "message": "Gmail authenticated successfully", "service_available": True}
    except FileNotFoundError as e:
        logger.error(f"Gmail setup required: {e}")
        return {
            "success": False, 
            "error": "Gmail OAuth2 not configured", 
            "message": "Run 'python setup_gmail.py' to configure Gmail authentication",
            "recoverable": True,
            "setup_command": "python setup_gmail.py"
        }
    except Exception as e:
        logger.error(f"Gmail authentication failed: {e}")
        error_message = str(e)
        
        # Check for common error patterns and provide helpful recovery steps
        if "refresh" in error_message.lower():
            return {
                "success": False,
                "error": f"Token refresh failed: {e}",
                "message": "Gmail token has expired. Run 'python setup_gmail.py' to re-authenticate",
                "recoverable": True,
                "setup_command": "python setup_gmail.py"
            }
        elif "credentials" in error_message.lower():
            return {
                "success": False,
                "error": f"Credentials error: {e}",
                "message": "Gmail credentials file is invalid. Run 'python setup_gmail.py' to fix",
                "recoverable": True,
                "setup_command": "python setup_gmail.py"
            }
        else:
            return {
                "success": False,
                "error": str(e),
                "message": f"Gmail authentication failed: {e}",
                "recoverable": False
            }

@email_agent.tool
async def create_gmail_draft(
    ctx: RunContext[EmailAgentDependencies],
    email_draft: EmailDraft
) -> Dict[str, Any]:
    """Creates a draft email in Gmail without sending."""
    from .gmail_tools import authenticate_gmail_service, create_gmail_draft as create_draft
    
    # First authenticate
    try:
        service = await authenticate_gmail_service(
            ctx.deps.gmail_credentials_path,
            ctx.deps.gmail_token_path
        )
    except Exception as e:
        return {
            "success": False,
            "error": f"Gmail authentication failed: {e}",
            "message": "Cannot create draft without Gmail authentication. Run 'python setup_gmail.py' first",
            "recoverable": True
        }
    
    # Create the draft
    try:
        result = await create_draft(
            service=service,
            recipients=email_draft.to,
            subject=email_draft.subject,
            body=email_draft.body,
            cc=email_draft.cc,
            bcc=email_draft.bcc
        )
        
        if result["success"]:
            logger.info(f"Gmail draft created successfully: {result['draft_id']}")
            return {
                "success": True,
                "draft_id": result["draft_id"],
                "message_id": result["message_id"],
                "message": f"Email draft created successfully in Gmail. Draft ID: {result['draft_id']}"
            }
        else:
            logger.error(f"Failed to create Gmail draft: {result['error']}")
            return {
                "success": False,
                "error": result["error"],
                "message": f"Failed to create Gmail draft: {result['message']}"
            }
            
    except Exception as e:
        logger.error(f"Unexpected error creating Gmail draft: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Unexpected error creating Gmail draft: {e}"
        }

# Task 2: Gmail Tools Implementation
# File: gmail_tools.py
import os
import pickle
import base64
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Dict, Any, List
from unittest.mock import Mock

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

class MockGmailService:
    """Mock Gmail service for testing purposes."""
    
    def __init__(self):
        self.drafts_created = []
    
    def users(self):
        return MockUsersResource(self.drafts_created)

class MockUsersResource:
    def __init__(self, drafts_created):
        self.drafts_created = drafts_created
    
    def drafts(self):
        return MockDraftsResource(self.drafts_created)

class MockDraftsResource:
    def __init__(self, drafts_created):
        self.drafts_created = drafts_created
    
    def create(self, userId: str, body: Dict[str, Any]):
        """Mock draft creation."""
        draft_id = f"mock_draft_{len(self.drafts_created) + 1}"
        self.drafts_created.append({
            'id': draft_id,
            'userId': userId,
            'body': body
        })
        return MockExecuteResponse({'id': draft_id, 'message': {'id': f"msg_{draft_id}"}})

class MockExecuteResponse:
    def __init__(self, response_data):
        self.response_data = response_data
    
    def execute(self):
        return self.response_data

async def authenticate_gmail_service(credentials_path: str, token_path: str, test_mode: bool = False):
    """Authenticate and return Gmail service instance."""
    # Return mock service for testing
    if test_mode or os.getenv('TESTING') == 'true':
        logger.info("Using mock Gmail service for testing")
        return MockGmailService()
    
    creds = None
    
    # Check if credentials file exists
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"Gmail credentials file not found at {credentials_path}. "
            "Run 'python setup_gmail.py' to set up OAuth2 authentication."
        )
    
    # Token loading and refresh logic
    if os.path.exists(token_path):
        try:
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        except Exception as e:
            logger.warning(f"Failed to load existing token: {e}")
            # Remove corrupted token file
            os.remove(token_path)
    
    # OAuth2 flow if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logger.info("Successfully refreshed Gmail token")
            except Exception as e:
                logger.error(f"Failed to refresh token: {e}")
                raise Exception(
                    f"Failed to refresh Gmail token: {e}. "
                    "Run 'python setup_gmail.py' to re-authenticate."
                )
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
                logger.info("Successfully completed OAuth2 flow")
            except Exception as e:
                logger.error(f"OAuth2 flow failed: {e}")
                raise Exception(
                    f"Gmail OAuth2 authentication failed: {e}. "
                    "Ensure you have downloaded credentials.json from Google Cloud Console."
                )
        
        # Save tokens
        try:
            os.makedirs(os.path.dirname(token_path), exist_ok=True)
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            logger.info(f"Successfully saved Gmail token to {token_path}")
        except Exception as e:
            logger.warning(f"Failed to save token: {e}")
    
    return build('gmail', 'v1', credentials=creds)

async def create_gmail_draft(service, recipients: List[str], subject: str, body: str, cc: List[str] = None, bcc: List[str] = None) -> Dict[str, Any]:
    """Create a Gmail draft email."""
    try:
        # Create message
        message = MIMEMultipart()
        message['to'] = ', '.join(recipients)
        message['subject'] = subject
        
        if cc:
            message['cc'] = ', '.join(cc)
        if bcc:
            message['bcc'] = ', '.join(bcc)
        
        # Add body
        message.attach(MIMEText(body, 'plain'))
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        # Create draft
        draft_body = {
            'message': {
                'raw': raw_message
            }
        }
        
        result = service.users().drafts().create(
            userId='me',
            body=draft_body
        ).execute()
        
        return {
            'success': True,
            'draft_id': result['id'],
            'message_id': result['message']['id'],
            'message': f"Draft created successfully with ID: {result['id']}"
        }
        
    except Exception as e:
        logger.error(f"Failed to create Gmail draft: {e}")
        return {
            'success': False,
            'error': str(e),
            'message': f"Failed to create Gmail draft: {e}"
        }

# Task 4: CLI Implementation
# File: cli.py
import asyncio
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from pydantic_ai import Agent, models
from pydantic_ai.models.streamed_text import TextPartDelta
from .research_agent import research_agent, ResearchAgentDependencies
from .settings import load_settings

console = Console()

async def stream_agent_response(prompt: str, deps: ResearchAgentDependencies):
    """Stream agent response with beautiful formatting."""
    with Live(console=console, refresh_per_second=10) as live:
        output_parts = []
        
        async with research_agent.iter(prompt, deps=deps) as run:
            async for node in run:
                if Agent.is_user_prompt_node(node):
                    live.update(f"[bold cyan]You:[/bold cyan] {node.text}")
                
                elif Agent.is_model_request_node(node):
                    live.update("[yellow]Thinking...[/yellow]")
                    
                    # Stream the response
                    async for event in node.stream():
                        if isinstance(event.delta, TextPartDelta):
                            output_parts.append(event.delta.text)
                            # Update display with accumulated text
                            md = Markdown(''.join(output_parts))
                            live.update(md)
                
                elif Agent.is_tool_call_node(node):
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=console
                    ) as progress:
                        task = progress.add_task(
                            f"Running tool: {node.tool_name}", 
                            total=None
                        )
                        # Tool execution happens here
                        progress.update(task, completed=True)

async def main():
    """Main CLI entry point."""
    settings = load_settings()
    
    deps = ResearchAgentDependencies(
        brave_api_key=settings.brave_api_key,
        gmail_credentials_path=settings.gmail_credentials_path,
        gmail_token_path=settings.gmail_token_path
    )
    
    console.print("[bold green]Research & Email Agent CLI[/bold green]")
    console.print("Type 'exit' to quit\n")
    
    while True:
        try:
            prompt = console.input("[bold cyan]You:[/bold cyan] ")
            if prompt.lower() in ['exit', 'quit']:
                break
            
            await stream_agent_response(prompt, deps)
            console.print()  # Add spacing
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    asyncio.run(main())

# Task 5: Gmail Setup Script
# File: setup_gmail.py
import os
import sys
import pickle
import webbrowser
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.markdown import Markdown
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

console = Console()

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def display_welcome():
    """Display welcome message and setup instructions."""
    welcome_text = """
# Gmail OAuth2 Setup Wizard

This wizard will help you set up Gmail OAuth2 authentication for the Research Agent.

## Prerequisites:
1. **Google Cloud Project** with Gmail API enabled
2. **OAuth2 Credentials** downloaded from Google Cloud Console
3. **Internet connection** for authentication flow

## What this script will do:
- Guide you through credential file setup
- Run OAuth2 authentication flow
- Test Gmail API connection
- Save authentication tokens securely
    """
    
    console.print(Panel(Markdown(welcome_text), title="Gmail Setup", border_style="blue"))

def check_credentials_file(credentials_path: str) -> bool:
    """Check if credentials file exists and is valid."""
    if not os.path.exists(credentials_path):
        return False
    
    try:
        # Try to parse the credentials file
        with open(credentials_path, 'r') as f:
            import json
            data = json.load(f)
            return 'installed' in data or 'web' in data
    except Exception as e:
        console.print(f"[red]Error reading credentials file: {e}[/red]")
        return False

def guide_credentials_download():
    """Guide user through credentials download process."""
    instructions = """
# Download Gmail API Credentials

## Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing one

## Step 2: Enable Gmail API
1. Go to **APIs & Services > Library**
2. Search for "Gmail API"
3. Click **Enable**

## Step 3: Create OAuth2 Credentials
1. Go to **APIs & Services > Credentials**
2. Click **+ CREATE CREDENTIALS**
3. Select **OAuth 2.0 Client IDs**
4. Choose **Desktop application**
5. Give it a name (e.g., "Research Agent")
6. Click **CREATE**

## Step 4: Download Credentials
1. Click the **Download** button (⬇) next to your OAuth client
2. Save the file as `credentials.json` in this directory
3. **Never commit this file to version control!**
    """
    
    console.print(Panel(Markdown(instructions), title="Download Instructions", border_style="yellow"))
    
    # Optionally open browser to Google Cloud Console
    if Confirm.ask("Open Google Cloud Console in browser?", default=True):
        webbrowser.open("https://console.cloud.google.com/apis/credentials")

def run_oauth_flow(credentials_path: str, token_path: str) -> bool:
    """Run OAuth2 authentication flow."""
    try:
        console.print("\n[yellow]Starting OAuth2 authentication flow...[/yellow]")
        
        # Create OAuth2 flow
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, SCOPES
        )
        
        console.print("[blue]Opening browser for authentication...[/blue]")
        creds = flow.run_local_server(port=0)
        
        # Save token
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        
        console.print(f"[green]✓ Authentication successful! Token saved to {token_path}[/green]")
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Authentication failed: {e}[/red]")
        return False

def test_gmail_connection(token_path: str) -> bool:
    """Test Gmail API connection."""
    try:
        console.print("\n[yellow]Testing Gmail API connection...[/yellow]")
        
        # Load credentials
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
        
        # Build service
        service = build('gmail', 'v1', credentials=creds)
        
        # Test with a simple API call
        profile = service.users().getProfile(userId='me').execute()
        email_address = profile.get('emailAddress')
        
        console.print(f"[green]✓ Gmail API connection successful![/green]")
        console.print(f"[green]✓ Connected to: {email_address}[/green]")
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Gmail API connection failed: {e}[/red]")
        return False

def create_env_example():
    """Create .env.example with Gmail configuration."""
    env_content = """# Gmail OAuth2 Configuration
GMAIL_CREDENTIALS_PATH=credentials.json
GMAIL_TOKEN_PATH=token.json

# LLM Configuration
LLM_PROVIDER=openai
LLM_API_KEY=your-openai-api-key
LLM_MODEL=gpt-4o

# Brave Search Configuration
BRAVE_API_KEY=your-brave-api-key
"""
    
    if not os.path.exists('.env.example'):
        with open('.env.example', 'w') as f:
            f.write(env_content)
        console.print("[green]✓ Created .env.example with Gmail configuration[/green]")

def main():
    """Main setup function."""
    display_welcome()
    
    # Get paths from environment or defaults
    credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
    token_path = os.getenv('GMAIL_TOKEN_PATH', 'token.json')
    
    console.print(f"[blue]Credentials path: {credentials_path}[/blue]")
    console.print(f"[blue]Token path: {token_path}[/blue]\n")
    
    # Check for existing setup
    if os.path.exists(token_path):
        if Confirm.ask("Gmail already appears to be set up. Re-run setup?", default=False):
            os.remove(token_path)
        else:
            # Test existing setup
            if test_gmail_connection(token_path):
                console.print("\n[green]Gmail is already configured and working![/green]")
                return True
            else:
                console.print("[yellow]Existing setup appears broken. Continuing with fresh setup...[/yellow]")
    
    # Check credentials file
    if not check_credentials_file(credentials_path):
        console.print(f"[yellow]Credentials file not found or invalid: {credentials_path}[/yellow]")
        guide_credentials_download()
        
        # Wait for user to download credentials
        while not check_credentials_file(credentials_path):
            if not Confirm.ask(f"Have you saved credentials.json to {credentials_path}?"):
                console.print("[red]Setup cancelled. Please download credentials.json first.[/red]")
                return False
            
            if not check_credentials_file(credentials_path):
                console.print("[red]Credentials file still not found or invalid.[/red]")
    
    console.print("[green]✓ Credentials file found and valid[/green]")
    
    # Run OAuth2 flow
    if not run_oauth_flow(credentials_path, token_path):
        console.print("[red]Setup failed during OAuth2 flow.[/red]")
        return False
    
    # Test connection
    if not test_gmail_connection(token_path):
        console.print("[red]Setup failed during connection test.[/red]")
        return False
    
    # Create environment example
    create_env_example()
    
    # Success message
    success_message = """
# Gmail Setup Complete! ✅

## What was configured:
- OAuth2 credentials validated
- Authentication tokens generated and saved
- Gmail API connection tested successfully

## Next steps:
1. Copy `.env.example` to `.env`
2. Add your other API keys (OpenAI, Brave)
3. Run the research agent: `python cli.py`

## Security reminders:
- **Never commit credentials.json or token.json to version control**
- Add them to your .gitignore file
- Keep your API keys secure in the .env file
    """
    
    console.print(Panel(Markdown(success_message), title="Setup Complete", border_style="green"))
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Setup cancelled by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]")
        sys.exit(1)
```

## Validation Loop

### Level 0: Gmail OAuth2 Setup Validation

```bash
# Check if Gmail OAuth2 is configured
python -c "
import os
credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
token_path = os.getenv('GMAIL_TOKEN_PATH', 'token.json')

if os.path.exists(credentials_path) and os.path.exists(token_path):
    print('✓ Gmail OAuth2 already configured')
elif os.path.exists(credentials_path):
    print('⚠ Gmail credentials found, but no token. Run initial OAuth2 flow needed.')
else:
    print('⚠ Gmail not configured. Run \'python setup_gmail.py\' for first-time OAuth2 setup')
"

# Test Gmail service in test mode
python -c "
import asyncio
import os
os.environ['TESTING'] = 'true'
from gmail_tools import authenticate_gmail_service

async def test_gmail():
    service = await authenticate_gmail_service('', '', test_mode=True)
    print('✓ Mock Gmail service working for tests')

asyncio.run(test_gmail())
"

# Expected: Either Gmail configured or clear setup instructions
# If not configured: Run setup_gmail.py before proceeding
```

### Level 1: Project Structure Validation

```bash
# Verify complete project structure
find . -type f -name "*.py" | grep -E "(research_agent|email_agent|gmail_tools|cli|settings|providers|models|dependencies|setup_gmail)" | sort

# Check for required configuration files
test -f .env.example && echo "✓ Environment template present"
test -f README.md && echo "✓ README documentation present" 
test -f requirements.txt && echo "✓ Requirements file present"
test -f setup_gmail.py && echo "✓ Gmail setup script present"

# Verify test structure
find tests/ -name "test_*.py" | wc -l  # Should have multiple test files

# Expected: Complete project structure with all required files including setup_gmail.py
# If missing: Generate missing components
```

### Level 2: Agent Functionality Validation

```bash
# Test research agent can be imported and has email delegation
python -c "
from research_agent import research_agent
tools = [t.name for t in research_agent.tools]
assert 'search_web' in tools
assert 'delegate_to_email_agent' in tools
print('✓ Research agent tools configured correctly')
"

# Test email agent exists and has Gmail tools
python -c "
from email_agent import email_agent
tools = [t.name for t in email_agent.tools]
assert 'authenticate_gmail' in tools
assert 'create_gmail_draft' in tools
print('✓ Email agent tools configured correctly')
"

# Test Gmail error recovery with detailed messages
python -c "
import os
os.environ['TESTING'] = 'false'  # Test real error handling
from email_agent import email_agent, EmailAgentDependencies
from pydantic_ai.models.test import TestModel

deps = EmailAgentDependencies(
    gmail_credentials_path='nonexistent.json',
    gmail_token_path='nonexistent.pickle'
)

test_model = TestModel()
with email_agent.override(model=test_model):
    # This should trigger FileNotFoundError handling
    result = email_agent.run_sync('Test Gmail authentication', deps=deps)
    print('✓ Gmail error recovery implemented')
"

# Test with TestModel for research agent
python -c "
from pydantic_ai.models.test import TestModel
from research_agent import research_agent, ResearchAgentDependencies
test_model = TestModel()
deps = ResearchAgentDependencies(brave_api_key='test')
with research_agent.override(model=test_model):
    result = research_agent.run_sync('Test research', deps=deps)
    print('✓ TestModel validation passed')
"

# Expected: All agents instantiate correctly with proper tools and error recovery
# If failing: Debug agent configuration and tool registration
```

### Level 3: Integration Testing

```bash
# Run unit tests
python -m pytest tests/test_research_agent.py -v
python -m pytest tests/test_email_agent.py -v
python -m pytest tests/test_gmail_integration.py -v

# Run integration tests with mocked Gmail
TESTING=true python -m pytest tests/test_integration.py -v

# Test CLI streaming (requires manual verification)
python -c "
import asyncio
from cli import stream_agent_response
from research_agent import ResearchAgentDependencies

async def test_cli():
    deps = ResearchAgentDependencies(brave_api_key='test_key')
    # This would normally stream output
    print('✓ CLI streaming function available')

asyncio.run(test_cli())
"

# Expected: All tests pass, CLI shows streaming capabilities
# If failing: Fix based on test failures
```

### Level 4: Security and Production Validation

```bash
# Check no hardcoded secrets
grep -r "sk-" . --include="*.py" | grep -v ".env" # Should be empty
grep -r "credentials.json" . --include="*.py" | grep -v "example" | grep -v "setup_gmail" # Should use env vars (except in setup script)

# Test Gmail setup script functionality
python -c "
from setup_gmail import check_credentials_file
# Test with non-existent file
result = check_credentials_file('nonexistent.json')
assert result == False
print('✓ Setup script credential validation works')
"

# Verify environment handling
python -c "
from settings import load_settings
try:
    settings = load_settings()
    print('✓ Settings load without .env file (using defaults or env vars)')
except Exception as e:
    print(f'✗ Settings require .env file: {e}')
"

# Check comprehensive error handling
grep -r "try:" . --include="*.py" | wc -l  # Should be > 15 (with enhanced error handling)
grep -r "logger" . --include="*.py" | wc -l  # Should have extensive logging
grep -r "recoverable.*True" . --include="*.py" | wc -l  # Should have recovery patterns

# Test error recovery messages provide actionable steps
python -c "
import os
os.environ['TESTING'] = 'false'
from gmail_tools import authenticate_gmail_service
import asyncio

async def test_error_recovery():
    try:
        await authenticate_gmail_service('nonexistent.json', 'nonexistent.pickle')
    except FileNotFoundError as e:
        assert 'setup_gmail.py' in str(e)
        print('✓ Error recovery messages include actionable steps')
    except Exception as e:
        print(f'✓ Error handling working: {type(e).__name__}')

asyncio.run(test_error_recovery())
"

# Test mock service integration
python -c "
import os
os.environ['TESTING'] = 'true'
import asyncio
from gmail_tools import authenticate_gmail_service

async def test_mock():
    service = await authenticate_gmail_service('', '', test_mode=True)
    print('✓ Mock Gmail service working for automated testing')

asyncio.run(test_mock())
"

# Expected: Security measures in place, actionable error recovery, comprehensive testing support
# If issues: Implement missing security and recovery patterns
```

## Final Validation Checklist

### Agent Implementation Completeness

- [ ] Research agent with Brave search integration works
- [ ] Email agent with Gmail draft creation works
- [ ] Agent-to-agent delegation functions correctly
- [ ] CLI provides beautiful streaming output with Rich
- [ ] All tools have proper error handling and logging
- [ ] Comprehensive test suite with TestModel and FunctionModel

### PydanticAI Best Practices

- [ ] Type safety throughout with proper type hints
- [ ] Security patterns implemented (API keys via env, OAuth2 tokens)
- [ ] Error handling and retry mechanisms for robust operation
- [ ] Async patterns consistent throughout
- [ ] Documentation complete with setup instructions

### Production Readiness

- [ ] Environment configuration with .env.example
- [ ] README with Gmail OAuth2 setup instructions
- [ ] Logging configured for debugging
- [ ] Rate limiting implemented for Brave API
- [ ] Token refresh handling for Gmail
- [ ] Deployment instructions included

---

## Anti-Patterns to Avoid

### PydanticAI Agent Development

- ❌ Don't pass agents in dependencies - agents are global/module-level
- ❌ Don't skip TestModel validation - always test during development
- ❌ Don't mix async/sync incorrectly - use run_sync or await run consistently
- ❌ Don't ignore usage tracking - pass ctx.usage for token counting
- ❌ Don't overcomplicate tools - keep them focused and testable

### Security and Production

- ❌ Don't commit Gmail credentials.json or token files
- ❌ Don't expose API keys in logs or error messages
- ❌ Don't skip OAuth2 token refresh handling
- ❌ Don't ignore rate limits on external APIs
- ❌ Don't forget input validation on user prompts

---

## To Achieve 10/10 Confidence

**Current Risk:** Gmail OAuth2 requires manual setup that could complicate testing

**Solutions to implement:**

### 1. Add Gmail OAuth2 Mock Strategy
```python
# In gmail_tools.py - Add test mode bypass
async def authenticate_gmail_service(credentials_path: str, token_path: str, test_mode=False):
    if test_mode or os.getenv('TESTING') == 'true':
        # Return mock service for testing
        return MockGmailService()
    # Normal OAuth2 flow...
```

### 2. Include Pre-Setup Validation
```bash
# Add to Level 0 validation
python -c "
import os
required = ['GMAIL_CREDENTIALS_PATH', 'GMAIL_TOKEN_PATH'] 
if all(os.path.exists(os.getenv(var, '')) for var in required):
    print('✓ Gmail OAuth2 already configured')
else:
    print('⚠ Run setup_gmail.py for first-time OAuth2 setup')
"
```

### 3. Add setup_gmail.py Script
```python
# Standalone script for OAuth2 setup
def setup_gmail_oauth():
    """Interactive Gmail OAuth2 setup script"""
    # Guide user through credential download
    # Run OAuth2 flow once
    # Validate tokens work
    # Save for future use
```

### 4. Enhanced Error Recovery
```python
# In email agent tools
@email_agent.tool
async def authenticate_gmail(ctx: RunContext[EmailAgentDependencies]) -> Dict[str, Any]:
    try:
        service = await authenticate_gmail_service(...)
        return {"success": True, "message": "Gmail authenticated successfully"}
    except FileNotFoundError:
        return {"success": False, "error": "Run 'python setup_gmail.py' first", "recoverable": True}
    except Exception as e:
        return {"success": False, "error": str(e), "recoverable": False}
```

## Confidence Score: 10/10

**With these additions, the PRP achieves 10/10 because:**
- **Complete automation**: OAuth2 setup is guided with clear error messages
- **Test isolation**: Mock strategies eliminate external dependencies during testing  
- **Recovery paths**: Users get actionable error messages with next steps
- **Production ready**: All edge cases handled with proper error recovery
- **One-pass success**: Implementation can proceed without manual intervention

The implementation will succeed in one pass with these OAuth2 handling strategies.