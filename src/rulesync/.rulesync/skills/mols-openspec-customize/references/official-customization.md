# Official OpenSpec Customization

Use this reference as a discovery map for OpenSpec's current customization
contract. The linked official sources remain authoritative.

## Authority by question

Do not use one global source priority for every OpenSpec question. Match the source
to the decision being made:

- **Current documented contract** — use the current documentation on
  `openspec.dev`.
- **Behavior in a concrete project** — use the OpenSpec version actually installed
  or selected by that project, including observed CLI behavior when relevant.
- **Implementation detail for that version** — inspect source corresponding to the
  project's version only when documentation and observed behavior are insufficient.
- **Latest upstream development** — inspect the upstream repository when the task is
  explicitly about current development rather than the target project's runtime.

Do not let upstream `main` silently override the behavior of an older project
version. If the relevant version or runtime cannot be inspected, preserve that
uncertainty instead of inventing precedence.

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

Use the official documentation to resolve exact details while keeping the main
ownership boundary clear:

- **Profiles** choose which OpenSpec workflows are installed and how supported
  workflow surfaces are delivered.
- **Project configuration** adds project context and scoped guidance to workflow
  runs and selects project-level behavior exposed by its current contract.
- **Schemas** own the planning artifact graph, templates, and schema-level workflow
  instructions.

## Schema package boundary

Official documentation describes a project schema around `schema.yaml` and the
templates it references under `openspec/schemas/<name>/`.

Do not present project-owned companion material such as `README.md` or `docs/` as
OpenSpec schema inputs unless the relevant OpenSpec version documents them as such.
Their colocating is a project maintenance convention, not an OpenSpec extension
contract.

When companion-file compatibility matters, verify it against the target project's
OpenSpec version rather than relying on assumptions about upstream implementation.
Schema-related commands may also carry experimental status, so re-check the current
contract before depending on exact command behavior.

A forked project schema is an owned snapshot rather than a live extension of the
built-in schema. Do not assume normal OpenSpec updates will merge later built-in
changes into that project copy; treat upstream comparison and porting as deliberate
maintenance work.
