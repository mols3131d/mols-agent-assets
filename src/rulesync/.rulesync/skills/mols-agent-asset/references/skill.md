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

Prefer the smallest deployable Skill package that preserves the required behavior.

- Let the governing source or target specification own required package names,
  fields, directories, and discovery semantics; do not mirror that schema here.
- Add supporting resources only when they provide a concrete runtime, loading, or
  deterministic-mechanics benefit.
- Put conditional detail behind an explicit load condition so always-loaded context
  stays focused on decisions needed for every activation.
- Keep repository-only verification or maintainer artifacts outside the deployable
  Skill surface unless the governing runtime explicitly requires them.
- Avoid supporting `SKILL.md` files that a host could discover as separate Skills;
  use non-entrypoint filenames for supporting material.

When a repository defines package or Markdown conventions, apply that live project
authority rather than copying it into the Skill.

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
