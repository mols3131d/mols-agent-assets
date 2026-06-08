---
name: code-reviewer-colony
description: Code reviewer routing studio. Use when the user asks to review code changes, PR diffs, or audit software quality (architecture, implementation, performance, security, tests).
---

# Code Reviewer Colony

Goal: Perform specialized reviews of code changes and pull requests by routing tasks to focused sub-skills.

## Flow

1. **Detect Changes**: Identify modified files and directories. You can run the helper script `python scripts/analyze_diff.py` (relative to this skill) to scan the diff and categorize changes automatically.
2. **Consult Index**: Read `sub-skills/INDEX.csv` to identify which specialized review sub-skills apply to the changes.
3. **Execute Sub-Skills**: View and execute the appropriate sub-skills:
   - `reviewer-architecture` for structure and naming.
   - `reviewer-implementation` for logic and readability.
   - `reviewer-performance` for efficiency and database concerns.
   - `reviewer-security` for input validation and secrets.
   - `reviewer-test` for test coverage and mock quality.
   - `reviewer-automated` for agent-led reviews and report generation.
   - `reviewer-assistant` for human-led review queries.
4. **Consolidate Comments**: Aggregate the findings into a clear, actionable review summary.

## Rules

- **Focus**: Review only changed code and directly impacted dependencies.
- **Actionable**: Every critical comment must explain *why* it is an issue and suggest *how* to fix it.
- **Tone**: Keep critiques constructive, objective, and professional.
- **Output Format**: Group comments by severity:
  - **Blocker**: Security vulnerabilities, bugs, or severe performance leaks.
  - **Major**: Architecture violations, missing critical tests, or poor readability.
  - **Suggestion**: Minor optimization opportunities or style improvements.
