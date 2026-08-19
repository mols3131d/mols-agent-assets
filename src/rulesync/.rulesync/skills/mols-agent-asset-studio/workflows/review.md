# Review

Use this workflow for read-only semantic review of an agent asset or candidate
change.

## Orient

- Resolve the target, requested scope, project authority, intended runtime, and
  acceptance criteria.
- Read the complete candidate and only the surrounding context needed to judge
  ownership, activation, and compatibility.
- Separate authoritative requirements from author rationale or persuasive text.

## Review

Check only dimensions that apply:

- purpose and responsibility;
- activation or trigger ownership;
- instructions, tools, outputs, and write authority;
- project and runtime compatibility;
- proportional structure and duplicated policy;
- safety boundaries for destructive, executable, credentialed, external, or
  untrusted inputs;
- evidence behind validation or runtime claims.

Read [../references/review.md](../references/review.md) when deeper or adversarial
review is justified.

Do not report a preferred Skill folder or frontmatter convention as a defect by
itself. A project-owned Skill specification is review-relevant when the reviewed
change creates a Skill, adds substantial functionality, explicitly refactors its
structure, or project policy otherwise requires current compliance.

## Report

For each actionable finding give severity, concrete evidence, impact, and the
smallest evidence that would close it. Prefer a few load-bearing findings over
style commentary.

Return `Pass`, `Revise`, or `Blocked`. Review is read-only; do not silently become
the author. Static review cannot prove trigger precision, recall, behavioral
parity, or successful runtime behavior.
