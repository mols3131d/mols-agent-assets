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
- `strategy` — `native-first`, `source-first`, `index-first`, `scan`, or `<auto>`. `<auto>` chooses the cheapest authoritative discovery path for each source.
- `fallback` — `none`, `declared`, `external`, or `<auto>`. `<auto>` permits declared fallbacks but never broadens to unrelated public sources on its own.

`<auto>` means **infer from evidence**, not “use a hidden fixed value.” `<none>` explicitly disables the optional behavior for that argument. Explicit values always win.

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

## Auto Resolution

Resolve each `<auto>` independently. Do not treat one inferred value as permission to invent the others.

Use this evidence order unless an explicit argument overrides it:

1. explicit caller arguments;
2. caller-established source or selection context;
3. capabilities and Skill catalogs already exposed by the active runtime;
4. current task or repository guidance that declares a Skill source, index, or root;
5. source-local evidence such as repository instructions, manifests, indexes, and package structure;
6. this Skill's declarative `metadata.default-source`, only when no more relevant source is established.

The metadata default is a **fallback**, not a routing rule. It must not override an explicit source, hijack discovery for an unrelated repository, or cause unrelated public-source expansion.

If a required value remains materially ambiguous, preserve it as unresolved or ask only for the smallest decision needed. Do not manufacture a repository path, target capability, revision, or compatibility claim.

## Contract

This Skill is **read-only discovery and selection**. It owns:

- resolving candidate sources;
- choosing an efficient discovery path;
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
- `inventory` enumerates all unique in-scope capabilities.
- `sync-prep` returns a complete, reconciliation-ready selection set without mutating the target.

When target information is irrelevant to the request, leave it unspecified rather than fabricating a target taxonomy.

### Resolve sources

Normalize `sources` into ordered SourceSpecs.

When `sources: <auto>`:

1. use an explicitly established task/source context when present;
2. otherwise use a runtime-native Skill catalog when it already exposes the relevant capability space;
3. otherwise use repository-declared Skill discovery for the current task repository when relevant;
4. otherwise use `metadata.default-source` when present and allowed by `fallback`.

Do not fetch a remote repository merely to rediscover Skills already exposed authoritatively by the active runtime.

### Choose a discovery path

For each source, prefer the cheapest authoritative representation that can answer the request:

1. direct/native Skill catalog;
2. source-declared index or manifest;
3. scoped package discovery using source conventions;
4. targeted repository scan only when the source lacks a sufficient catalog/index;
5. external search only when explicitly permitted by `fallback` or caller intent.

An index is an optimization and authority hint, not a universal requirement. Do not assume a fixed filename or path unless the source declares it.

### Enumerate candidates

Inspect only enough candidate material to establish the fields relevant to the request:

- name and description;
- activation intent and responsibility;
- intended outcome and negative boundary;
- runtime-required files, tools, or resources;
- provenance and revision when available;
- observable compatibility with `target` and `constraints`.

For `match`, stop when the relevant candidate set is sufficiently covered. For `inventory` and `sync-prep`, cover the complete resolved scope.

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