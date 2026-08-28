# Official OpenSpec Customization

Use this reference as a discovery map for OpenSpec's current customization
contract. The linked official sources remain authoritative.

## Authority

Prefer sources in this order when exact behavior matters:

1. current documentation on `openspec.dev`;
1. the upstream `Fission-AI/OpenSpec` repository when implementation or examples
   clarify a documented contract;
1. the installed OpenSpec CLI for version-specific observed behavior in the target
   environment.

Do not treat this file as a frozen copy of OpenSpec's schema or CLI contract.
Re-check the official source when fields, commands, paths, precedence, experimental
status, or generated surfaces can affect the result.

## Official entrypoints

| Topic | Official source |
| --- | --- |
| Customization overview | <https://openspec.dev/docs/customize> |
| Profiles and delivery | <https://openspec.dev/docs/profiles> |
| Project configuration guide | <https://openspec.dev/docs/project-config> |
| Custom schemas guide | <https://openspec.dev/docs/customize-schemas> |
| `config.yaml` reference | <https://openspec.dev/docs/configuration/config-yaml> |
| `schema.yaml` reference | <https://openspec.dev/docs/schemas/schema-yaml> |
| CLI reference | <https://openspec.dev/docs/cli> |
| Upstream repository | <https://github.com/Fission-AI/OpenSpec> |
| Schema command implementation | <https://github.com/Fission-AI/OpenSpec/blob/main/src/commands/schema.ts> |
| Schema resolver implementation | <https://github.com/Fission-AI/OpenSpec/blob/main/src/core/artifact-graph/resolver.ts> |

## Responsibility map

Use the official documentation to resolve details, but keep the main ownership
boundary clear:

- **Profiles** choose which OpenSpec workflows are installed and how the supported
  workflow surfaces are delivered.
- **Project configuration** adds project context and scoped guidance to workflow
  runs and selects project-level OpenSpec behavior exposed by its current contract.
- **Schemas** own the planning artifact graph, templates, and schema-level workflow
  instructions.

## Schema package boundary

Official documentation describes a schema's semantic surface as a directory with
`schema.yaml` and the templates referenced by it. Project schemas live under
`openspec/schemas/<name>/` and are normally versioned with the project.

Do not present `README.md`, `docs/`, examples, tuning notes, or other companion
files as official schema inputs unless OpenSpec documents them as such.

At the time this reference was authored, upstream implementation:

- resolves a schema from a directory containing `schema.yaml`;
- validates `schema.yaml` and its referenced template files rather than rejecting
  unrelated regular files in the schema directory;
- recursively copies the schema directory when forking.

This makes colocated maintainer documentation a usable project convention today,
but not an OpenSpec schema contract. Schema commands are currently marked
experimental, so re-check current documentation or implementation before relying on
companion-file behavior.

A forked schema is also a snapshot: normal OpenSpec update flows do not merge later
built-in schema improvements into the project copy. Treat upstream comparison and
porting as explicit maintenance decisions.
