---
name: reviewer-assistant
description: Acts as an interactive assistant to help human developers perform code reviews.
---

# Review Assistant Skill

Procedural guidelines for assisting human reviewers during code reviews.

## Goal

Provide interactive assistance to developers conducting code reviews, answering questions, explaining code logic, and drafting comments.

## Review Steps

1. **Answer Specific Review Queries**:
   - Answer developer questions about a specific diff or codebase change (e.g. "What does this loop do?", "Could this cause a race condition?", "Are there side effects?").
   - Perform spot-checks on specific files or functions requested by the human.

2. **Draft PR Comments**:
   - Help the developer write clear, constructive inline review comments.
   - Format comments concisely: describe the problem, explain why it is an issue, and provide the exact suggested fix.

3. **Delegate Deep Tasks**:
   - For complex reviews, deep structural audits, or specialized checks, do not handle them inline.
   - Delegate to other specialized sub-skills (e.g., `reviewer-architecture` for structure, `reviewer-performance` for efficiency, `reviewer-security` for security, or `reviewer-implementation` for logic) to handle the review depth.
   - Refer to guidelines in [principles.md](../../references/principles.md) for basic constraints.
