---
name: code-builder-colony
description: Code builder routing studio. Use when the user asks to write, modify, refactor, test, or validate Python code, data pipelines, big data queries, or database schemas.
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

See [INDEX.csv](sub-skills/INDEX.csv)

## Constraints

- Route requests to the most specific sub-skill by evaluating `keywords`, `trigger`, and `exclusion` in [INDEX.csv](sub-skills/INDEX.csv).
- Do not execute code modifications directly in this master skill; delegate all execution steps to the selected sub-skill.
- Make the smallest focused change required (Minimal Diff).
