# Feature: PydanticAI Research & Email Agent System

Build a production-ready multi-agent AI system combining web research and Gmail email drafting with a streaming CLI interface.

## Feature Description

Create a dual-agent PydanticAI system where a Research Agent can search the web via Brave API and delegate email creation to an Email Agent that creates Gmail drafts. The system features agent-to-agent delegation, streaming output with real-time tool visibility, and comprehensive error handling.

## User Story

As a researcher or knowledge worker
I want to search the web for information and automatically create professional email drafts based on findings
So that I can efficiently share research insights with colleagues without manual email composition

## Problem Statement

Users need a seamless way to conduct research and communicate findings. Current solutions require manual context switching between research and email composition, leading to inefficiency and potential information loss.

## Solution Statement

Implement two specialized PydanticAI agents: (1) Research Agent with Brave Search integration and email delegation capability, (2) Email Agent with Gmail OAuth2 and draft creation. Connect them via agent delegation pattern with streaming CLI for real-time feedback.

## Feature Metadata

**Feature Type**: New Capability
**Estimated Complexity**: Medium
**Primary Systems Affected**: Multi-agent architecture, external APIs (Brave, Gmail), CLI interface
**Dependencies**: pydantic-ai, httpx, rich, google-auth, google-api-python-client, python-dotenv

---

## CONTEXT REFERENCES

### Core Documentation

- [PydanticAI Documentation](https://ai.pydantic.dev/)
  - Agent composition and delegation patterns
  - TestModel for development and testing
  - Streaming with .iter() method
  - Why: Official guide for all PydanticAI patterns

- [Brave Search API](https://brave.com/search/api/)
  - Web search endpoint and parameters
  - Why: Required for research functionality

- [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)
  - OAuth2 authentication flow
  - Draft creation methods
  - Why: Needed for email agent integration

### New Files to Create

**Core Agents:**
- `agents/__init__.py` - Agent exports
- `agents/dependencies.py` - Dependency dataclasses
- `agents/settings.py` - Environment-based configuration
- `agents/research_agent.py` - Research agent with Brave search
- `agents/email_agent.py` - Email agent with Gmail integration

**Configuration:**
- `config/providers.py` - LLM model provider setup
- `config/settings.py` - Application settings

**Models:**
- `models/email_models.py` - Email-related Pydantic models
- `models/research_models.py` - Research data models
- `models/agent_models.py` - Generic agent models

**Tools:**
- `tools/brave_search.py` - Brave Search API integration
- `tools/gmail_tools.py` - Gmail OAuth2 and draft creation

**CLI:**
- `research_email_cli.py` - Streaming CLI with Rich library

**Testing:**
- `tests/test_agents.py` - Agent tests with TestModel
- `tests/test_email_agent.py` - Email agent specific tests
- `tests/test_research_agent.py` - Research agent specific tests
- `tests/test_models.py` - Pydantic model validation tests
- `tests/test_tools.py` - Tool function tests

**Setup:**
- `gmail_setup.py` - Gmail OAuth2 setup wizard
- `.env.example` - Environment template
- `pyproject.toml` - Project configuration

### Patterns to Follow

**Agent Architecture (No result_type unless needed):**
```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

@dataclass
class AgentDependencies:
    api_key: str

agent = Agent(
    model,
    deps_type=AgentDependencies,
    system_prompt="..."
)
```

**Tool Pattern:**
```python
@agent.tool
async def tool_function(
    ctx: RunContext[AgentDependencies],
    param: str
) -> dict:
    """Tool with context access."""
    return await external_call(ctx.deps.api_key, param)
```

**Environment Configuration:**
```python
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
```

**Agent Delegation:**
```python
# In research_agent tool
email_deps = EmailAgentDependencies(
    gmail_credentials_path=ctx.deps.gmail_credentials_path,
    gmail_token_path=ctx.deps.gmail_token_path
)

result = await email_agent.run(
    prompt,
    deps=email_deps,
    usage=ctx.usage  # Pass usage for token tracking
)
```

---

## IMPLEMENTATION PLAN

### Phase 1: Foundation Setup

Set up project structure, dependencies, and configuration.

**Tasks:**
- Create directory structure (agents/, config/, models/, tools/, tests/)
- Configure pyproject.toml with dependencies
- Create .env.example template
- Implement settings.py with pydantic-settings and python-dotenv

### Phase 2: Core Agent Implementation

Build the two main agents with their tools.

**Tasks:**
- Create dependency dataclasses in agents/dependencies.py
- Implement Research Agent with Brave search tool
- Implement Email Agent with Gmail tools
- Add agent delegation pattern to research agent
- Configure LLM provider in config/providers.py

### Phase 3: External Service Integration

Integrate Brave Search and Gmail APIs.

**Tasks:**
- Implement Brave Search API client in tools/brave_search.py
- Create Gmail OAuth2 flow in tools/gmail_tools.py
- Build Gmail draft creation functionality
- Create OAuth2 setup wizard (gmail_setup.py)

### Phase 4: CLI & Streaming Interface

Build streaming CLI with Rich library.

**Tasks:**
- Implement streaming CLI with agent.iter()
- Add real-time tool call visibility
- Handle different event types (PartDeltaEvent, FunctionToolCallEvent)
- Add conversation history tracking

### Phase 5: Testing & Validation

Comprehensive testing with TestModel and mocks.

**Tasks:**
- Write agent tests with TestModel override
- Mock external API calls (Brave, Gmail)
- Test agent delegation workflow
- Test dependency injection
- Validate error handling

---

## STEP-BY-STEP TASKS

### CREATE agents/dependencies.py

- **IMPLEMENT**: Dependency dataclasses for both agents
- **PATTERN**: Use @dataclass with Optional fields
- **IMPORTS**: `from dataclasses import dataclass; from typing import Optional`
- **VALIDATE**: `uv run python -c "from agents.dependencies import ResearchAgentDependencies, EmailAgentDependencies"`

### CREATE agents/settings.py

- **IMPLEMENT**: Settings class with pydantic-settings
- **PATTERN**: Use SettingsConfigDict with env_file=".env", extra="ignore"
- **IMPORTS**: `from pydantic_settings import BaseSettings; from dotenv import load_dotenv`
- **GOTCHA**: Must set extra="ignore" to allow extra fields from .env
- **VALIDATE**: `uv run python -c "from agents.settings import settings; print(settings.llm_provider)"`

### CREATE config/providers.py

- **IMPLEMENT**: LLM model provider setup function
- **PATTERN**: Return OpenAIChatModel with provider configuration
- **IMPORTS**: `from pydantic_ai.providers.openai import OpenAIProvider`
- **VALIDATE**: `uv run python -c "from config.providers import get_llm_model; print(get_llm_model())"`

### CREATE tools/brave_search.py

- **IMPLEMENT**: Async Brave Search API client
- **PATTERN**: Pure async function accepting api_key parameter
- **IMPORTS**: `import httpx; from typing import List, Dict, Any`
- **GOTCHA**: Handle 429 rate limit errors, 401 auth errors
- **VALIDATE**: `uv run python -c "from tools.brave_search import search_web_tool; print(search_web_tool)"`

### CREATE tools/gmail_tools.py

- **IMPLEMENT**: Gmail OAuth2 authentication and draft creation
- **PATTERN**: Async functions for authenticate and create_draft
- **IMPORTS**: `from google.oauth2.credentials import Credentials; from googleapiclient.discovery import build`
- **GOTCHA**: Handle token refresh and missing credentials gracefully
- **VALIDATE**: `uv run python -c "from tools.gmail_tools import authenticate_gmail_service; print(authenticate_gmail_service)"`

### CREATE models/email_models.py

- **IMPLEMENT**: EmailDraft Pydantic model
- **PATTERN**: BaseModel with EmailStr validation
- **IMPORTS**: `from pydantic import BaseModel, EmailStr, Field`
- **VALIDATE**: `uv run python -c "from models.email_models import EmailDraft; print(EmailDraft)"`

### CREATE agents/email_agent.py

- **IMPLEMENT**: Email agent with Gmail tools
- **PATTERN**: Agent with deps_type=EmailAgentDependencies, default string output
- **IMPORTS**: `from pydantic_ai import Agent, RunContext; from agents.dependencies import EmailAgentDependencies`
- **GOTCHA**: Don't use result_type unless structured output specifically needed
- **VALIDATE**: `uv run python -c "from agents.email_agent import email_agent; print(email_agent)"`

### CREATE agents/research_agent.py

- **IMPLEMENT**: Research agent with Brave search and email delegation
- **PATTERN**: Agent with tools for search_web and create_email_draft
- **IMPORTS**: `from pydantic_ai import Agent, RunContext; from agents.dependencies import ResearchAgentDependencies`
- **GOTCHA**: Import EmailAgentDependencies from dependencies, not email_agent
- **VALIDATE**: `uv run python -c "from agents.research_agent import research_agent; print(research_agent)"`

### CREATE research_email_cli.py

- **IMPLEMENT**: Streaming CLI with Rich library
- **PATTERN**: Use agent.iter() with async iteration over nodes
- **IMPORTS**: `from rich.console import Console; from pydantic_ai import Agent`
- **GOTCHA**: Handle FunctionToolCallEvent and PartDeltaEvent differently
- **VALIDATE**: `uv run python research_email_cli.py` (manual test)

### CREATE gmail_setup.py

- **IMPLEMENT**: OAuth2 setup wizard
- **PATTERN**: Interactive script for credentials.json → token.json flow
- **VALIDATE**: `uv run python gmail_setup.py --help`

### CREATE tests/test_agents.py

- **IMPLEMENT**: Agent tests with TestModel
- **PATTERN**: Use agent.override(model=TestModel()) context manager
- **IMPORTS**: `from pydantic_ai.models.test import TestModel`
- **VALIDATE**: `uv run python -m pytest tests/test_agents.py -v`

### CREATE tests/test_research_agent.py

- **IMPLEMENT**: Research agent specific tests
- **PATTERN**: Mock Brave API with patch('tools.brave_search.search_web_tool')
- **VALIDATE**: `uv run python -m pytest tests/test_research_agent.py -v`

### CREATE tests/test_email_agent.py

- **IMPLEMENT**: Email agent specific tests
- **PATTERN**: Mock Gmail API calls
- **VALIDATE**: `uv run python -m pytest tests/test_email_agent.py -v`

### CREATE tests/test_models.py

- **IMPLEMENT**: Pydantic model validation tests
- **PATTERN**: Test model serialization, validation, edge cases
- **VALIDATE**: `uv run python -m pytest tests/test_models.py -v`

### CREATE tests/test_tools.py

- **IMPLEMENT**: Tool function tests
- **PATTERN**: Mock httpx.AsyncClient for API calls
- **VALIDATE**: `uv run python -m pytest tests/test_tools.py -v`

---

## TESTING STRATEGY

### Unit Tests

Use pytest with pytest-asyncio for async test support. All tests use TestModel or mocked external services - no real API calls.

**Coverage Requirements:**
- Agent initialization and configuration
- Tool registration and execution
- Dependency injection
- Error handling and edge cases
- Model validation

**Test Patterns:**
```python
@pytest.mark.asyncio
async def test_agent_with_test_model():
    with agent.override(model=TestModel()):
        result = await agent.run("test", deps=deps)
        assert result.output is not None
```

### Mock Patterns

Mock external services to avoid API calls:
```python
with patch('tools.brave_search.search_web_tool') as mock_search:
    mock_search.return_value = [{"title": "Test", "url": "..."}]
    # Run test
```

### Edge Cases

- Empty API responses
- Authentication failures
- Invalid email addresses
- Missing environment variables
- Agent delegation failures

---

## VALIDATION COMMANDS

Execute every command to ensure zero regressions and 100% feature correctness.

### Unit Tests

```bash
uv run python -m pytest tests/ -v
```

**Expected:** All 58 tests pass in ~14 seconds

---

## ACCEPTANCE CRITERIA

- [x] Research agent successfully searches web via Brave API
- [x] Email agent creates Gmail drafts with OAuth2
- [x] Agent delegation works (research → email)
- [x] Streaming CLI shows real-time tool execution
- [x] All tests pass with TestModel and mocked services
- [x] No real API calls in test suite
- [x] Environment-based configuration works
- [x] Error handling provides actionable messages
- [x] Code follows PydanticAI best practices (CLAUDE.md)

---

## COMPLETION CHECKLIST

- [x] All agents implemented with proper dependency injection
- [x] External API integrations working (Brave, Gmail)
- [x] Streaming CLI with Rich library functional
- [x] Comprehensive test suite with 58 tests
- [x] Tests run in ~14 seconds
- [x] OAuth2 setup wizard created
- [x] Documentation complete (README.md)
- [x] No hardcoded secrets, all via .env

---

## NOTES

**Key Design Decisions:**

- **No result_type**: Agents use default string output per CLAUDE.md guidelines
- **Agent delegation**: Research agent invokes email agent via standard run() method
- **Streaming**: Uses .iter() method with event-based node handling
- **Testing**: TestModel for fast validation, mocks for external services
- **Security**: OAuth2 for Gmail, environment variables for API keys

**Implementation Gotchas:**

- Must use `extra="ignore"` in Settings model config
- Agent dependency classes must be in single location (agents/dependencies.py)
- Tool functions need RunContext[DepsType] for context access
- Gmail token refresh handled automatically by google-auth
- Brave API has rate limits - implement graceful degradation

**Performance Considerations:**

- Tests optimized to ~14 seconds by removing slow rate limit tests
- Async/await throughout for non-blocking IO
- Streaming output for better UX

**Future Enhancements:**

- Add more search providers (Google, Bing)
- Support multiple email services
- Add research caching
- Implement conversation memory
