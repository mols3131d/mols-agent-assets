# Skill

Use this reference only for Agent Skill authoring or material Skill changes.

## Authority

Resolve Skill decisions from the actual source and target rather than one universal
schema:

1. The active source framework owns the canonical authored representation.
1. Apply the portable Agent Skills contract when it actually governs the source or
   target.
1. The selected target or harness owns target-specific discovery, metadata,
   permissions, packaging, and runtime behavior.
1. Project conventions own only local behavior not already decided above.
1. Skill-local contracts and established intent remain binding inside their scope.

Do not convert a target projection into canonical source by assumption. When a
source framework such as Rulesync projects one canonical Skill into target
surfaces, edit the canonical source and treat generated projections as derived.

When exact or current target behavior can affect the change, read the current
official target documentation. If that target provides an official Skill creator
or authoring guide, use it as target-specific guidance rather than a portable
standard.

If current authoritative source material is unavailable, preserve the established
source shape, avoid inventing target-specific fields, paths, packaging, permissions,
or creator behavior, and expose the compatibility gap when it can affect the
result.

## Package

Prefer the smallest deployable Skill package.

- Start with `SKILL.md`.
- Add `references/`, `scripts/`, `assets/`, or templates only when the runtime
  actually needs them.
- Keep discovery information in the description and loaded behavior in the body.
- Keep runtime-required knowledge inside the deployable Skill surface.
- Keep repository verification such as tests and eval fixtures outside the runtime
  package.
- Do not create maintainer documentation merely because a Skill is directory-based
  or was edited. Use a project-defined maintainer surface only when durable
  rationale, recovery knowledge, or fragile invariants materially lower future
  maintenance cost.
- Avoid nested `SKILL.md` files for supporting material because hosts may interpret
  them as separate discoverable Skills.

Use multiple top-level Markdown sections when they provide real responsibility
boundaries; do not split a readable single-file Skill only because it is long.

## Change

Prefer improving an accepted owner to creating a competing Skill.

For an existing Skill, preserve its essential responsibility and valid behavior
unless the request changes them. Distinguish that intent from incidental wording,
folder layout, or obsolete target assumptions.

For target or project adaptation:

- preserve portable intent;
- replace incompatible assumptions with project-native or target-native mechanisms;
- isolate target-specific representation instead of universalizing it;
- do not weaken useful behavior merely to reach the lowest common denominator;
- prefer reading live project authority over copying project documentation into
  the Skill.

Do not normalize frontmatter, folders, metadata, or packaging merely because a
Skill is being touched. Apply only contracts that actually govern the current
source, target, and change.

## Check

After a material Skill change, inspect at least:

- responsibility and trigger boundary;
- source versus target ownership;
- referenced runtime resources;
- unnecessary always-loaded context;
- accidental vendor-specific assumptions in portable guidance;
- regression of established intent;
- applicable deterministic project checks.

Static review can find obvious trigger or structure problems, but it does not prove
runtime selection, behavioral parity, or compatibility.
