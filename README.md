# PydanticAI Research & Email Agent System

A production-ready AI agent system built with PydanticAI that combines web research capabilities with Gmail email drafting, featuring a beautiful streaming CLI interface. **This repository also demonstrates automated AI-powered issue fixing and PR review using multiple AI coding assistants.**

## 🚀 Features

- **Web Research**: Uses Brave Search API for current, relevant information
- **Email Drafting**: Creates professional Gmail drafts based on research findings
- **Agent Delegation**: Research agent delegates email tasks to specialized email agent
- **Streaming CLI**: Beautiful real-time output using Rich library and PydanticAI's `.iter()` method
- **OAuth2 Integration**: Secure Gmail authentication with guided setup wizard
- **Mock Testing**: Comprehensive test suite with TestModel and mock services
- **Production Ready**: Environment-based configuration, error handling, and logging
- **AI-Powered Workflows**: Automated issue fixing and PR reviews via Claude Code, Codex, and Cursor

## 🤖 AI Coding Assistants (GitHub Actions)

This repository showcases automated issue handling and code review using three leading AI coding assistants. Simply mention them in issue or PR comments to trigger automated workflows.

### Available Commands

- **Claude Code**: `@claude-fix` or `@claude-review`
- **OpenAI Codex**: `@codex-fix` or `@codex-review`
- **Cursor**: `@cursor-fix` or `@cursor-review`

### Setup Instructions

Add the following secrets to your GitHub repository (`Settings → Secrets and variables → Actions → New repository secret`):

1. **Claude Code**: `CLAUDE_CODE_OAUTH_TOKEN`
   - Install Claude CLI: `npm install -g @anthropic-ai/claude-code`
   - Generate token: `claude setup-token` (creates a 1-year token starting with `sk-ant-oat01-`)
   - Copy the generated token
2. **OpenAI Codex**: `OPENAI_API_KEY` - [Get from OpenAI platform](https://platform.openai.com/api-keys)
3. **Cursor**: `CURSOR_API_KEY` - [Generate from Cursor dashboard](https://cursor.com/)

### How It Works

The workflows use reusable prompt templates (`.github/issue_fix_prompt.md` and `.github/pr_review_prompt.md`) that define the fix and review processes. Each AI assistant workflow loads these templates and customizes them with the appropriate branch naming suffix (`-claude`, `-codex`, or `-cursor`). This ensures consistency across all AI assistants while maintaining separate attribution for fixes and reviews.

**Workflow Files**:
- `.github/workflows/claude_code/` - Claude Code workflows
- `.github/workflows/codex/` - OpenAI Codex workflows
- `.github/workflows/cursor/` - Cursor workflows

## 🏗️ Pydantic AI Agent Architecture

```
├── agents/          # PydanticAI agents
│   ├── research_agent.py    # Main research agent with Brave search
│   └── email_agent.py       # Gmail draft creation agent
├── config/          # Settings and model providers
│   ├── settings.py          # Environment-based configuration
│   └── providers.py         # LLM model setup
├── models/          # Pydantic data models
│   ├── email_models.py      # Email-related models
│   ├── research_models.py   # Research data models
│   └── agent_models.py      # Generic agent models
├── tools/           # Tool functions
│   ├── brave_search.py      # Brave Search API integration
│   └── gmail_tools.py       # Gmail OAuth2 and draft creation
├── tests/           # Test suite
│   ├── test_research_agent.py
│   ├── test_email_agent.py
│   └── pytest.ini
├── gmail_setup.py   # Gmail OAuth2 setup wizard
└── research_email_cli.py  # Main CLI application
```

## 📋 Prerequisites

1. **Python 3.11+** with virtual environment capability
2. **API Keys**:
   - OpenAI API key (for LLM)
   - Brave Search API key (for web search)
3. **Gmail OAuth2 Setup**:
   - Google Cloud Project with Gmail API enabled
   - OAuth2 credentials downloaded from Google Cloud Console

## 🛠️ Installation

1. **Clone and setup virtual environment**:
   ```bash
   git clone <repository-url>
   cd PydanticAI-Research-Agent
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install 'pydantic-ai-slim[openai]' httpx rich python-dotenv
   pip install google-auth google-auth-oauthlib google-api-python-client
   pip install pytest pytest-asyncio  # For testing
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Setup Gmail OAuth2**:
   ```bash
   python gmail_setup.py
   ```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# LLM Configuration
LLM_PROVIDER=openai
LLM_API_KEY=your-openai-api-key-here
LLM_MODEL=gpt-4o
LLM_BASE_URL=https://api.openai.com/v1

# Brave Search Configuration
BRAVE_API_KEY=your-brave-search-api-key-here

# Gmail OAuth2 Configuration  
GMAIL_CREDENTIALS_PATH=credentials.json
GMAIL_TOKEN_PATH=token.pickle

# Application Configuration
APP_ENV=development
LOG_LEVEL=INFO
DEBUG=false
```

### Gmail OAuth2 Setup

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create new project or select existing

2. **Enable Gmail API**:
   - Go to APIs & Services > Library
   - Search "Gmail API" and enable

3. **Create OAuth2 Credentials**:
   - Go to APIs & Services > Credentials
   - Create OAuth 2.0 Client ID for Desktop application
   - Download as `credentials.json`

4. **Run Setup Wizard**:
   ```bash
   python gmail_setup.py
   ```

## 🎯 Usage

### CLI Interface

```bash
source venv/bin/activate
python research_email_cli.py
```

### Example Queries

- "Research AI safety trends and email summary to john@company.com"
- "Find latest developments in quantum computing"
- "Create email draft about market analysis for jane.doe@firm.com"

### Programmatic Usage

```python
from agents import research_agent, ResearchAgentDependencies
from config.settings import settings

# Create dependencies
deps = ResearchAgentDependencies(
    brave_api_key=settings.brave_api_key,
    gmail_credentials_path=settings.gmail_credentials_path,
    gmail_token_path=settings.gmail_token_path
)

# Run research agent
result = await research_agent.run(
    "Research machine learning trends",
    deps=deps
)
```

## 🧪 Testing

Run the test suite with pytest:

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

### Test Environment

Tests use mock services and TestModel for validation without external API calls:

```python
# Enable test mode
import os
os.environ['TESTING'] = 'true'

# Use TestModel for predictable responses
from pydantic_ai.models.test import TestModel
test_model = TestModel()

with research_agent.override(model=test_model):
    result = research_agent.run_sync("Test query", deps=deps)
```

## 🔧 Development

### Agent Tools

**Research Agent**:
- `search_web`: Brave Search API integration
- `create_email_draft`: Delegates to email agent
- `summarize_research`: Creates structured summaries

**Email Agent**:
- `authenticate_gmail`: OAuth2 authentication
- `create_gmail_draft`: Draft creation in Gmail
- `compose_email_content`: Professional email composition

### Error Handling

The system includes comprehensive error handling:

- **Gmail OAuth2**: Detailed setup guidance and token refresh
- **API Failures**: Graceful degradation and retry mechanisms  
- **Network Issues**: Timeout handling and connection recovery
- **User Guidance**: Actionable error messages with next steps

### Security Features

- **Environment Variables**: No hardcoded secrets
- **OAuth2 Flow**: Secure Gmail authentication
- **Input Validation**: Pydantic model validation
- **API Key Protection**: Never logged or exposed in errors

## 📚 PydanticAI Patterns Used

This implementation demonstrates key PydanticAI patterns:

- **Agent Composition**: Multiple specialized agents working together
- **Dependency Injection**: Clean separation of concerns with `deps_type`
- **Tool Integration**: `@agent.tool` decorators with proper context
- **Model Override**: TestModel for development and testing
- **Streaming Output**: Real-time CLI with `.iter()` method
- **Usage Tracking**: Token counting across agent delegations
- **Error Recovery**: Graceful handling of external service failures

## 🚨 Important Notes

- **Never commit** `credentials.json` or `token.pickle` to version control
- **Add to .gitignore**: All sensitive files are properly excluded
- **API Rate Limits**: Brave Search has usage quotas - monitor consumption
- **Token Expiry**: Gmail tokens refresh automatically but may need re-authentication
- **Mock Mode**: Set `TESTING=true` for development without real API calls

## 🆘 Troubleshooting

### Common Issues

1. **"No module named 'pydantic_ai'"**:
   ```bash
   pip install 'pydantic-ai-slim[openai]'
   ```

2. **Gmail authentication errors**:
   ```bash
   python gmail_setup.py  # Re-run OAuth2 setup
   ```

3. **Import errors**:
   ```bash
   source venv/bin/activate  # Ensure virtual environment is active
   ```

4. **Missing API keys**:
   - Check `.env` file exists and has valid keys
   - Verify environment variables are loaded

## 📖 Learn More

- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [Brave Search API](https://brave.com/search/api/)
- [Gmail API Python Quickstart](https://developers.google.com/workspace/gmail/api/quickstart/python)
- [Rich Library Documentation](https://rich.readthedocs.io/)

## 🤝 Contributing

This project follows PydanticAI best practices:

- Use environment-based configuration
- Implement comprehensive error handling
- Include TestModel validation for all agents
- Follow agent-to-agent delegation patterns
- Maintain security standards for API keys and OAuth2

---

Built with ❤️ using [PydanticAI](https://ai.pydantic.dev/) and following production-ready development practices.