---
name: data-check-quality
description: >
  Read when executing data profiling, verifying dataframe schemas, or validating data quality constraints.
  Do not read when dataset validation is not requested.
---

# Data Quality Checker

Runs checks for null thresholds, schema drift, and data anomalies.

## Steps
1. Write a helper script testing for schema expectations, null counts, and column types.
2. Execute the verification and generate a data quality report.
