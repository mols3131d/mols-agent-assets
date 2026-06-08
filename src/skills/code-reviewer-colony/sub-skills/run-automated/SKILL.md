---
name: run-automated
description: Performs agent-led automated code reviews and generates structured code review reports.
---

# Automated Reviewer Skill

Procedural guidelines for performing autonomous code reviews and compiling findings into a structured report.

## Goal

Autonomously analyze a set of code changes, apply relevant review sub-skills, and output a comprehensive Code Review Report.

## Review Steps

1. **Perform Initial Diff Scan**:
   - Run the diff analyzer helper script: `python scripts/analyze_diff.py` (relative to the reviewer root).
   - Capture the output to identify which specialized review categories apply.

2. **Run Specialized Audits**:
   - For each recommended review category, execute its specific sub-skill:
     - **Architecture**: Audit code layouts, naming patterns, and dependency flows.
     - **Implementation**: Inspect core logic correctness, clean code standards, and error boundaries.
     - **Performance**: Scan for database bottlenecks (N+1 queries), loop complexity, and leakages.
     - **Security**: Scan for secrets leakage, input injection risks, and authorization missing checks.
     - **Tests**: Evaluate test presence, assertions, and mock isolation.

3. **Compile and Format Report**:
   - Consolidate all findings into a Markdown report.
   - Organize the feedback by severity:
     - **Blockers**: Critical bugs, security vulnerabilities, or resource leaks.
     - **Major**: Architecture violations or missing tests.
     - **Suggestions**: Enhancements, style tips, or performance optimizations.
   - Provide concrete, copy-pasteable code suggestions to fix identified problems.
   - Refer to guidelines in [principles.md](../../references/principles.md).
