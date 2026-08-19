---
name: mols-skill-find
description: Discover, match, and select Skills from runtime-native catalogs, repositories, indexes, directories, URLs, or explicit packages without installing them. Use when the caller needs one best Skill, a scoped inventory, or a sync-ready selection set and the source, target, discovery path, or constraints may be partially unspecified.
---

# Mols Skill Find

## Arguments

```yaml
sources: <auto>
query: <auto>
mode: <auto>
target: <auto>
constraints: <auto>
strategy: <auto>
fallback: <auto>
```

- `sources` — `<auto>`, one source, or an ordered list of sources. A source may be a runtime-native Skill catalog, repository, directory, index, URL, or concrete Skill package.
- `query` — capability need or selection intent. `<auto>` infers it from the caller. It may be omitted for inventory or sync preparation.
- `mode` — `match`, `inventory`, `sync-prep`, or `<auto>`. `<auto>` derives the smallest mode that satisfies the caller.
- `target` — intended Skill consumer or runtime. `<auto>` uses the active target when target fit materially affects selection. `<none>` disables target-specific filtering.
- `constraints` — optional `require`, `prefer`, and `exclude` conditions over capability, package requirements, tools, resources, provenance, or target support. `<auto>` infers only constraints established by the caller or environment.
- `strategy` — `first-match`, `merge`, `exhaustive`, or `<auto>`. It controls how ordered source results are combined, not how an individual source is scanned.
- `fallback` — `none`, `declared`, `external`, or `<auto>`. `<auto>` behaves as `declared`: declared fallbacks are allowed, unrelated public-source expansion is not.

`<auto>` means **infer from evidence**, not “use a hidden fixed value.” `<none>` explicitly disables the optional behavior for that argument. Explicit values always win.

## Defaults

```yaml
defaults:
  sources:
    - https://github.com/mols3131d/mols-agent-assets
```

Defaults are declarative last-resort values, not routing rules. They are considered only when `sources: <auto>` has no more relevant source and `fallback` allows declared fallbacks. An explicit `sources` value always overrides them, and `fallback: none` disables them.

Keep defaults in the Skill body because target projections may omit optional custom front-matter metadata. A default must remain visible and usable in the deployed Skill, not only in the canonical source.

For advanced calls, each item in `sources` may use a SourceSpec:

```yaml
sources:
  - source: <location-or-native-catalog>
    ref: <auto>
    scope: <auto>
    index: <auto>
```

- `source` identifies the source itself.
- `ref` pins a branch, tag, commit, version, or equivalent revision when the source supports one.
- `scope` limits discovery to a repository area, package set, or capability boundary.
- `index` may be an explicit index, `<auto>` to use a source-declared index when useful, or `<none>` to force direct discovery.

A scalar source is shorthand for `{source: <value>, ref: <auto>, scope: <auto>, index: <auto>}`.

Constraints may stay simple or be structured only when needed:

```yaml
constraints:
  require: []
  prefer: []
  exclude: []
```

## Auto Resolution

Resolve each `<auto>` independently. Do not treat one inferred value as permission to invent the others.

Use this evidence order unless an explicit argument overrides it:

1. explicit caller arguments;
1. caller-established source or selection context;
1. capabilities and Skill catalogs already exposed by the active runtime;
1. current task or repository guidance that declares a Skill source, index, or root;
1. source-local evidence such as repository instructions, manifests, indexes, and package structure;
1. declared `Defaults`, only when no more relevant source satisfies the request and `fallback` permits them.

Declared defaults must not override an explicit source, hijack discovery for an unrelated repository, or cause unrelated public-source expansion.

If a required value remains materially ambiguous, preserve it as unresolved or ask only for the smallest decision needed. Do not manufacture a repository path, target capability, revision, or compatibility claim.

## Contract

This Skill is **read-only discovery and selection**. It owns:

- resolving candidate sources;
- choosing an efficient discovery path within each source;
- matching capabilities to the caller's need;
- applying explicit constraints and observable target compatibility;
- grouping clear identity continuity;
- returning a selection that a delivery capability can consume.

It does not:

- install, update, rename, delete, or overwrite Skills;
- mutate source or target state;
- assume one repository layout, vendor, or runtime model is universal;
- broaden discovery to unrelated public sources unless `fallback: external` or equivalent caller intent explicitly allows it;
- downgrade an unsupported capability and report it as equivalent.

## Discovery

### Resolve intent

Resolve `mode`, `query`, `target`, and `constraints` before spending work on broad discovery.

- `match` finds the smallest relevant candidate set and selects the best supported candidate.
- `inventory` enumerates all unique capabilities in the resolved source scope.
- `sync-prep` returns a complete, reconciliation-ready selection set without mutating the target.

When target information is irrelevant to the request, leave it unspecified rather than fabricating a target taxonomy.

### Build the source plan

Normalize `sources` into ordered SourceSpecs.

When `sources: <auto>`, build a source plan from applicable evidence rather than choosing one source prematurely:

1. caller-established task/source context;
1. runtime-native Skill catalog when it exposes the relevant capability space;
1. current repository-declared Skill source when relevant;
1. declared `Defaults` only when `fallback` permits them.

Deduplicate equivalent sources while preserving the strongest provenance and most specific scope.

For `match`, `<auto>` strategy normally walks the plan as `first-match` and reaches declared fallbacks only when earlier sources do not produce a sufficient candidate.

For `inventory` and `sync-prep`, do not silently aggregate unrelated sources. With `sources: <auto>`, use the highest-priority authoritative source that defines the requested scope unless the caller explicitly supplies multiple sources or requests `strategy: merge` or `strategy: exhaustive`.

Do not fetch a remote repository merely to rediscover Skills already exposed authoritatively by the active runtime.

### Discover within a source

For each source, prefer the cheapest authoritative representation that can answer the request:

1. direct/native Skill catalog;
1. source-declared index or manifest;
1. scoped package discovery using source conventions;
1. targeted repository scan only when the source lacks a sufficient catalog or index;
1. external search only when explicitly permitted by `fallback` or caller intent.

`index` in SourceSpec controls index use for that source. An index is an optimization and authority hint, not a universal requirement. Do not assume a fixed filename or path unless the source declares it.

### Apply strategy

- `first-match` — walk ordered sources until the request has a sufficient supported result, then stop.
- `merge` — combine candidates from the resolved sources, deduplicate capability identity, and preserve source provenance.
- `exhaustive` — fully enumerate every resolved source before selection; use only when the caller needs complete cross-source coverage.
- `<auto>` — use `first-match` for ordinary matching and the narrowest single-source plan for inventory or sync preparation unless explicit intent requires broader coverage.

Do not use `strategy` to override `sources` order, SourceSpec scope, or `index` policy.

### Enumerate candidates

Inspect only enough candidate material to establish the fields relevant to the request:

- name and description;
- activation intent and responsibility;
- intended outcome and negative boundary;
- runtime-required files, tools, or resources;
- provenance and revision when available;
- observable compatibility with `target` and `constraints`.

For `match`, stop when the strategy is satisfied. For `inventory` and `sync-prep`, cover the complete resolved scope promised by the selected source plan.

### Resolve identity

Names are signals, not identity by themselves. Group candidates only when evidence shows continuity through provenance, source history, stable identity metadata, or materially matching activation, responsibility, outcome, and contract.

Do not invent target profiles or sibling classes. If a source genuinely exposes multiple implementations or projections of one capability, keep them as alternatives under the same capability identity and select only one when the caller requires one.

Use `confirmed`, `probable`, or `uncertain` identity confidence. Do not force uncertain identity for downstream destructive decisions.

### Select

Apply hard constraints before preferences.

Prefer the simplest candidate that fully preserves the requested capability and satisfies observable target requirements. More files, richer packaging, newer naming, or a vendor-specific surface are not quality signals by themselves.

If no candidate satisfies required constraints, return `unsupported` or `no-match`. Do not silently weaken the requirement.

## Handoff

Return records that `mols-skill-install` or another delivery capability can consume:

```yaml
capability: <name-or-identity>
selected: <candidate-path-id-or-url | null>
source: <resolved-source>
ref: <resolved-ref | null>
target: <resolved-target | null>
compatibility: supported | unsupported | unknown
identity: confirmed | probable | uncertain
alternatives: []
notes: <only material selection or compatibility notes>
```

For `inventory` and `sync-prep`, return one record per capability identity. Do not duplicate one capability merely because the source exposes multiple representations.

## Output

Answer the discovery intent first.

- `match` — return the selected candidate and only meaningful alternatives.
- `inventory` — return the complete in-scope capability inventory.
- `sync-prep` — return the complete selection set plus unresolved conflicts or unsupported items.
- Surface only material uncertainty, source limitations, or target incompatibility.
- Do not include installation instructions unless requested. Hand mutation ownership to `mols-skill-install` or the target-native equivalent.