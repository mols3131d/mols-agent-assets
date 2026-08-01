# Operations

| Need | Command or template |
| --- | --- |
| Resolve project policy | `python scripts/profile_project.py <repo> --output <profile.json>` |
| Quarantine imported source | `python scripts/scan_source_asset.py <source> --output <scan.json>` |
| Validate provenance | `python scripts/validate_tuning_record.py <provenance.yaml>` |
| Capture source behavior | [source-contract.md](../templates/source-contract.md) |
| Map changes | [adaptation-matrix.md](../templates/adaptation-matrix.md) |
| Record provenance | [provenance.yaml](../templates/provenance.yaml) |
| Report tuning | [tuning-report.md](../templates/tuning-report.md) |
| Start a project profile | [project-profile.yaml](../templates/project-profile.yaml) |

Project profile precedence is explicit path, `.agent-assets/studio.yaml`,
`agent-assets.yaml`, then conservative defaults. Profiles are not silently merged.

Project-owned validation uses the Studio `run_host_validation.py` argv contract.
Imported scripts are never added to that plan until provenance, source review, and
explicit execution authority are complete.
