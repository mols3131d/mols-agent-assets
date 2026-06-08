---
name: big-data-engineering
description: >
  Read when designing distributed pipelines, processing datasets >10GB, structuring partition/bucket storage layouts, or stream processing.
  Do not read for memory-safe datasets (<10GB) or simple in-memory scripts (e.g., pandas DataFrame writes).
---

# Big Data Engineering Principles

High-density, technology-agnostic guidelines for processing, storage, and pipeline reliability.

## Applicability

- **Apply When**: Processing datasets exceeding single-node memory capacity, building production ETL/ELT pipelines, or developing event-driven streaming applications.
- **Do Not Apply To**: Small utility scripts, local file converters, or processing datasets under 10GB where simple in-memory operations (e.g., in-memory DataFrames, local file writes) are sufficient and more efficient.

## 1. Distributed Processing Optimization

- **Shuffle Mitigation**: Shuffling is the primary network bottleneck. Filter early, aggregate locally before transfer, and leverage map-side combines.
- **Join Strategy Selection**:
  - *Broadcast Join*: Use when one dataset fits in memory. Zero network shuffle.
  - *Sort-Merge Join*: Use for dual-large datasets. Require pre-sorted, bucketed keys to minimize partition scanning.
- **Data Skew Control**: Prevent single-node hotspots. Mitigate via *Salting* (appending randomized suffixes to hot keys) or AQE skew splitting.

## 2. Storage & Schema Design

- **Layout Hierarchy**:
  - *Partitioning*: Group directories by low-cardinality keys (e.g., `date`, `region`). Avoid high-cardinality partitioning (e.g., `uuid`, `timestamp`) to prevent metadata bottlenecks.
  - *Bucketing*: Distribute files evenly via hash values of join/group-by keys to speed up co-located joins.
- **Small File Avoidance**: Merge partitions periodically (Compaction) to maintain target file sizes of **256MB–1GB**, minimizing directory scanning overhead.
- **ACID Transaction Layer**: Use atomic commit logs to enable concurrent readers/writers, time travel (snapshot isolation), and schema evolution.

## 3. Idempotency & Backfill Patterns

- **Idempotent Storage Updates**:
  - Avoid insert-only structures. Use **Upsert/Merge** patterns with unique business keys.
  - For batch runs, use atomic partition-overwrite rather than whole-table append.
- **Time Parameterization**: Never use system-time (`now()`) inside pipelines. Enforce execution time parameters (`execution_date`) supplied by the orchestrator to isolate batch boundaries.

## 4. Streaming Mechanics

- **Watermark & State Cleanup**: Enforce watermark thresholds on event-time windows to discard late-arriving records and reclaim state store memory.
- **Exactly-Once Semantics (EOS)**: Guarantee using two-phase commit protocols or consumer-side idempotent sinks.
- **Backpressure & Flow Control**: Align ingestion rates dynamically with downstream processing throughput to prevent out-of-memory (OOM) failures.
