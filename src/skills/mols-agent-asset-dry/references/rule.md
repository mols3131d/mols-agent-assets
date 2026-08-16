# Rule DRY

Use this reference for reusable guidance attached by a host as persistent, scoped, relevance-selected, agent-requested, or manual rule context.

## Preserve

Preserve rule meaning, discovery or selector metadata, attachment mode, intended activation or target set, source authority, load timing, and runtime precedence.

A rule contributes guidance to another task. Do not turn a manual or selectively attached rule into an always-loaded rule merely to remove repetition.

## Attachment Model

Discover the host's supported rule modes rather than assuming one universal model. Common patterns include:

- always or project-wide attachment;
- directory, file, path, or glob attachment;
- relevance-based or agent-requested attachment; and
- explicit manual attachment.

Different attachment modes are meaningful behavior even when rule text is identical.

## Current and Intended Activation

Derive both where each rule currently applies and where it is intended to apply. Do not assume current location, selector, or attachment mode proves intended scope.

For directory or selector rules, compare actual target sets. For relevance or manual rules, preserve the discovery description and explicit selection boundary.

## Scope and Placement

When a directly loaded rule uses directory or selector scope, prefer the smallest supported placement that represents the intended targets exactly. Use inherited directory placement for one exact subtree and a pattern rule for cross-cutting targets when the host supports those mechanisms.

If one owner cannot express the intended activation set exactly, keep the smallest correct set of owners even when physical repetition remains. Activation correctness outranks DRY.

## Inheritance, Overlap, and Precedence

Remove narrower restatements when a broader applicable rule already supplies the same requirement unchanged. Keep genuine exceptions and intentionally different attachment modes.

Overlap alone does not prove duplication. Treat directory depth, selector specificity, source type, attachment mode, and load order as behavior when the runtime uses them. Do not move a rule across a precedence boundary unless the effective rule set remains unchanged. If relevant precedence cannot be determined, preserve the placement and report the uncertainty.

## Generated Rule Layers

If runtime rule files are generated from a canonical input layer, preserve that source model. Do not apply direct-runtime placement rules to generated outputs.

## Verify

Check representative automatic, scoped, relevance-selected, or manual activation paths that the affected rules actually use. Verify the full affected target set when feasible; otherwise report sampled coverage.
