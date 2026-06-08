---
name: big-data-builder
description: >
  Read when processing datasets >10GB, tuning SQL queries, or writing PySpark tasks.
  Do not read for small local datasets (<10GB) or simple backend APIs.
---

# Big Data Builder

Optimizes query layouts and distributed calculations.

## Goal
Prevent network bottlenecks, out-of-memory errors, and processing skew on large datasets.

## Code Generation Steps
1. **Optimize Joins**: Apply Broadcast joins for small tables; ensure sorted-bucket keys for Sort-Merge joins.
2. **Reduce Shuffling**: Minimize wide transformations. Filter/select columns before join/groupby.
3. **Partition Strategically**: Layout folders by low-cardinality keys. Avoid partitioning by high-cardinality values.
4. **Data Skew Control**: Apply salting/AQE adjustments to hot partition keys.

## References Loaded
- [performance-optimization.md](../../references/performance-optimization.md) (N+1 query, loop caching)
- [big-data-engineering.md](../../references/big-data-engineering.md) (Shuffling, Skew, Compaction, Streaming)
