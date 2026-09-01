# Skill Lifecycle

Use this reference for Agent Skill authoring, review, validation, and bounded improvement.

## Authority

Resolve Skill decisions from the actual source and target rather than one universal schema:

1. The active source framework owns the canonical authored representation.
1. Apply a portable Agent Skills contract only when it actually governs the source or target.
1. The selected target or harness owns target-specific discovery, metadata, permissions, packaging, and runtime behavior.
1. Project conventions own only local behavior not already decided above.
1. Skill-local contracts and established intent remain binding inside their scope.

Do not convert a target projection into canonical source by assumption. When a source framework projects one canonical Skill into target surfaces, edit the canonical source and treat generated projections as derived.

When exact or current target behavior can affect the change, read the current authoritative target documentation. If that target provides an official Skill creator or authoring guide, use it as target-specific guidance rather than a portable standard.

## Design

### Responsibility and activation

A Skill should own a coherent capability that is useful to select as a unit.

- Define what the Skill enables and what responsibility it does not own.
- Treat selection metadata as an activation surface, not as a summary for humans only.
- Put the information required to select the Skill in metadata that is available before activation; do not rely on body instructions that are loaded only after selection.
- Express both what the Skill does and the contexts or intents in which it should be used.
- When a nearby Skill is easy to confuse with it, include only the boundary needed to separate realistic near-miss requests.
- Prefer intent and task language over brittle keyword lists.

For a new or materially changed Skill, inspect representative intended use and at least one plausible non-use or near-miss when activation boundaries are not obvious. Formal trigger evaluation belongs to the validator when stronger evidence is required.

### Package and progressive disclosure

Prefer the smallest deployable Skill package that preserves the required behavior.

- Let the governing source or target specification own required package names, fields, directories, and discovery semantics; do not mirror that schema here.
- Keep instructions needed on every activation in the entrypoint and move conditional detail behind directly discoverable references.
- Link supporting resources from the entrypoint with a clear condition for when to read or use them.
- Avoid reference chains that materially increase retrieval cost or hide required context.
- Add scripts when repeated deterministic mechanics or reliability justify executable behavior instead of prose.
- Add output assets only when the runtime or task consumes them; do not load them as reasoning context without need.
- Keep repository-only verification or maintainer artifacts outside the deployable Skill surface unless the governing runtime explicitly requires them.
- Avoid supporting `SKILL.md` files that a host could discover as separate Skills; use non-entrypoint filenames for supporting material.

### Instruction precision

Match the degree of instruction to the task:

- leave room for judgment when many approaches are valid;
- give preferred structure when consistency matters but local adaptation is expected;
- use deterministic mechanics or narrow procedures when order, safety, or reproducibility is fragile.

Do not teach the model generic knowledge merely to make the Skill look comprehensive. Include non-obvious procedural knowledge, local contracts, reusable resources, and failure boundaries that materially improve execution.

### Change and adaptation

Prefer improving an accepted owner to creating a competing Skill.

For an existing Skill, preserve its essential responsibility and valid behavior unless the request changes them. Distinguish that intent from incidental wording, folder layout, or obsolete target assumptions.

For target or project adaptation:

- preserve portable intent;
- replace incompatible assumptions with project-native or target-native mechanisms;
- isolate target-specific representation instead of universalizing it;
- do not weaken useful behavior merely to reach the lowest common denominator;
- prefer reading live project authority over copying project documentation into the Skill.

Do not normalize frontmatter, folders, metadata, or packaging merely because a Skill is being touched. Apply only contracts that actually govern the current source, target, and change.

## Review

Inspect at least the axes that can affect the requested behavior:

- **Responsibility** — is the capability coherent and owned once?
- **Activation** — can intended requests select it, while realistic near-miss requests remain distinguishable?
- **Description quality** — does selection metadata contain the pre-activation information needed to choose the Skill without becoming a catalog of implementation detail?
- **Progressive disclosure** — is always-loaded context limited to what every activation needs, and are conditional resources directly discoverable?
- **Instruction precision** — are constraints proportional to failure cost rather than over-prescriptive or underspecified?
- **Package** — do references, scripts, and output assets each provide a concrete benefit and live on the correct runtime surface?
- **Authority** — are portable intent, source-framework representation, target-specific behavior, and local deltas kept distinct?
- **Regression** — did the change preserve established responsibility, useful behavior, and supported target assumptions that remain valid?

Static review can identify obvious activation or structure problems, but it does not prove runtime selection, behavioral parity, or compatibility.

## Validate

Use evidence that matches the claim:

- inspect metadata, entrypoint, resource links, and package boundaries directly;
- run the repository or source framework's existing Skill validation for machine-checkable package and metadata contracts;
- inspect generated projections only when target representation is part of the claim;
- use actual runtime selection or behavioral evaluation only when claiming trigger precision, behavioral stability, or compatibility.

When runtime evidence is unavailable, separate what is structurally verified from what remains inferred or unknown. A valid package can still be a poorly routed or ineffective Skill.
