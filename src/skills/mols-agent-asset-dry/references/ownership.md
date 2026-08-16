# Ownership

Use this reference only when deciding which source owns repeated agent-asset content.

## Source of Truth

Determine authority from project rules, configuration, generation flow, explicit caller direction within project authority, or other concrete evidence. A file's current location or age is not authority by itself.

When authority cannot be resolved safely, preserve the current state and report the conflict.

## Canonical Ownership

Prefer one authoritative owner for a requirement or responsibility when the asset model can preserve behavior with one owner. Ownership must not change activation, scope, permissions, outputs, or lifecycle.

A canonical owner may be different from the files that eventually load or expose the content.

## Generated and Derived Copies

Generated, converted, vendored, or otherwise derived assets are projections unless project evidence explicitly makes them authoritative.

Do not count required projections as independent ownership. Do not delete or hand-edit them merely because their text is repeated.

If changing the authoritative source requires regeneration or synchronization outside the current task, preserve the current state and report that boundary rather than leaving projections stale.

## Independent Capsules

Physical repetition can be correct when assets intentionally have independent ownership or release lifecycles. Do not create hidden sibling dependencies solely to centralize text.

## Ownership Conflicts

If multiple assets claim authority and evidence does not resolve the conflict, do not choose one by preference. Report unresolved ownership.
