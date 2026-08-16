# Rule Ownership

Use this reference only when deciding which rule source is authoritative.

## Source of Truth

Determine authority from project rules, configuration, generation flow, explicit caller direction within project authority, or other concrete evidence. A rule's current file location is not authority by itself.

When no authoritative source can be determined safely, preserve the current state and report unresolved ownership.

## Canonical Source

Prefer one authoritative source for each rule when the project and runtime allow it. The canonical source may be different from the runtime files that ultimately load the rule.

Do not use ownership decisions to broaden or narrow the rule's intended scope. Scope is resolved separately.

## Generated and Derived Copies

A generated, converted, or otherwise derived rule file is a projection of its authoritative source unless project evidence explicitly makes it authoritative.

Do not count required projections as independent rule ownership, and do not delete or hand-edit them merely because their text is duplicated.

Do not perform generation, conversion, or cross-harness synchronization as part of this reference.

## Ownership Conflicts

If multiple files claim authority and project evidence does not resolve the conflict, do not choose one by preference. Preserve the current state and report the conflict.
