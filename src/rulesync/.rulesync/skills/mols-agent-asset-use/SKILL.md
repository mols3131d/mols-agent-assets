---
name: mols-agent-asset-use
description: >-
  Find, select, load, apply, install, register, update, sync, or migrate an Agent
  Asset into a target. Use when the caller needs an agent-facing capability found
  from catalogs, repositories, indexes, directories, URLs, or explicit assets, or
  when a known asset must be made usable. Covers Skills, Rules or instructions,
  prompts, agents or subagents, hooks, tool or MCP configuration, templates, and
  other agent-facing assets. Prefer direct or temporary use when persistence is not
  required; create durable target state only when the requested end state needs it.
  Do not use for authoring or materially changing asset behavior, or for formal
  validation and evaluation.
---

# Mols Agent Asset Use

Find the right Agent Asset and make it usable with the **least persistent state that
satisfies the request**.

# Contract

- Skip discovery when the asset is already unambiguous.
- Keep selection read-only until the requested end state requires target mutation.
- Prefer an asset already available in the active runtime or target over copying or
  reinstalling an equivalent asset.
- Prefer temporary load or direct use when the request only needs the asset for the
  current task or session.
- Persist only for explicit durable intent, an established durable target contract,
  or a requested synchronization state. Never install merely because installation is
  possible.
- Preserve target-native semantics. `install`, `register`, `import`, `apply`, `place`,
  and `configure` are possible target operations, not one universal Agent Asset model.
- Do not report a temporary load, staged import, generated file, or pending approval as
  a stronger persistent state than the target actually reached.
- Do not overwrite, rename, delete, merge, or discard customization when asset identity
  is uncertain.

# Arguments

```yaml
sources: <auto>
query: <auto>
asset_types: <auto>
target: <auto>
state: <auto>
constraints: <auto>
fallback: <auto>
on_conflict: <auto>
```

- `sources` — `<auto>`, one source, or an ordered list of runtime catalogs,
  repositories, directories, indexes, URLs, registries, or explicit assets.
- `query` — capability need or selection intent. `<auto>` infers it from the caller;
  it may be empty when the asset is already resolved.
- `asset_types` — `<auto>`, `all`, or one or more applicable Agent Asset types.
- `target` — intended consumer or runtime. `<auto>` uses the active target only when
  target fit or delivery materially affects the result. `<none>` disables target-specific
  filtering and delivery.
- `state` — `select`, `use`, `persist`, `sync`, or `<auto>`.
- `constraints` — optional required, preferred, or excluded capability, provenance,
  runtime, package, tool, or compatibility conditions.
- `fallback` — `none`, `declared`, `external`, or `<auto>`. `<auto>` behaves as
  `declared`; unrelated public discovery requires `external` or equivalent caller intent.
- `on_conflict` — `override`, `separate`, `skip`, or `<auto>`. `<auto>` never authorizes
  destructive conflict resolution.

`<auto>` means infer from current evidence, not use one hidden profile. Explicit values
win inside higher authority and safety constraints.

# Defaults

```yaml
defaults:
  sources:
    - https://github.com/mols3131d/mols-agent-assets
```

The declared default is a last-resort source, not a routing rule. It does not override an
explicit source, a more relevant runtime or repository source, or `fallback: none`.

# Resolve

Resolve only what can change the result:

1. requested capability or already-known asset;
1. required asset type, if any;
1. source scope and fallback boundary;
1. intended target, when target fit or delivery matters;
1. required state;
1. hard constraints and conflict policy.

Resolve `state: <auto>` by requested end state:

- inspection, comparison, inventory, or "find" intent → `select`;
- current-task/session use without durable intent → `use`;
- install, register, keep, reuse later, or equivalent durable intent → `persist`;
- reconcile an explicit source set with target state → `sync`.

Do not infer persistence from convenience. If the target can only satisfy a temporary-use
request through a durable mutation, expose that transition instead of silently escalating.

# Discover and Select

When discovery is needed, build the smallest source plan that can answer the request.
Prefer, in order:

1. an authoritative runtime-native or target-native catalog already exposing the relevant
   asset space;
1. the current repository or workspace source explicitly governing the task;
1. a source-declared index, manifest, registry, or routing surface;
1. scoped direct discovery inside the resolved source;
1. declared fallback sources;
1. external search only when explicitly permitted.

Do not assume one filename, package layout, registry, or discovery mechanism is universal.
An index is an optimization and authority hint, not a requirement.

Inspect only enough candidate material to establish what matters for selection:

- responsibility and activation or application scope;
- intended outcome and important negative boundaries;
- provenance and revision when available;
- runtime-required files, tools, dependencies, or target capabilities;
- observable compatibility with the target and explicit constraints.

Names are signals, not identity. Group or replace assets only with evidence of continuity
through provenance, history, stable identity metadata, or materially matching responsibility
and contract. Preserve uncertainty instead of forcing a match.

For inventory requests, stay inside the resolved source scope unless the caller explicitly
requests cross-source aggregation.

# Use and Deliver

After selection, stop at the least persistent state that satisfies the request.

## `select`

Return the selected asset or bounded candidate set. Do not mutate the target.

## `use`

Prefer, in order:

1. direct invocation or use when the asset is already available;
1. temporary context or session load;
1. another target-native non-durable mechanism that satisfies the request.

Do not create persistent state merely to make future use easier. If runtime support is
insufficient, return the smallest remaining target-native action rather than pretending the
asset was used.

## `persist`

Use the target's native durable mechanism, such as install, register, import, apply, place,
or configure. Preserve the requested persistent semantics instead of substituting a
session-only load.

Before mutation, inspect existing target state when supported. If the same identity is
already current, make no mutation. If the same identity is stale and update is supported,
update rather than duplicate.

## `sync`

Require an explicit or otherwise bounded source set. Reconcile each selected capability
against observable target state and apply only the selected source identity.

Do not delete target-only assets automatically. Report them as orphan or extra candidates
when that concept is observable. Process an asset controlling the current run after other
selected assets, and use its new version only on the next invocation.

# Asset Handling

Preserve source and target semantics instead of forcing every Agent Asset into a Skill-like
package.

- Skill or packaged capability — preserve runtime-required package resources; exclude
  maintainer-only material when the source distinguishes it.
- Rule or instruction — preserve selector, scope, precedence, inheritance, and target
  attachment semantics.
- Prompt, agent, subagent, hook, tool, MCP, template, or config — preserve the owning
  runtime's accepted representation and required relationships.
- Single-file assets remain single-file when the target accepts them.
- Do not invent wrappers, archives, manifests, or conversion layers unless the chosen
  target path actually requires them.

If a required dependency or semantic contract cannot be represented by the target, return
`unsupported` rather than applying a silently degraded asset.

# Conflict Safety

Without sufficient identity evidence, do not overwrite, rename, delete, merge, or replace
an existing asset.

- `override` requires explicit caller choice.
- `separate` keeps both under distinct target identities when supported.
- `skip` leaves the existing target state unchanged.
- `<auto>` reports the conflict and valid choices.

Preserve target-managed settings and user customization unless the requested transition
explicitly supersedes them and authority permits it.

# Output

Report the actual result, not the attempted operation:

- `Selected`
- `Used / Loaded` — include temporary scope when material
- `Persisted / Installed / Registered / Applied`
- `Updated`
- `Synced`
- `Already Available`
- `Already Current`
- `Pending User Action`
- `Conflict`
- `Unsupported`
- `No Match`

Include only material provenance, compatibility, conflict, or remaining-action detail.

# Boundary

- Authoring, refactoring, or materially changing Agent Asset behavior belongs to
  `mols-agent-asset` when that Skill's maintained types apply.
- Formal validation, readiness, adversarial evaluation, regression validation, and
  validation-driven bounded correction belong to `mols-agent-asset-validator`.
- Discovery does not grant mutation authority, and loading does not imply permission to
  persist.
