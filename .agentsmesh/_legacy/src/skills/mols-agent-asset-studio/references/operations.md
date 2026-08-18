# Shared Operations

Use these mechanics only when the selected workflow needs deterministic support.
They are helpers, not additional workflow stages.

## Command Map

| Need | Command |
| --- | --- |
| Inventory repository assets | `python scripts/inventory_assets.py <repo> --format json --output <report>` |
| Validate an asset | `python scripts/validate_asset.py <target> --profile <profile> --strict` |
| Audit context size | `python scripts/audit_context.py <skill-root>` |
| Audit Skill structure | `python scripts/audit_skill_structure.py <skill-root> [--tests-root <tests>]` |
| Check declared invariants | `python scripts/check_invariants.py <target-root> <invariants.yaml>` |
| Scan imported source without executing it | `python scripts/scan_source_asset.py <source> --output <report.json>` |
| Scan likely secrets | `python scripts/scan_secrets.py <target> --json` |
| Package one Skill | `python scripts/package_skill.py <skill-root> --output <zip>` |

Do not scan the scripts directory to invent additional capabilities. Runtime
behavior evaluation is not a supported Studio operation.

## Validation Profiles

Use the narrowest profile that matches the actual runtime or specification:

- `agent-skill`
- `openai-skill`
- `openai-interface`
- `vscode-agent`
- `github-agent`
- `vscode-instruction`
- `agents-md`
- `copilot-instructions`
- `vscode-prompt`
- `vscode-hooks`
- `github-hooks`
- `github-mcp`

A Studio runtime profile validates only that named contract. It is not a substitute
for a project's own Skill convention or repository checks.

## Refactor Invariants

Use [behavior-invariants.yaml](../templates/behavior-invariants.yaml) only when a
refactor needs durable literal, path, heading, regex, or ordering checks. Do not
create an invariant artifact for ordinary edits that can be reviewed directly.

## Rules

- Scripts own deterministic mechanics, never semantic judgment or project policy.
- Use project-owned checks through the project's existing authoritative mechanism;
  do not invent a Studio configuration file solely to execute them.
- Execute commands only with explicit authority and a bounded working directory.
- Package only accepted source. Run applicable validation, structural hygiene, and
  secret scanning before distribution.
- Report unavailable or unexecuted checks as `Not run` or `Deferred`; never infer
  success.
