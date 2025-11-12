# PydanticAI Research & Email Agent

Production-ready agents that combine Brave-powered research with Gmail draft generation, packaged with a streaming CLI and the standard PydanticAI context-engineering workflow.

## Highlights
- Research agent delegates to a Gmail-focused email agent through PydanticAI tool calls
- Model configuration, dependencies, and secrets handled via `config/settings.py` and `.env`
- Streaming CLI (`research_email_cli.py`) built on Rich and `.iter()` for real-time output
- Tests rely on `TestModel`/mock services so you can develop without external calls
- GitHub workflows showcase automated fixes/reviews using Claude Code, Codex, and Cursor

## Quick Start
```bash
git clone <repository-url>
cd PydanticAI-Research-Agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # add OpenAI + Brave keys
python gmail_setup.py     # run once to store OAuth tokens
```

## Running the Agent
- **CLI:** `python research_email_cli.py` (prompts for a research task and recipient)
- **Programmatic use:**
  ```python
  from agents.research_agent import research_agent, ResearchAgentDependencies
  from config.settings import settings

  deps = ResearchAgentDependencies(
      brave_api_key=settings.brave_api_key,
      gmail_credentials_path=settings.gmail_credentials_path,
      gmail_token_path=settings.gmail_token_path,
  )
  result = research_agent.run_sync("Research machine learning trends", deps=deps)
  ```

## Configuration Essentials
- `.env` drives model provider selection, Brave API key, and Gmail credential paths
- `python gmail_setup.py` guides you through OAuth2 and saves tokens under `credentials/`
- `config/providers.py` exposes `get_llm_model()` for OpenAI/Anthropic/Gemini swaps

## Tests
```bash
source venv/bin/activate
python -m pytest -v
```
Set `TESTING=true` to force TestModel usage and skip external APIs during local runs.

## Project Layout
```
agents/         # research_agent.py, email_agent.py
config/         # settings.py, providers.py, dotenv handling
models/         # structured outputs for research + email flows
tools/          # Brave search + Gmail tool implementations
tests/          # pytest suite using TestModel overrides
research_email_cli.py
gmail_setup.py
```

## Automated Assistants
Mention an assistant in issues/PRs to trigger GitHub Actions:
- `@claude-fix`, `@codex-fix`, `@cursor-fix` for implementations
- `@claude-review`, `@codex-review`, `@cursor-review` for PR feedback

## Learn More
- [PydanticAI documentation](https://ai.pydantic.dev/)
- [Brave Search API](https://brave.com/search/api/)
- [Gmail API Quickstart](https://developers.google.com/workspace/gmail/api/quickstart/python)
