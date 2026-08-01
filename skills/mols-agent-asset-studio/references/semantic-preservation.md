# Semantic Preservation

Use this contract for `refactor`, compression, restructuring, and consolidation
work that claims behavior preservation.

## Preserve Explicitly

- activation triggers and near-miss exclusions
- frontmatter capability and authority fields
- commands, paths, URLs, API names, versions, and numeric thresholds
- required headings or output fields
- safety constraints, stop rules, and permission boundaries
- ordering where changing order changes behavior
- completion evidence and verdict meanings

## Usually Remove or Reduce

- filler, hedging, and decorative prose
- duplicated rules and examples
- prose that merely repeats a table or code block
- obsolete compatibility notes already enforced elsewhere

## Procedure

1. Capture observable behavior and literal invariants in
   `templates/behavior-invariants.yaml`.
1. Run `scripts/check_invariants.py <target-root> <invariants.yaml>` before edits.
1. Apply the smallest coherent change.
1. Run the same invariant check after edits and compare behavior cases.
1. Treat a missing invariant as `Revise`, not as acceptable compression loss.

Literal checks do not prove full semantic equivalence. They protect fragile facts
while general and behavior review establish the broader contract.
