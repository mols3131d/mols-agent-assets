---
name: data-analysis-builder
description: >
  Read when creating dataframes, cleaning columns, aggregating, or plotting data in Python (Pandas/Polars).
  Do not read for SQL schema modeling or distributed Spark pipelines.
---

# Data Analysis Builder

Writes high-performance Python data manipulation scripts.

## Goal

Implement vectorized, memory-efficient data cleaning and calculation scripts.

## Code Generation Steps

1. **Identify Source Format**: Determine source formats (Parquet, CSV, JSON) and target formats.
2. **Write Vectorized Logic**: Never use `iterrows()` or manual loops for Row-by-Row operations. Use vector maps, `.apply()` (in Polars, use expressions), or `.groupby()`.
3. **Schema Verification**: Explicitly type column names and cast types at entry boundaries.
4. **Validation**: Call `data-check-quality` to test dataframes.

## References Loaded

- [python-style-guide.md](../../references/python-style-guide.md) (Pythonic idioms)
- [performance-optimization.md](../../references/performance-optimization.md) (Loop optimization)
