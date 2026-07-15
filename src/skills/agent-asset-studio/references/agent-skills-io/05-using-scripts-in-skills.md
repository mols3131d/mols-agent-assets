# 05. Using Scripts in Skills

## Core Concept

Use one-off commands for simple tools. Wrap complex/repetitive logic into tested `scripts/`. Ensure non-interactive execution, actionable errors, structured outputs, idempotency, and safe defaults.

## 1. One-off Commands

Run directly in `SKILL.md` if simple.

- Python: `uvx ruff@0.8.0 check .`
- Node: `npx eslint@9 --fix .`
- Go: `go run ...@vX.Y.Z .`
Rule: Pin versions. Note runtime requirements in frontmatter.

## 2. Referencing Scripts

Use paths relative to Skill root.
List scripts and usage steps in `SKILL.md`:

```markdown
1. Run `bash scripts/validate.sh input.json`
```

## 3. Self-contained Scripts

Bundle dependencies inside scripts to avoid separate install steps.

- Python: PEP 723 inline metadata (`uv run scripts/script.py`).
- Deno/Bun: URL imports with pinned versions.
- Ruby: `bundler/inline`.

## 4. Agent-Friendly Interfaces

- **No Interactive Prompts**: Blocked by harness. Use flags, stdin, env vars. Error on missing args instead of prompting.
- **Concise `--help`**: Show purpose, args, defaults, examples, exit codes.
- **Actionable Errors**: State what failed, valid options, and next command to run.
- **Structured Output**: stdout = JSON/CSV results. stderr = logs/warnings. No whitespace-aligned ascii tables for data.

## 5. Design Principles

- **Idempotent**: Safe to retry.
- **Strict Input**: Reject ambiguous inputs via enums/flags.
- **Dry-run**: Provide `--dry-run` for mutations.
- **Exit Codes**: Distinct codes for distinct errors (auth vs missing file).
- **Safe Defaults**: Require `--force` for destructive actions.
- **Bounds**: Limit output size; add pagination.

## Checklist

- [ ] Pinned dependencies.
- [ ] Relative paths only.
- [ ] Zero interactive prompts.
- [ ] Clear `--help` & actionable errors.
- [ ] stdout (data) vs stderr (logs) separated.
- [ ] Supports dry-run & idempotency.
- [ ] Output bounded/paginated.
