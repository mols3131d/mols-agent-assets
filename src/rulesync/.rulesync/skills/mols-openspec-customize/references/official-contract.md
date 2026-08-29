---
description: >-
  Load when an OpenSpec customization decision depends on the exact vendor
  contract: supported profiles, project config, schema or CLI behavior, command or
  field semantics, paths, precedence, experimental status, version-specific
  behavior, or an authoritative OpenSpec source. Do not load merely because a task
  mentions OpenSpec or customization; reusable ownership decisions belong in
  customization-design.md and concrete repository decisions belong in
  project-customization.md.
---

# Official OpenSpec Contract

Use this reference for **exact OpenSpec contract questions that can change a
customization decision**. It answers what OpenSpec supports or does; it is not the
default reference for customization design.

## Which source answers the question?

There is no single source priority for every OpenSpec question. Match the source to
the claim you need to make.

| Question | Source to use |
| --- | --- |
| What does OpenSpec currently document and support? | Current `openspec.dev` documentation |
| What does this project actually run? | The OpenSpec version selected or installed by the project; observe its CLI when useful |
| Why does that project version behave this way? | Source corresponding to that version, only when docs and observed behavior are insufficient |
| What is changing in OpenSpec upstream development? | Upstream repository, only when the user or task explicitly requires latest upstream development or implementation research |

Do not browse or inspect upstream implementation merely because the task involves
OpenSpec customization. Use upstream source only when the decision genuinely depends
on latest development or unresolved implementation behavior.

Do not let upstream `main` silently override the behavior of an older project
version. If the relevant version cannot be inspected, keep that uncertainty visible.

## Official entrypoints

| Topic | Official source |
| --- | --- |
| Customization overview | <https://openspec.dev/docs/customize> |
| Configuration overview | <https://openspec.dev/docs/configuration> |
| Profiles and delivery | <https://openspec.dev/docs/profiles> |
| Project configuration | <https://openspec.dev/docs/project-config> |
| Custom schemas | <https://openspec.dev/docs/customize-schemas> |
| `config.yaml` reference | <https://openspec.dev/docs/configuration/config-yaml> |
| `schema.yaml` reference | <https://openspec.dev/docs/schemas/schema-yaml> |
| CLI reference | <https://openspec.dev/docs/cli> |
| Upstream repository | <https://github.com/Fission-AI/OpenSpec> |

## What each OpenSpec surface owns

Use the official sources above for exact details. At a high level:

- **Profiles** choose which OpenSpec workflows are installed and how supported
  workflow surfaces are delivered.
- **Project configuration** adds project context and scoped guidance and selects
  project-level behavior exposed by the current contract.
- **Schemas** own the planning artifact graph, referenced templates, and
  schema-level workflow instructions.

For reusable judgment about which owner to choose, use
[Customization design](customization-design.md).

## Schema package boundary

OpenSpec documents project schemas under `openspec/schemas/<name>/`, centered on
`schema.yaml` and the templates it references.

Project-owned companion material such as `README.md` or `docs/` is **not** an
OpenSpec schema input unless the relevant OpenSpec version explicitly documents it
as one. Colocating those files is a project maintenance convention, not an OpenSpec
extension contract.

When companion-file behavior or exact schema commands matter, verify them against
the target project's OpenSpec version. Schema-related commands may be experimental,
so avoid freezing their current syntax or behavior into reusable local guidance.

Current OpenSpec documentation treats a forked project schema as a snapshot that is
not updated by routine `openspec update`. For reusable guidance on maintaining that
owned snapshot or optional companion documentation, use
[Schema maintenance](schema-maintenance.md).
