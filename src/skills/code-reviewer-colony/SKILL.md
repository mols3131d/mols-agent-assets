---
name: code-reviewer-colony
description: >
  Read when the user requests a code review, PR audit, or software quality check.
  Do not read for code writing, bug fixing, or structural code modifications.
---

# Code Reviewer Colony

## Overview

- Perform specialized reviews of code changes and pull requests by routing tasks to focused sub-skills.

## Triggers

- User requests a code review, PR audit, or software quality check.

## Exclusions

- Code writing, bug fixing, or structural code modifications.

## Sub Skills

Read [INDEX.csv](sub-skills/INDEX.csv) to identify all matching sub-skills for the request.
- Multi-skill routing: If the request spans multiple categories, select and execute matching sub-skills sequentially.
- Workflow: Load instructions for all matched sub-skills → Plan a step-by-step sequence → Execute and report progress.

## Constraints

- Route tasks to the appropriate sub-skills by evaluating `keywords`, `trigger`, and `exclusion` in [INDEX.csv](sub-skills/INDEX.csv).
- If a request matches multiple sub-skills, load and execute all relevant sub-skills in sequence.
- Do not perform review audits directly in this master skill; delegate all auditing steps to the selected sub-skills.
