# Duplicate Rules

Use this reference only when deciding whether two or more rules are redundant.

## Same Rule

Treat rules as duplicates only when all of these match:

- operational requirement;
- intended target scope; and
- exception or override intent.

Similar wording is only a clue. Different wording may express the same rule, and similar wording may express different policy.

## Inherited Duplication

If a parent `AGENTS.md` rule already applies unchanged to a child scope, repeating it in the child is duplication. Keep only the child-specific delta or exception.

Do not copy parent text into a child merely to make the child file self-contained.

## Redundant Exceptions

A narrower rule is not an exception when it only restates what the broader rule already requires. Remove the restatement.

Keep a narrower rule when it genuinely changes, limits, or overrides the broader rule for that scope.

## Ambiguity

If rule equivalence or exception intent is unclear, preserve the existing rules and report unresolved duplication. Do not infer policy merely to remove repetition.
