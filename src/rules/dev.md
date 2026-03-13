# Development Guidelines

1. Test-Driven
   - Require Validation: All changes must be tested. Failing code is incomplete.
   - Reuse Tests: Append to existing test files (e.g., tests/) before creating new ones.

2. Style & Patterns
   - Match Environment: Adopt the patterns and styles of surrounding code.
   - Top-Level Imports: Place all imports at the file top. Avoid function-level imports.
   - Use Existing Utils: Do not reinvent the wheel. Check for built-ins or project utilities before writing extensive new code.

3. Safety & Clean
   - Specific Exceptions: Avoid broad try-except Exception. Define explicit errors.
   - Remove Dead Code: Immediately delete unused or commented-out code.

4. Documentation
   - Explain "Why": Document the reasoning and invariants, not "what" the code does.
   - Concise Errors: Write clear, terminal-friendly error messages.
