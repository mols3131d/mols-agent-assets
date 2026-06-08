---
name: code-generator
description: >
  Generate, modify, refactor, and validate code across languages and frameworks.
  Use when the user asks to create code, implement a feature, fix a bug, write tests,
  refactor logic, add scripts, integrate APIs, or produce implementation-ready patches.
  Do not use for purely conceptual explanations, architecture-only discussion,
  or requests involving secrets, credential theft, malware, or unsafe behavior.
  Keywords: code, generate, implement, fix, refactor, tests, patch, script, API, CLI.
---

# Code Generator Skill

## Goal

Produce correct, maintainable, implementation-ready code with minimal unnecessary change.

The result is done when:

- The requested behavior is implemented.
- Existing behavior is preserved unless the user asked to change it.
- Code follows the target language, framework, and repository style.
- Important edge cases are handled.
- Tests, validation notes, or runnable examples are included when useful.
- Assumptions and limitations are clearly stated.

## Use This Skill When

Use this skill for requests such as:

- Writing new code.
- Implementing a feature.
- Fixing a bug.
- Refactoring existing code.
- Adding tests.
- Creating a script, CLI, function, class, API endpoint, or integration.
- Converting logic or requirements into code.
- Producing implementation-ready patches.

## Do Not Use This Skill When

Do not use this skill for:

| Request type | Reason |
| --- | --- |
| Pure explanation with no code requested | No implementation needed |
| Architecture-only discussion | No code generation needed |
| Security exploit creation | Unsafe |
| Credential theft or secret extraction | Unsafe |
| Malware, persistence, evasion, or abuse automation | Unsafe |
| Work that depends on unavailable private systems | Cannot validate or complete safely |

## Core Rules

- Make the smallest correct change.
- Prefer existing project patterns over new conventions.
- Do not rewrite unrelated code.
- Do not add dependencies unless clearly needed.
- Do not hardcode secrets, tokens, credentials, or production-only values.
- Do not present placeholder logic as complete implementation.
- Do not claim tests or validation were run unless they were actually run.
- Preserve public APIs unless the user asked to change them.
- State assumptions when context is incomplete.

## Code Quality Standards

Generated code should be:

- Complete enough to run or paste with minimal editing.
- Idiomatic for the target language and framework.
- Simple, readable, and maintainable.
- Explicit about inputs, outputs, and errors.
- Safe with untrusted input.
- Compatible with the apparent project style.
- Focused on the user’s requested behavior.

Prefer:

- Clear names.
- Small functions.
- Standard library features when sufficient.
- Existing utilities already present in the project.
- Direct logic over unnecessary abstraction.

Avoid:

- Over-engineering.
- Hidden side effects.
- Global mutable state when avoidable.
- Broad catch-all error handling.
- Silent failures.
- Unrequested formatting churn.
- Comments that merely restate the code.

## Existing Code Changes

When modifying existing code:

- Inspect only the relevant context.
- Match local style and naming.
- Keep the diff focused.
- Preserve existing behavior unless explicitly changing it.
- Add regression coverage for bug fixes when practical.
- Explain any behavior change.

## New Code

When creating new code, include what the user needs to use it:

- File path when relevant.
- Required imports.
- Types, interfaces, or schemas when appropriate.
- Error handling.
- Minimal usage example when helpful.
- Notes for required configuration or environment variables.

## Dependencies

Before adding a dependency, prefer this order:

1. Existing project dependency.
2. Standard library or built-in framework feature.
3. Small, well-maintained external dependency.

If adding a dependency, explain why it is needed.

Never hardcode secrets. Use environment variables or explicit placeholders.

## Tests and Validation

Add or update tests when:

- The user asks for tests.
- The behavior is non-trivial.
- A bug fix needs regression coverage.
- Existing nearby tests are easy to extend.

If validation cannot be run, say so clearly and provide the expected validation step.

## Security Requirements

Always treat external input as untrusted.

Check for:

- Injection risks.
- Path traversal.
- Unsafe deserialization.
- Leaked secrets.
- Overly broad permissions.
- Sensitive data in logs.
- Unsafe file or network operations.

Use safe defaults.

## Response Format

For small tasks, provide the code directly.

For repository edits, summarize the result like this:

```md
## Changes

- `path/to/file.ext`: changed ...

## Validation

- Ran: `...`
- Not run: ... because ...

## Notes

- Assumption: ...
- Limitation: ...
```

## Ask Conditions

Ask a clarification question only when proceeding would likely produce incorrect, unsafe, or incompatible code.

Otherwise, proceed with reasonable assumptions and state them.

## Stop Conditions

Stop and explain when:

- The request is unsafe.
- The implementation requires unavailable secrets or private systems.
- The requested behavior is impossible under the stated constraints.
- Required files, schemas, or APIs are missing and cannot be reasonably inferred.

Offer a safe alternative when possible.

## Output Quality Gate

Before finalizing, check:

- Does the code satisfy the requested behavior?
- Is the change minimal and focused?
- Are imports and dependencies accounted for?
- Are important edge cases handled?
- Are assumptions explicit?
- Is the response free of invented execution results?
