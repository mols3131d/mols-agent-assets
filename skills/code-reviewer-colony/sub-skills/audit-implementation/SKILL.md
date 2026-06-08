---
name: audit-implementation
description: Reviews core code logic, readability, style, correctness, error handling, and formatting.
---

# Implementation Reviewer Skill

Procedural guidelines for reviewing code implementation details, logic flow, and clean code qualities.

## Goal

Ensure the implemented code is correct, maintainable, readable, and conforms to target guidelines.

## Review Steps

1. **Check Correctness & Logic**:
   - Verify if the code satisfies the functional requirements.
   - Look for edge cases (e.g., empty arrays, null values, out-of-range inputs, division by zero) and verify they are handled properly.
   - Check if public APIs are preserved unless specifically requested to change.

2. **Evaluate Readability & Style**:
   - Verify if variables and functions are named clearly and express intent.
   - Ensure the code follows consistent style patterns.
   - Flag unnecessary code changes or formatting churn in unrelated files.
   - Ensure functions and files are focused (SRP). Prefer short functions.
   - Check guidelines in [principles.md](../../references/principles.md).

3. **Assess Error Handling**:
   - Ensure errors are not silently swallowed.
   - Check that error handling uses appropriate language conventions (e.g., try-catch blocks, Go style err returns, Result types).
   - Verify that logs do not contain secrets or sensitive user information (PII).
