---
name: code-builder-colony
description: Code builder routing studio. Use when the user asks to write, modify, refactor, test, or validate Python code, data pipelines, big data queries, or database schemas.
---

# Code Builder Colony

Goal: Generate, modify, refactor, and test Python code, data analysis scripts, database schemas, and ETL pipelines by routing tasks to specialized sub-skills.

## Flow

1. **Analyze Request**: Understand the domain and scope of the user's request (e.g., Python backend, Pandas/Polars, ETL workflows, Spark/Big Data, database modeling, or writing tests).
2. **Consult Index**: Read [INDEX.csv](sub-skills/INDEX.csv) to identify the appropriate sub-skill based on `keywords`, `trigger`, and `exclusion`.
3. **Execute Sub-Skill**: View and execute only the selected sub-skill instruction.
4. **Format & Verify**: Run linting, formatting, and test execution using the common utility sub-skills listed in the index to ensure code quality.

## Rules

- **Minimal Scope**: Route to the narrowest sub-skill that fits the request by evaluating `sub-skills/INDEX.csv`. Do not load multiple sub-skills into context.
- **Reference Check**: Check the `Applicability` section of any loaded reference files before implementing code to avoid over-engineering.
- **Minimal Diff**: Make the smallest correct change required to achieve the goal.
