Updated the Gmail token handling to default to `token.json` and made the setup/runtime tooling honor that extension while still accepting legacy pickle tokens.

**Changes**
- `.env.example:10-12`, `config/settings.py:37-39`, and `examples/main_agent_reference/settings.py:36-38` now default `GMAIL_TOKEN_PATH` to `token.json` so new environments align with the OAuth output.
- `gmail_setup.py:26-53,134-205,250-266` adds shared helpers that save/load credentials as JSON by default (with pickle fallback), updates the setup wizard defaults, and refreshes the security copy to mention `token.json`.
- `tools/gmail_tools.py:63-148` mirrors the JSON-aware load/save helpers so the runtime agent can read existing pickle tokens and write JSON tokens going forward.
- `README.md:122-125,257-258` reflects the new `.env` guidance and security note.
- Test fixtures and assertions in `tests/test_email_agent.py:16-94` and `tests/test_research_agent.py:16-88` now expect `token.json`, matching the new defaults.

**Testing**
- `pytest tests/test_email_agent.py tests/test_research_agent.py` *(fails: `pytest` not installed in runner environment).*

**Next Steps**
1. Install pytest in the runner (`pip install pytest`) and rerun the targeted suite to confirm the updates.
2. Regenerate Gmail credentials via `gmail_setup.py` if you currently rely on a pickle token and want to migrate to JSON.