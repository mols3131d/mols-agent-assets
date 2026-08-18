# Improve

Use this workflow when an existing agent asset needs a focused quality or behavior
improvement. If structural redesign is the primary objective, use
[refactor.md](refactor.md). If fitting an existing Skill to a specific project is
the primary objective, use [tune.md](tune.md).

## Orient

- Read the target, applicable project authority, nearby owners, and relevant
  checks.
- State what should improve and what must remain true.
- Set the write boundary before mutation.
- Distinguish desired behavior from accidental wording or incidental structure.

## Improve

- Make the smallest coherent change that solves the stated problem.
- Preserve authority, activation, safety, and ownership unless the request
  explicitly changes them.
- Prefer simplification, deletion, or clearer ownership over another abstraction
  layer.
- Incidental structural edits may stay here; do not switch workflows merely
  because a file moved.
- When substantial new Skill functionality is added, apply an applicable
  project-owned Skill authoring specification to the new or materially changed
  structure without normalizing unrelated parts.

## Check

Compare the result with both the requested improvement and preservation
requirements. Check affected paths, links, schemas, scripts, and deterministic
project checks when applicable.

Use [review.md](review.md) or [validate.md](validate.md) when read-only semantic
review or deterministic evidence is requested or required. Do not repeat review
loops without a concrete finding or failed check.

Report what changed, what was intentionally preserved or changed, checks actually
performed, and unresolved findings.
