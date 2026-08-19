# Default Git Message Convention Reference

Fallback commit message convention used when no repository-specific convention is defined.

## Format Template

```text
<type>([optional scope]): <description>

[optional body]

[optional footer(s)]
```

## Allowed Types

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change without a feature or fix
- `perf`: Performance improvement
- `docs`: Documentation only
- `test`: Add or fix tests
- `style`: Code style only; no behavior change
- `chore`: Build, dependencies, tooling, or non-src/non-test changes

## Formatting Rules

- **Subject**: Imperative mood, lowercase after colon, no trailing period (target ≤50 chars, max 72).
- **Body**: Explain non-obvious *why*, not *what*; omit if obvious; wrap lines at 72 chars; use `-` bullets.
- **Footer**: Breaking changes (`BREAKING CHANGE: ...`) or issue references (`Closes #12`).
- **Prohibited**: AI attribution, personal pronouns ("I", "we"), or phrases like "This commit does".
