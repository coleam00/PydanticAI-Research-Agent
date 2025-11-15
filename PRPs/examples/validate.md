Run comprehensive validation of the PydanticAI Research Agent, including unit tests and intelligent end-to-end testing via the CLI.

## Phase 1: Unit Test Suite

Run the unit test suite to verify component-level functionality:

```bash
uv run python -m pytest tests/ -v
```

**Expected:** All tests pass

## Phase 2: Intelligent End-to-End Validation

**IMPORTANT:** Use the CLI (`cli.py`) to interact with the research agent as a real user would. Design and execute test queries dynamically based on:

1. **Agent capabilities** (web search, email drafting, research summarization)
2. **Common failure modes** (context access issues, API errors, tool execution failures)
3. **Edge cases** (empty results, malformed queries, dependency injection issues)
4. **Real-world usage patterns**

### Instructions for AI Assistant:

You should intelligently design 3-5 test queries that:
- Test the search tool with real queries (this will verify `ctx.deps.brave_api_key` works)
- Test different types of research requests
- Verify the agent handles errors gracefully
- Check that tools are properly registered and accessible

Run each query using:
```bash
uv run python cli.py --query "your test query here" --quiet
```

For each test:
- Analyze the output to verify success
- Check for errors or unexpected behavior
- Verify the agent actually executes tools (not just returns mock responses)

**Be creative and thorough** - design tests that would catch real production issues like:
- Incorrect RunContext attribute access (e.g., `ctx.brave_api_key` vs `ctx.deps.brave_api_key`)
- Tool registration problems
- Dependency injection failures
- API integration issues

## Summary Report

After both phases complete, provide a comprehensive report with:

### Unit Tests
- Total tests passed/failed
- Execution time
- Any warnings or deprecations

### E2E Validation via CLI
- Test queries you designed and why
- Results for each query (success/failure)
- Any errors or issues discovered
- Verification that tools actually executed

### Overall Assessment
**Status: ✅ PASS / ⚠️ WARNINGS / ❌ FAIL**

**Production Ready:** YES / NO

**Issues Found:** List any bugs, errors, or improvements needed

**Format the report clearly with status indicators and actionable insights**