---
name: code-reviewer-colony
description: Code reviewer routing studio. Use when the user asks to review code changes, PR diffs, or audit software quality (architecture, implementation, performance, security, tests).
---

# Code Reviewer Colony

## Overview

- Perform specialized reviews of code changes and pull requests by routing tasks to focused sub-skills.

## Triggers

- User requests a code review, PR audit, or software quality check.

## Exclusions

- Code writing, bug fixing, or structural code modifications.

## Sub Skills

See [INDEX.csv](sub-skills/INDEX.csv)

## Constraints

- Identify modified files by running `python scripts/analyze_diff.py` (relative to this skill).
- Route tasks to the appropriate sub-skills by evaluating `keywords`, `trigger`, and `exclusion` in [INDEX.csv](sub-skills/INDEX.csv).
- Do not perform review audits directly in this master skill; delegate all auditing steps to the selected sub-skills.
- Consolidate findings from executed sub-skills into a unified final report.
