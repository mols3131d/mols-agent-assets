---
name: code-builder-colony
description: >
  Read when the user asks to write, modify, refactor, test, or validate Python code, data pipelines, big data queries, or database schemas.
  Do not read for code review requests with no modification requests, or non-Python code changes.
---

# Code Builder Colony

## Overview

- Generate, modify, refactor, and test Python code, data analysis scripts, database schemas, and ETL pipelines by routing tasks to specialized sub-skills.

## Triggers

- User asks to create, modify, refactor, optimize, or write tests for Python code, data pipelines, or database schemas.

## Exclusions

- Non-Python code modifications (unless part of a configuration file).
- Pure code review requests with no modification requests.

## Sub Skills

Read [INDEX.csv](sub-skills/INDEX.csv) to identify all matching sub-skills for the request.
- Multi-skill routing: If the request spans multiple categories, select and execute matching sub-skills sequentially.
- Workflow: Load instructions for all matched sub-skills → Plan a step-by-step sequence → Execute and report progress.

## Constraints

- Route requests to the most specific sub-skills by evaluating `keywords`, `trigger`, and `exclusion` in [INDEX.csv](sub-skills/INDEX.csv).
- If a request matches multiple sub-skills, load and execute all relevant sub-skills in sequence.
- Do not execute code modifications directly in this master skill; delegate all execution steps to the selected sub-skills.
