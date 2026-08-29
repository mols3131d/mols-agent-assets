---
description: >-
  Exact OpenSpec contract lookup for customization work. Load when commands,
  fields, paths, precedence, schema or CLI semantics, experimental status,
  version-specific behavior, or authoritative vendor sources can change the
  decision. Do not load merely because a task mentions OpenSpec; reusable design
  belongs in customization-design.md and project evidence belongs in
  project-customization.md.
---

# Official OpenSpec Contract

Use this reference only when **exact OpenSpec behavior can change the customization
decision**. It routes vendor-contract questions to the right source; it is not the
default customization guide.

## Choose the source by the claim

There is no single source priority for every question.

| Question | Source |
| --- | --- |
| What does OpenSpec currently document and support? | Current `openspec.dev` documentation |
| What does this project actually run? | The OpenSpec version selected or installed by the project; observe its CLI when useful |
| Why does that project version behave this way? | Source corresponding to that version, only when docs and observed behavior are insufficient |
| What is changing in upstream development? | Upstream repository, only when latest development or implementation research is explicitly needed |

Do not inspect upstream implementation merely because the task involves OpenSpec.
Upstream `main` must not silently override the behavior of the version a project
actually uses. If the relevant version cannot be inspected, keep that uncertainty
visible.

## Source map

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

For reusable judgment about which customization owner to choose, use
[Customization design](customization-design.md) instead of restating the vendor
contract here.

## Schema package boundary

OpenSpec documents project schemas under `openspec/schemas/<name>/`, centered on
`schema.yaml` and the templates it references.

Project-owned companion material such as `README.md` or `docs/` is not an OpenSpec
schema input unless the relevant OpenSpec version explicitly documents it as one.
Colocating those files is a project maintenance convention, not an OpenSpec extension
contract.

When companion-file behavior or schema commands matter, verify them against the
target project's OpenSpec version. Schema-related commands may be experimental, so
do not freeze current syntax or behavior into reusable local guidance.

Current OpenSpec documentation treats a forked project schema as a snapshot that is
not updated by routine `openspec update`. For guidance on maintaining that owned
schema and optional companion documentation, use
[Schema maintenance](schema-maintenance.md).
