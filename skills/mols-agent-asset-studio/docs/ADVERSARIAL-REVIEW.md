# Adversarial Review

## Verdict

`Pass` after correction for tested deterministic attack paths. Runtime-dependent
misuse remains part of the deferred dogfooding gate.

## Attack Closure

| Attack | Mitigation | Regression evidence |
| --- | --- | --- |
| YAML/frontmatter injection through descriptions | JSON-quoted YAML scalars | `test_scaffold_quotes_hostile_description` |
| Symlink exfiltration outside skill root | validator and packagers reject symlinks | `test_package_rejects_symlink_and_inner_output` |
| Archive generated inside a source tree | skill and bundle packagers reject source-boundary outputs | `test_bundle_rejects_output_inside_source_boundary` |
| Secret stored in an innocent filename | redacted likely-secret content scanner blocks package | `test_package_blocks_secret_content_in_innocent_filename` |
| Secret-like filenames | `.env*`, credentials, keys, and related files excluded and recorded | `test_package_excludes_secret_named_files_and_writes_manifest` |
| Invalid agent capability fields | runtime-specific type and host-boundary validation | `test_invalid_agent_types_fail`; `test_cloud_agent_rejects_vscode_only_fields` |
| Invalid MCP configuration | top-level and per-server schema checks | `test_invalid_mcp_top_level_and_server_types_fail` |
| Imported code execution | Tuner scanner hashes and inspects without execution | `test_source_scanner_never_executes_and_hides_absolute_path` |
| Local-path disclosure | project and source profiles hide absolute paths by default | Tuner profile and source-scanner tests |
| Prompt-injection content in imported source | static quarantine signals and untrusted-data rule | Tuner scanner test and `source-trust.md` |
| Silent profile fallback | malformed highest-precedence profile blocks lower fallback | `test_malformed_high_precedence_profile_blocks_fallback` |
| False Pass without runtime evidence | incomplete observations grade as `Deferred` | `test_runtime_eval_is_deferred_until_observed_and_compares_baseline` |

## Residual Risk

- Secret scanning is a redacted likely-plaintext-secret detector, not a substitute
  for an organization-approved scanner such as its CI secret-detection lane.
- Static imported-source signals require human or reviewer interpretation.
- Runtime metadata and behavior can change; validate against the target host
  version before publication.
- Trigger quality and action behavior are not proven until the supplied cases run
  in the named runtime.
