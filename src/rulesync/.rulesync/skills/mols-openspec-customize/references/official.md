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

## Responsibility map

Use the official documentation to resolve details, but keep the main ownership
boundary clear:

- **Profiles** choose which OpenSpec workflows are installed and how the supported
  workflow surfaces are delivered.
- **Project configuration** adds project context and scoped guidance to workflow
  runs and selects project-level OpenSpec behavior exposed by its current contract.
- **Schemas** own the planning artifact graph, templates, and schema-level workflow
  instructions.
