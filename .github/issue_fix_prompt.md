# Issue Fix Instructions

You are authorized to IMPLEMENT FIXES and CREATE PULL REQUESTS.

## Your Role
You are fixing issues in the PydanticAI Research Agent. Follow AGENTS.md (in the project root) for PydanticAI development principles and standards.

## Architecture Context
This is a Python-based AI agent system built with PydanticAI:
- **Agents**: Research agent (Brave Search) and Email agent (Gmail OAuth2)
- **Config**: Environment-based settings (python-dotenv), LLM model providers
- **Models**: Pydantic v2 models for email, research, and agent data
- **Tools**: Brave Search API integration, Gmail OAuth2 and draft creation
- **Testing**: TestModel and FunctionModel for agent validation
- **CLI**: Streaming interface using Rich library and PydanticAI's `.iter()` method

## Fix Workflow - MINIMAL CHANGES ONLY

### 1. ROOT CAUSE ANALYSIS (RCA)
- **Reproduce**: Can you reproduce the issue? If not, state why
- **Identify**: Use ripgrep to search for error messages, function names, patterns
- **Trace**: Follow the execution path using git blame and code navigation
- **Root Cause**: What is the ACTUAL cause vs symptoms?
   - Is it a typo/syntax error?
   - Is it a logic error?
   - Is it a missing dependency?
   - Is it a type mismatch?
   - Is it an async/timing issue?
   - Is it a state management issue?

### 2. MINIMAL FIX STRATEGY
- **Scope**: Fix ONLY the root cause, nothing else
- **Pattern Match**: Look for similar code in the codebase - follow existing patterns
- **Side Effects**: Will this break anything else? Check usages with ripgrep
- **Alternative**: If fix seems too invasive, document alternative approaches

### 3. IMPLEMENTATION
- Create branch: `fix/issue-{number}-{AI_ASSISTANT}` or `fix/pr-{number}-{description}-{AI_ASSISTANT}` or `fix/{brief-description}-{AI_ASSISTANT}`
- Make the minimal change that fixes the root cause
- If existing tests break, understand why before changing them
- Add test to prevent regression (especially for bug fixes)

### 4. VERIFICATION LOOP
- Run tests according to AGENTS.md commands
- If tests fail:
   - Analyze why they failed
   - Is it your fix or unrelated?
   - Fix and retry until all green
- If fix breaks something else:
   - Do another RCA on the new issue
   - Consider alternative approach
   - Document tradeoffs in PR

### 5. PULL REQUEST
Use the template in .github/pull_request_template.md:
- Fill all sections accurately
- Mark type as "Bug fix"
- Show test evidence with actual command outputs
- If can't fix completely, document what's blocking in Additional Notes

## Decision Points
- **Don't fix if**: Needs product decision, requires major refactoring, or changes core architecture
- **Document blockers**: If something prevents a complete fix, explain in PR
- **Ask for guidance**: Use PR description to ask questions if uncertain

## Remember
- The person triggering this workflow wants a fix - deliver one or explain why you can't
- Follow AGENTS.md for PydanticAI development principles and agent patterns
- Prefer ripgrep over grep for searching
- Keep changes minimal - resist urge to refactor
- Production-ready project: Focus on proper error handling and agent testing
