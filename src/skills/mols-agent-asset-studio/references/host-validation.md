# Host Validation

Built-in validators establish portable and runtime-specific structure. Project
validators establish repository conventions and integration health.

## Plan Format

Declare local checks in the selected project profile as argv arrays, never shell
strings:

```yaml
validation:
  local_commands:
    - id: skill-tests
      argv: [python, -m, pytest, -q, tests/skills]
      cwd: .
      timeout_sec: 120
      required: true
```

## Execution

```bash
python scripts/run_host_validation.py <repo> --allow-execution --output <report.json>
```

Without `--allow-execution`, the command emits a plan and exits `Deferred`.
The runner uses `shell=False`, rejects path escapes, and blocks obvious network or
package-install commands when project policy disallows them.

CI lanes remain declarative unless a separate trusted integration executes them.
Missing required CI evidence is `Deferred`, not Pass.
