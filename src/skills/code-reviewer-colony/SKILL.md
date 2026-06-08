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

See [INDEX.csv](sub-skills/INDEX.csv)

## Constraints

- Route tasks to the appropriate sub-skills by evaluating `keywords`, `trigger`, and `exclusion` in [INDEX.csv](sub-skills/INDEX.csv).
- Do not perform review audits directly in this master skill; delegate all auditing steps to the selected sub-skills.
