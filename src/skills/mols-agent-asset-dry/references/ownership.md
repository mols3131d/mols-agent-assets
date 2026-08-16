# Ownership

Use this reference only when deciding which source owns repeated agent-asset content.

## Source of Truth

Determine authority from project rules, configuration, generation flow, explicit caller direction within project authority, or other concrete evidence. A file's current location or age is not authority by itself.

When authority cannot be resolved safely, preserve the current state and report the conflict.

## Canonical Ownership

Prefer one authoritative owner for a requirement or responsibility when the asset model can preserve behavior with one owner. Ownership must not change activation, scope, permissions, outputs, dependencies, or lifecycle.

A canonical owner may be different from the files that eventually load or expose the content.

## Generated and Derived Copies

Treat an asset as a projection only when a generation, conversion, or derivation flow establishes that relationship. Do not infer projection status from similar content or location alone.

Do not count required projections as independent ownership. Do not delete or hand-edit them merely because their text is repeated.

If changing the authoritative source requires regeneration or synchronization outside the current task, preserve the current state and report that boundary rather than leaving projections stale.

## Imported or External Assets

An imported, vendored, or externally maintained asset may have external ownership rather than being a generated projection. Preserve its ownership model unless project evidence explicitly transfers authority.

## Cross-Harness Copies

When repeated content exists in harness-specific native assets, resolve only whether source authority is duplicated. If removing physical duplication requires native reuse, generation, conversion, or fan-out across harnesses, report that as a synchronization boundary rather than designing or executing it here.

## Independent Assets

Physical repetition can be correct when assets intentionally have independent ownership or release lifecycles. Do not create hidden sibling dependencies solely to centralize text.

## Ownership Conflicts

If multiple assets claim authority and evidence does not resolve the conflict, do not choose one by preference. Report unresolved ownership.
