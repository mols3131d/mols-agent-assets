# OpenSpec Customization Patterns

Use these as reusable design heuristics, not OpenSpec requirements. Confirm exact
fields, commands, paths, and supported behavior through [Official](official.md).

## Config before schema

Prefer project configuration when the existing workflow structure can stay intact
and the change only adds context, artifact guidance, operation guidance, or another
project-level option supported by OpenSpec.

Use a custom schema when the planning artifact set, dependency flow, templates, or
schema-level workflow instructions must materially differ.

A schema fork creates another schema snapshot to own, so do not use it for a change
that additive configuration can express.

## Narrowest surface

Put a customization on the smallest supported surface that needs it.

| Needed effect | First surface to consider |
| --- | --- |
| Choose installed workflows or delivery form | Profile |
| Add broadly applicable project planning context | Project configuration |
| Add guidance for one planning artifact | Artifact-scoped project rule |
| Add apply or archive guidance | Operation guidance |
| Select a project schema | Project configuration |
| Change artifacts, dependencies, templates, or schema instructions | Custom schema |
| Preserve repository policy OpenSpec does not need to inject | Existing repository owner |

The table is a selection heuristic, not a replacement for OpenSpec's current
contract.

## Delta-only context

Do not turn OpenSpec configuration into a second project handbook.

Keep only context that should materially shape OpenSpec workflow output. Put narrow
rules on narrow surfaces. When the active agent can reliably load existing
repository guidance, prefer that canonical owner and inject only the delta OpenSpec
actually needs.

## Preserve project authority

OpenSpec customization should adapt to repository policy, not become a competing
owner of testing, architecture, security, documentation, language, contribution,
or other project rules.

If the same rule appears in project instructions, OpenSpec configuration, and a
schema template, identify the actual owner and remove accidental copies unless
OpenSpec needs a deliberate operational copy.

## Treat schema forks as owned snapshots

A project-local custom schema is an intentionally owned copy. Do not assume normal
OpenSpec updates will merge future built-in schema improvements into it.

Keep shared project schemas versioned with the project, and port upstream changes
only when they remain useful for that project.

## Verify resolved behavior

Static YAML review proves less than resolved workflow behavior.

When the claim concerns what an agent receives or which schema or template resolves,
use the current OpenSpec inspection or validation command that observes that surface.
Verify the smallest output that can prove the customization worked.
