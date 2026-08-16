# Rule Ownership

Use this reference only when deciding whether repeated rule content already has an authoritative source or is eligible for canonicalization.

## Established Authority

Determine established authority from project rules, configuration, generation flow, explicit caller direction within project authority, or other concrete evidence. A rule's current file location, age, or similarity to another copy is not authority by itself.

When authority is established, preserve it. The canonical source may be different from the runtime files that ultimately load or expose the rule.

Do not use ownership decisions to broaden or narrow the rule's intended application. Application is resolved separately.

## Peer Copies

When no source has established authority, equivalent ordinary editable copies are eligible for canonicalization if all of these hold:

- the copies express the same requirement;
- no copy has a distinct ownership or projection role;
- the write boundary permits the required mutations; and
- the resolved application can be preserved without changing precedence.

Do not select the new owner here. Placement chooses the native owner or owners after ownership status is resolved.

## Generated and Derived Copies

Treat a rule file as a projection only when an evidenced generation, conversion, or derivation flow establishes that relationship. Do not infer projection status from duplicate text or location alone.

Do not count required projections as independent rule ownership, and do not delete or hand-edit them merely because their text is duplicated.

If changing the authoritative source requires regeneration or synchronization outside the current task, preserve the current state and report that boundary rather than leaving required projections stale.

Do not perform generation, conversion, or cross-harness synchronization as part of this reference.

## Ownership Conflicts

If multiple sources have conflicting evidence of authority or a required ownership relationship cannot be resolved, do not choose one by preference. Preserve the current state and report the conflict.
