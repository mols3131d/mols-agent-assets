# Extensibility

Projects extend Asset Studio through one authoritative project profile without
editing the core skill.

## Discovery Order

Select the first available source. Do not silently merge profiles.

1. caller-provided `--profile <path>`
1. `<repo>/.agent-assets/studio.yaml`
1. `<repo>/agent-assets.yaml`
1. built-in conservative defaults

Use `python scripts/project_profile.py <repo>` to report the selected source and
validate the profile. A malformed higher-precedence profile blocks fallback so a
broken policy is not silently ignored.

## Profile Contents

- canonical and runtime asset roots
- target runtimes and supported metadata
- naming and language policy
- specifications, architecture, decisions, and code sources of truth
- local validation commands and CI lanes
- network, package-installation, publication, attribution, and secret policy

Use [project-profile.yaml](../templates/project-profile.yaml) as the schema example.
Project policy may narrow Studio defaults but may not silently widen write
authority or disable security gates.

## Generated Adapters

Keep portable source separate from runtime-generated output. Record the generator
and regenerate host adapters instead of editing them manually.
