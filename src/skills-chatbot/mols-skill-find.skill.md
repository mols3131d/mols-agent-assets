---
name: mols-skill-find
description: >-
  Find and select installable Skills from a repository or explicit skill source without
  installing them. Use to discover available capabilities, match a requested capability,
  inventory Skills for synchronization, or choose one target-specific sibling before
  installation. Do not mutate the source or install Skills.
metadata:
  references:
    - vercel-labs/skills:skills/find-skills/SKILL.md
---

# Mols Skill Find

## Arguments

```yaml
source: <auto>
ref: <auto>
scope: <auto>
query: <auto>
target: <auto>
profiles: <auto>
```

- `source` — repository, directory, URL, or other explicit Skill source. `<auto>` uses an explicit or live task source when available, otherwise defaults to `mols3131d/mols-agent-assets`.
- `ref` — branch, tag, commit, or equivalent source revision. `<auto>` uses the live/current ref when known, otherwise the source default.
- `scope` — repository area or capability set allowed for discovery. `<auto>` follows the caller's intent and repository-declared Skill surfaces without widening beyond the source.
- `query` — capability need. `<auto>` infers it from the user or caller; for inventory/sync intent, enumerate all in-scope candidates.
- `target` — intended agent/chatbot harness. `<auto>` uses the active harness and its actual capabilities.
- `profiles` — Skill locations or target profiles to inspect. `<auto>` discovers them from repository instructions, documentation, and structure instead of assuming fixed paths.

`<auto>` is an inference sentinel. Resolve values from explicit user input, live task context, repository evidence, then current harness capabilities. The `source` fallback exists for dogfooding and is not a scope lock: an explicit source always overrides it. Do not expand to unrelated public sources automatically.

## Contract

This Skill is **read-only discovery**. It owns finding, identity grouping, target-fit selection, and handoff to an installation capability.

It does not:

- install, update, rename, delete, or overwrite Skills;
- mutate repository files;
- infer repository conventions from one ecosystem or platform when the source defines its own;
- recommend duplicate target variants as separate capabilities when they are sibling projections of the same Skill.

## Discovery

### Resolve the source

Confirm `source`, `ref`, and `scope` from live evidence. For a repository source, read only enough governing context to discover Skill placement and semantics, such as applicable instructions, README material, or asset-profile documentation.

Do not assume that `skills/`, `skills-chatbot/`, `SKILL.md`, or `*.skill.md` are universal conventions. Use them when the source or active platform establishes them.

### Enumerate candidates

Discover candidate Skills inside the resolved scope. For each candidate, inspect the smallest sufficient material needed to determine:

- name and description;
- activation intent and negative boundary;
- responsibility and intended outcome;
- package/runtime dependencies;
- target profile or deployment shape when relevant.

For a specific `query`, stop once the relevant candidate set is sufficiently covered. For inventory/sync intent, enumerate the full in-scope set.

### Group capability identity

Names are strong signals, not identity by themselves. Treat candidates as the same capability when evidence shows continuity in responsibility, activation, outcome, behavioral contract, provenance, or repository history.

Use strong evidence first:

- stable identity, provenance, previous-name metadata;
- repository history showing rename, move, replacement, or projection;
- matching responsibility, activation, outcome, and core contract.

Do not merge candidates merely because their names or domains are similar.

When identity is not clear enough for a destructive downstream decision, mark it `uncertain` rather than forcing a match.

### Select target-specific siblings

When the same capability exists in multiple target profiles, return the sibling set as one capability and choose at most one preferred variant for `target`.

Prefer the **simplest sufficient variant**:

- choose a bundled/runtime variant when the target supports its required resources or tools and those materially improve or enable the capability;
- choose a self-contained/flat variant when it provides the same capability without meaningful runtime benefit or when dependencies are unsupported;
- do not prefer a variant because it has more files, more instructions, or a more complex profile name.

If no variant can preserve the capability on the target, return the capability as unsupported rather than silently degrading it.

## Handoff

Return discovery results in a form that `mols-skill-install` can consume. For each capability, preserve at least:

```yaml
capability: <name-or-identity>
source: <resolved-source>
ref: <resolved-ref>
scope: <resolved-scope>
target: <resolved-target>
preferred: <candidate-path-or-id | null>
siblings: []
identity: confirmed | probable | uncertain
notes: <only material selection or compatibility notes>
```

For inventory/sync, return one record per capability, not one record per sibling variant.

## Output

Answer the caller's discovery intent first.

- For a single capability query, show the best match and meaningful alternatives only.
- For inventory/sync, return the complete capability selection set.
- Expose unsupported or identity-uncertain cases that require a decision.
- Do not include installation instructions unless the caller asks; hand mutation ownership to `mols-skill-install`.
