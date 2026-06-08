---
name: performance-optimization
description: >
  Read when optimizing network/database queries (ORMs), managing asynchronous operations, concurrent threading, or lock timeouts.
  Do not read for synchronous, compute-bound scripts without network or database I/O.
---

# Performance Optimization Guide

Key standards for asynchronous efficiency, concurrency control, and database performance.

## Applicability

- **Apply When**: Handling network operations, database queries (especially ORMs), file systems, multi-threaded/asynchronous operations, or loops that contain potentially slow calls.
- **Do Not Apply To**: Strictly synchronous, local, compute-bound scripts with no I/O boundaries where async patterns or db optimizations would add redundant overhead.


## 1. Asynchronous & Concurrency Control

- **Non-blocking I/O**: Use `async`/`await` or Promise-based mechanisms for network requests, database queries, and file system tasks to prevent blocking thread execution.
- **Parallel Execution**: Group independent asynchronous operations to run concurrently using tools like `asyncio.gather` (Python) or `Promise.all` (JS/TS).
- **Prevent Deadlocks**: Minimize critical sections protected by mutexes or semaphores. Always define a **Timeout** on any lock acquisition.
- **State Immutability**: Limit mutable shared states in concurrent threads/tasks. Prefer immutable data structures or pass copies of data instead of mutating shared variables.

## 2. Resource & Database Query Optimization

- **No Heavy Operations inside Loops**: Move database calls, external API requests, or resource-heavy instantiations outside of loops. Fetch bulk data into a Map or Cache before iterating.
- **Prevent N+1 Queries**: Avoid executing child-record queries within a loop after fetching a list of parent records. Resolve this using:
  - **Eager Loading**: Query parent and children in a single request using SQL Joins (e.g. `joinedload` in SQLAlchemy).
  - **Batch Selection**: Collect child IDs and run a single `IN` query to load child records, then map them in memory.

  ```python
  # Bad (Causes N+1 query execution)
  users = db.query(User).all()
  for u in users:
      print(u.profile.nickname)

  # Good (Eager loads with JOIN FETCH)
  users = db.query(User).options(joinedload(User.profile)).all()
  ```
