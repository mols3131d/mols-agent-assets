---
name: reviewer-security
description: Reviews security vulnerabilities, input validation, authentication/authorization checks, and prevents hardcoded secrets.
---

# Security Reviewer Skill

Procedural guidelines for scanning and preventing security vulnerabilities in code changes.

## Goal

Ensure the code is secure against common vulnerabilities (OWASP Top 10) and does not leak sensitive data.

## Review Steps

1. **Check for Code Injections**:
   - Verify that all database queries use parameterized queries / ORM prepared statements instead of raw string interpolation to prevent **SQL Injection**.
   - Check if inputs rendered in UI or templates are properly escaped to prevent **XSS (Cross-Site Scripting)**.
   - Inspect command executions (e.g., `os.system`, `subprocess`, `exec`, `eval`) to ensure they do not run raw untrusted input.

2. **Audit Secrets & Sensitive Data**:
   - Scan the changes for hardcoded credentials, API keys, passwords, private tokens, or certificate files. Ensure they are placed in environment variables or configuration files.
   - Verify that sensitive information (PII or secrets) is not printed to stdout or written to logs.

3. **Check Input Validation & Path Safety**:
   - Ensure external input is validated against a whitelist/schema.
   - Guard against **Path Traversal** (e.g., verify that file paths constructed from inputs are sanitized and restricted to a specific base directory).
   - Check against SSRF (Server-Side Request Forgery) by validating URLs before calling them.

4. **Verify Authentication & Access Control**:
   - Check that any new endpoints or APIs require appropriate authentication and authorization checks.
   - Ensure access checks are performed on the server-side, not just in UI.
   - Refer to guidelines in [principles.md](../../references/principles.md).
