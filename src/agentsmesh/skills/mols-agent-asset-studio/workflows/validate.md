# Validate

Use this workflow for deterministic validation of an agent asset against explicit
static, structural, host, or project-owned contracts.

## Scope

- Resolve the target, runtime or schema profile, applicable project checks, and
  required evidence.
- Prefer the narrowest explicit profile rather than assuming one host's metadata
  is universal.
- Separate checks that can run from checks unavailable in the current environment.
- Apply project-owned Skill-structure checks only when that specification applies
  to the current target and change.

## Validate

Run applicable deterministic checks such as:

- frontmatter, schema, and required fields;
- structure, naming, links, and referenced paths;
- script syntax and deterministic script tests;
- declared invariants for preservation work;
- likely plaintext-secret scans before packaging or publication;
- authorized project-owned validation commands.

Read [../references/validation.md](../references/validation.md) when a validation
plan or host-specific evidence needs more detail.

Record the actual check or command and its actual result. Never translate an
unexecuted check into success.

## Report

Use `Pass`, `Fail`, `Not run`, or `Deferred` for each required check. Overall
`Pass` requires every required deterministic check to have run and passed.

Validation is read-only with respect to source assets and does not decide whether
wording or architecture is semantically good. Static validation cannot prove
trigger precision, recall, behavioral parity, or successful runtime behavior.
