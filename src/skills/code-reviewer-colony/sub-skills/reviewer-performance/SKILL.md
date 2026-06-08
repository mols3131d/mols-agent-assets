---
name: reviewer-performance
description: Reviews performance-sensitive code, execution complexity, resource management, database queries, and async patterns.
---

# Performance Reviewer Skill

Procedural guidelines for identifying performance bottlenecks, resource leaks, and inefficiencies in code.

## Goal

Ensure the code executes efficiently, manages memory and resources correctly, and scales appropriately.

## Review Steps

1. **Check Algorithmic Complexity**:
   - Check for heavy nested loops or high time/space complexity (e.g., O(N^2) or worse on large datasets).
   - Ensure collections are sized or filtered correctly rather than processing unnecessary items.

2. **Audit Database & I/O Operations**:
   - Watch out for N+1 query problems (e.g., executing DB queries or external API calls inside a loop).
   - Verify that database queries are indexed and efficient (avoiding SELECT *).
   - Ensure caching is utilized where appropriate for heavy or frequently repeated operations.

3. **Check Resource Management**:
   - Verify that file descriptors, DB connections, and network sockets are closed properly (use context managers like `with` in Python, try-with-resources in Java/Go defer, etc.).
   - Check for potential memory leaks (e.g., global list additions without deletion, unremoved event listeners).

4. **Verify Concurrency & Async Usage**:
   - Check if asynchronous operations are used for I/O bound tasks.
   - Verify that concurrency controls (locks, mutexes, semaphores) are correctly managed to prevent deadlocks or race conditions.
   - Refer to guidelines in [principles.md](../../references/principles.md).
