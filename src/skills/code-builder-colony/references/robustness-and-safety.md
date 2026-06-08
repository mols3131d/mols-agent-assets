---
name: robustness-and-safety
description: >
  Read when writing production-grade code, handling untrusted external inputs (APIs, CLI), implementing error boundaries, or protecting secrets.
  Do not read for internal helper utilities, test suites, or scratch files with trusted inputs.
---

# Robustness & Safety Guide

Guidelines to ensure code stability, validation accuracy, error resilience, and security.

## Applicability

- **Apply When**: Writing production-grade code, exposing public APIs, processing untrusted external inputs, or handling critical business logic where security, data integrity, and failure recovery are essential.
- **Do Not Apply To**: Internal helper utilities with trusted inputs, local test suites, or scratch files where lightweight inline checks or simple assertion statements are preferred over heavy validation schemas and custom exceptions.

## 1. Standard Error Handling

- **Categorize Exceptions**: Distinguish clearly between *Business Exceptions* (expected client-side or rule validation failures) and *System Exceptions* (unexpected internal errors, network drops).
- **No Silent Catching**: Do not swallow exceptions. At a minimum, log the exception, and re-throw or map it to a structured response.
- **Custom Exceptions**: Inherit from the language's base Exception/Error class to create descriptive domain-specific exceptions.

  ```python
  class ApplicationError(Exception):
      def __init__(self, code: str, message: str, status_code: int = 400):
          super().__init__(message)
          self.code = code
          self.status_code = status_code
  ```

- **Consistent API Response Format**: All error responses must adhere to a standard template:

  ```json
  {
    "status": "error",
    "code": "USER_NOT_FOUND",
    "message": "The specified user does not exist.",
    "details": []
  }
  ```

## 2. Boundary Validation (Data Verification)

- **Verify at Boundaries**: Validate all external inputs (HTTP payloads, query parameters, CLI flags, event payloads) immediately at the entry point layer (Controller/Handler) before passing them to core logic.
- **Declarative Schemas**: Use library-based schemas (e.g. Zod, Pydantic) for validation.

  ```typescript
  const createUserSchema = z.object({ email: z.string().email() });
  const payload = createUserSchema.parse(req.body); // Done in handler
  ```

## 3. Defensive Programming

- **Null/Undefined Guards**: Use optional chaining (`?.`) and null-coalescing (`??`) operators to prevent reference errors.
- **Guard Clauses (Early Return)**: Avoid deep nested conditional branches. Handle error/invalid conditions first, returning or throwing early.

  ```python
  def process_order(order):
      if not order:
          return
      if not order.is_paid:
          raise ApplicationError("NOT_PAID", "Order has not been paid.")
      # Core logic proceeds here flat
  ```

## 4. Secure Coding Principles

- **Prevent Injection Attacks**: Never concatenate or interpolate user input directly into database queries, shell commands, or HTML outputs. Always use **Parameterized Bindings** or ORM query builders.

  ```python
  # Bad: db.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
  # Good: db.execute("SELECT * FROM users WHERE id = :id", {"id": user_id})
  ```

- **No Hardcoded Secrets**: Never store credentials, API keys, tokens, or private configurations in the source code. Retrieve them from Environment Variables (`.env`) or a dedicated Secret Manager.
- **Mask Sensitive Data**: Mask Personal Identifiable Information (PII), credentials, passwords, and tokens before logging. Ensure debug logs do not leak secrets in CI/CD or log monitors.
