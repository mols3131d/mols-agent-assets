# Rule Ownership

Use this reference only when deciding which rule source is authoritative.

## Source of Truth

Preserve a source of truth only when project rules, configuration, generation flow, or other evidence establishes it. A rule's current file location is not authority by itself.

When no authoritative source can be determined safely, preserve the existing rules and report unresolved ownership.

## Canonical Owner

When the runtime can represent the intended scope exactly, prefer one canonical owner for each rule.

Choose the owner only after the intended scope is known. Ownership must not broaden or narrow the rule's policy.

## Generated and Derived Copies

A generated, converted, or otherwise derived rule file is not an independent source of truth unless the project explicitly makes it authoritative.

Keep derived copies only when the runtime or delivery process requires them. Treat them as projections of the authoritative rule rather than competing owners.

Do not perform cross-harness generation, conversion, or synchronization as part of this skill.

## Ownership Conflicts

If multiple files claim authority and project evidence does not resolve the conflict, do not choose one by preference. Preserve the current state and report the ownership conflict.
