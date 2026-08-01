# Operations

Use these scripts from the skill root. Run only the operation selected by the
workflow; do not scan the directory to discover capabilities.

## Command Map

| Operation | Command | Output |
| --- | --- | --- |
| Inventory repository assets | `python scripts/inventory_assets.py <repo> --format json --output <report>` | Asset paths and inferred types |
| Detect likely skill overlap | `python scripts/detect_skill_overlap.py <skills-root>` | Warning-only candidate pairs |
| Analyze consolidation | `python scripts/analyze_consolidation.py <skills-root> --format json` | Candidate pairs and required authority evidence |
| Scaffold a portable skill | `python scripts/scaffold_asset.py skill <name> --path <root> --description "..."` | Minimal skill directory |
| Scaffold a VS Code agent | `python scripts/scaffold_asset.py vscode-agent <name> --path <root> --description "..."` | `.agent.md` file |
| Validate an asset | `python scripts/validate_asset.py <target> --profile <profile> --strict` | Runtime-specific verdict |
| Audit context size | `python scripts/audit_context.py <skill-root>` | Entry and reference size report |
| Audit package structure | `python scripts/audit_skill_structure.py <skill-root> [--tests-root <tests>]` | Nested skill, empty, orphan, and test-evidence findings |
| Check behavior invariants | `python scripts/check_invariants.py <target-root> <invariants.yaml>` | Literal, heading, path, regex, and order verdict |
| Scan for secrets | `python scripts/scan_secrets.py <target> --json` | Redacted content findings |
| Package one skill | `python scripts/package_skill.py <skill-root> --output <zip>` | Strict skill ZIP and manifest |
| Package mixed assets | `python scripts/package_asset_bundle.py <asset-bundle.yaml> --output <zip>` | Multi-asset ZIP and install map |
| Discover project profile | `python scripts/project_profile.py <repo>` | Selected profile and validated data |
| Run project checks | `python scripts/run_host_validation.py <repo> --allow-execution --output <report.json>` | argv-only local validation evidence |
| Validate trigger cases | `python scripts/validate_eval_set.py <cases.json>` | Case balance and schema verdict |
| Create runtime result sheet | `python scripts/init_runtime_eval.py <cases.json> --runtime <name> --configuration candidate --output <results.json>` | Fillable runtime results |
| Grade runtime results | `python scripts/grade_runtime_eval.py <cases.json> <candidate.json> [--baseline <legacy.json>]` | Precision, recall, F1, deltas |

## Profiles

Use explicit profiles when runtime authority matters:

- `agent-skill`: Agent Skills open specification
- `openai-skill`: OpenAI Codex-compatible `SKILL.md` frontmatter
- `openai-interface`: `agents/openai.yaml`
- `vscode-agent`: VS Code custom agent
- `github-agent`: GitHub Copilot cloud custom agent
- `vscode-instruction`: `*.instructions.md`
- `agents-md`: `AGENTS.md`
- `copilot-instructions`: `.github/copilot-instructions.md`
- `vscode-prompt`: `*.prompt.md`
- `vscode-hooks`: VS Code hook JSON
- `github-hooks`: Copilot CLI/cloud hook JSON
- `github-mcp`: GitHub repository MCP JSON
- `project-profile`: Studio project profile
- `asset-bundle`: mixed asset bundle descriptor

## Template Map

| Need | Template |
| --- | --- |
| Scope a new or changed asset | [asset-brief.md](../templates/asset-brief.md) |
| Plan asset consolidation | [consolidation-plan.md](../templates/consolidation-plan.md) |
| Protect refactor behavior | [behavior-invariants.yaml](../templates/behavior-invariants.yaml) |
| Record recovery readiness | [rollback-plan.yaml](../templates/rollback-plan.yaml) |
| Define host checks | [validation-plan.yaml](../templates/validation-plan.yaml) |
| Author a route case | [route-eval-case.yaml](../templates/route-eval-case.yaml) |
| Define project extension policy | [project-profile.yaml](../templates/project-profile.yaml) |
| Define a mixed package | [asset-bundle.yaml](../templates/asset-bundle.yaml) |
| Author a trigger or behavior case | [eval-case.yaml](../templates/eval-case.yaml) |
| Record runtime execution | [runtime-eval-result.json](../templates/runtime-eval-result.json) |
| Record imported-source provenance | [provenance.yaml](../templates/provenance.yaml) |
| Write general or adversarial findings | [review-report.md](../templates/review-report.md) |

## Rules

- Package commands always run strict validation and write reproducible ZIP metadata.
- Release closure runs structural audit; nested skills, empty directories, and
  zero-byte resources are errors.
- Secret findings block packaging unless the caller explicitly accepts the exact
  findings with `--allow-secret-finding`.
- `detect_skill_overlap.py` is a triage aid, never a semantic verdict.
- Runtime evaluation remains `Deferred` until every case has an observed result.
