# Prime for Tool Development

Load tool development patterns from Module 3 to prepare for building agent tools and do the rest of the priming.

## Context

You are about to work on building or modifying agent tools that will be used by Pydantic AI agents. Load the comprehensive patterns and best practices we established for writing agent-optimized tool docstrings and do the regular priming outlined below too.

## Read

Read the tool docstring patterns: @.agents/reference/adding_tools_guide.md

## Process

### 1. For the tool guide, understand and internalize:

1. **Core Philosophy** - How agent tool docstrings differ from standard docstrings
2. **7 Required Elements** - One-line summary, "Use this when", "Do NOT use", Args with guidance, Returns, Performance Notes, Examples
3. **Agent Perspective** - Writing for LLM comprehension and tool selection
4. **Token Efficiency** - Documenting token costs and optimization strategies
5. **Anti-patterns** - Common mistakes that confuse agents
6. **Template Structure** - The exact format to follow

Pay special attention to:

- "Use this when" (affirmative guidance for tool selection)
- "Do NOT use" (negative guidance to prevent tool confusion)
- Performance Notes (token costs, execution time, limits)
- Realistic examples (not "foo", "bar", "test.md")

### 2. Analyze Project Structure

List all tracked files:
!`git ls-files`

Show directory structure:
On Linux, run: `tree -L 3 -I 'node_modules|__pycache__|.git|dist|build'`

### 3. Read Core Documentation

- Read CLAUDE.md or similar global rules file
- Read README files at project root and major directories
- Read any architecture documentation

### 4. Identify Key Files

Based on the structure, identify and read:
- Main entry points (main.py, index.ts, app.py, etc.)
- Core configuration files (pyproject.toml, package.json, tsconfig.json)
- Key model/schema definitions
- Important service or controller files

### 5. Understand Current State

Check recent activity:
!`git log -10 --oneline`

Check current branch and status:
!`git status`

## Output Report

Provide a concise summary covering:

### Project Overview
- Purpose and type of application
- Primary technologies and frameworks
- Current version/state

### Architecture
- Overall structure and organization
- Key architectural patterns identified
- Important directories and their purposes

### Tech Stack
- Languages and versions
- Frameworks and major libraries
- Build tools and package managers
- Testing frameworks

### Core Principles
- Code style and conventions observed
- Documentation standards
- Testing approach

### Current State
- Active branch
- Recent changes or development focus
- Any immediate observations or concerns

**Make this summary easy to scan - use bullet points and clear headers.**