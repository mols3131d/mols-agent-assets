# Rule DRY

Use this reference only for persistent or scoped agent rules such as `AGENTS.md`, repository instructions, or path/glob rule assets.

## Preserve

Preserve rule meaning, intended target set, source authority, load timing, and runtime precedence.

Derive both the **current scope** and the **intended scope**. Do not assume a rule's current location proves where it should apply.

## Scope and Placement

For directly loaded directory or selector rules, prefer the smallest supported placement that represents the intended targets exactly:

- Project-wide scope -> project-wide rule owner.
- One directory subtree -> the highest directory rule whose inherited subtree is still exact.
- Cross-cutting file, extension, path, or repeated-directory scope -> a matching pattern rule when supported.

If one owner cannot represent the intended target set exactly, keep the smallest correct set of owners even when physical repetition remains. Scope correctness outranks DRY.

## Inheritance and Overlap

Remove narrower restatements when a broader rule already supplies the same requirement unchanged. Keep genuine narrower exceptions.

For overlapping selectors, compare the actual target sets. Overlap alone does not prove duplication; requirement equivalence is decided separately.

## Precedence

Treat directory depth, selector specificity, source type, and load order as behavior when the runtime uses them. Do not move a rule across a precedence boundary unless the effective rule set remains unchanged. If relevant precedence cannot be determined, preserve the placement and report the uncertainty.

## Generated Rule Layers

If runtime rule files are generated from a canonical input layer, preserve that source model. Do not apply direct-runtime placement rules to generated outputs.

## Verify

Check intended targets and nearby non-targets around inheritance and selector boundaries. Verify the full affected set when feasible; otherwise report sampled coverage.
