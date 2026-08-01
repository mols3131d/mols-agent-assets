# Portability

Use the open Agent Skills core (`SKILL.md`, optional scripts, references, and
assets) as the portable layer. Add host adapters only when the target runtime is
known.

## Common Project Layouts

| Runtime | Typical project skill location |
| --- | --- |
| GitHub Copilot | `.github/skills/<name>/`, `.agents/skills/<name>/`, or another supported compatible location |
| OpenAI Codex | repository or user skill location supported by the installed Codex version |
| Claude Code | `.claude/skills/<name>/` or compatible Agent Skills location |
| Shared source repository | canonical `src/skills/<name>/` plus installation or linking step |

Verify current host documentation before asserting an exact discovery path.

## Metadata

- `name` and `description` are the portable activation core.
- Put optional host-specific fields only in assets targeting a runtime that
  documents them.
- Keep UI metadata such as OpenAI `agents/openai.yaml` as an adapter, not part of
  the portable behavioral contract.
- Do not claim one host's `tools`, invocation, or subagent fields work everywhere.

## Context Isolation

- Use native subagents for independent review or bounded work when supported.
- Use a fresh or forked context when available.
- Fall back to sequential roles with durable inputs and outputs.
- Keep statuses, findings, and acceptance evidence identical across modes.
