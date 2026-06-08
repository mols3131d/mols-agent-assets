---
name: code-builder-colony
description: Code builder routing studio. Use when the user asks to write, modify, refactor, test, or validate Python code, data pipelines, big data queries, or database schemas.
---

# Code Builder Colony

Goal: Generate, modify, refactor, and test Python code, data analysis scripts, database schemas, and ETL pipelines by routing tasks to specialized sub-skills.

## Flow

1. **Analyze Request**: Understand the domain and scope of the user's request (e.g., general Python, Pandas/Polars dataframes, ETL workflows, Spark/Big Data, database modeling, or writing tests).
2. **Consult Index**: Read [INDEX.csv](sub-skills/INDEX.csv) to identify which builder or common utility sub-skills apply to the task.
3. **Execute Sub-Skills**: View and execute the appropriate sub-skills:
   - `python-builder` for general Python classes, backend APIs, and logic.
   - `data-analysis-builder` for Pandas/Polars dataframe operations.
   - `data-pipeline-builder` for ETL pipelines and Airflow/Prefect workflows.
   - `big-data-builder` for PySpark and large-scale query optimization.
   - `data-modeling-builder` for SQLAlchemy ORMs, Pydantic schemas, and DDL migrations.
   - `test-builder` for pytest test suites.
   - `python-run-linter`, `test-run-pytest`, and `data-check-quality` for common formatting and validation tasks.
4. **Format & Verify**: Run linting, formatting, and tests using the common utility sub-skills to ensure code quality.

## Rules

- **Minimal Scope**: Route to the narrowest sub-skill that fits the request. Do not load unnecessary sub-skills into context.
- **Reference Check**: Check the `Applicability` section of any loaded reference files before implementing code to avoid over-engineering.
- **Minimal Diff**: Make the smallest correct change required to achieve the goal.
