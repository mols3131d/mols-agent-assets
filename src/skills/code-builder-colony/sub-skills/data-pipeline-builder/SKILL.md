---
name: data-pipeline-builder
description: >
  Read when writing ETL pipelines, database sync scripts, or Airflow/Prefect DAGs.
  Do not read for simple database querying or in-memory analysis.
---

# Data Pipeline Builder

Creates production-grade, fault-tolerant ETL workflows.

## Goal
Produce pipeline scripts that guarantee data consistency and allow safe re-runs.

## Code Generation Steps
1. **Enforce Idempotency**: Use Upsert (Merge Into) or dynamic Partition Overwrite. Never append without checks.
2. **Time Parameterization**: Bind filters to orchestrator execution timestamps. No hardcoded `datetime.now()`.
3. **Retry Strategy**: Implement exponential backoff for network extraction steps.
4. **Static Validation**: Run `pipeline-validate-dag` for Airflow integrations.

## References Loaded
- [design-principles.md](../../references/design-principles.md) (SoC)
- [robustness-and-safety.md](../../references/robustness-and-safety.md) (Secure injection, env secrets)
- [big-data-engineering.md](../../references/big-data-engineering.md) (Idempotency, Backfill)
