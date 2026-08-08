# Independent Review Closure

## Verdict

All independent findings F-001 through F-008 are closed for deterministic
implementation. Live target-runtime behavior remains `Deferred`.

## Finding Matrix

| ID | Original finding | Correction | Evidence |
| --- | --- | --- | --- |
| F-001 | Scripts and templates were orphaned | Added Studio operation table, direct command map, profile list, and template map | `src/skills/mols-agent-asset-studio/SKILL.md:36`; `references/operations.md`; `artifacts/review-probes/f001-operation-map.txt` |
| F-002 | Validator accepted invalid agent and MCP structures | Added profile-specific validators for skills, OpenAI UI, VS Code/GitHub agents, instructions, prompts, hooks, MCP, profiles, and bundles | `validators/github_agent.py:45`; `validators/github_mcp.py:64`; probes `f002-invalid-agent.txt`, `f002-invalid-mcp.txt`; negative tests |
| F-003 | Skill packaging bypassed strict validation | Packaging invokes `validate_target(..., strict=True)` and has no non-strict default | `scripts/package_skill.py:54`; `f003-strict-package.txt`; `test_package_is_strict_and_rejects_unknown_skill_field` |
| F-004 | Secret protection relied on filenames | Added redacted likely plaintext-secret patterns, filename exclusion, manifest reporting, and blocking behavior | `scripts/scan_secrets.py:85`; `f004-secret-block.txt`; secret packaging tests |
| F-005 | Eval sets were below the stated standard and not executable | Expanded to 24 and 22 balanced cases; added observation initializer and baseline grader; incomplete observations return Deferred | `validate_eval_set.py:11`; `grade_runtime_eval.py:62`; F-005 probes; runtime-eval test |
| F-006 | Project extension discovery was undefined | Defined explicit profile, `.agent-assets/studio.yaml`, `agent-assets.yaml`, defaults; single highest-precedence profile and no hidden merge | `project_profile.py:12,29-48,67`; `f006-profile-discovery.json`; profile tests |
| F-007 | Package mode supported only one skill | Added mixed asset descriptor and packager with per-asset profiles, install map, collision and source-boundary checks | `package_asset_bundle.py:43`; `asset-bundle.yaml`; `f007-bundle-manifest.txt`; mixed-bundle tests |
| F-008 | Review evidence was narrative-only | Added exact failure probes, command output, test names, finding-level evidence, final validation JSON, and this closure report | `artifacts/review-probes/`; `artifacts/validation-results.json`; `docs/asset-studio/FINAL-VALIDATION.md` |

## Required Negative Probes

| Probe | Expected result |
| --- | --- |
| invalid `tools` and `handoffs` agent | exit `1` with type errors |
| top-level-array MCP config | exit `1` |
| unknown Agent Skill field during package | exit `1`; no archive |
| likely secret in innocent `.txt` filename | exit `1`; redacted value |
| incomplete runtime result sheet | exit `2`; `Deferred` |

## Closure Boundary

This closure proves deterministic implementation and evidence handling in the
packaged Python environment. It does not prove semantic trigger or behavior
quality in a named agent runtime; that separate gate remains `Deferred` and is
specified in `RUNTIME-EVALUATION.md`.
