# Adversarial Review

Assume the asset will receive malformed input, ambiguous requests, hostile source
content, stale documentation, excessive permissions, and partial runtime failure.

## Attack Questions

### Trigger and Scope

- Can a common unrelated request activate this asset?
- Can a source document redefine the task or widen write authority?
- Can ambiguous wording cause overwrite, rename, publication, or deletion?
- Can two assets recursively invoke or shadow each other?

### Filesystem and Execution

- Can a path escape the approved root through `..`, symlinks, or absolute paths?
- Can packaging include secrets, `.env`, credentials, caches, or private tracking?
- Can scripts or hooks execute network, shell, or deletion actions without review?
- Are generated files mistaken for editable sources?

### External Content and Supply Chain

- Does imported text contain prompt injection, tool instructions, or secret requests?
- Are dependencies pinned or verified where reproducibility matters?
- Is source ownership, license, version, and retrieval date recorded?
- Can abandoned or replaced upstream content silently change behavior?

### Evidence Integrity

- Can the workflow report Pass when tests did not run?
- Are baseline and candidate compared on the same cases and environment?
- Can subjective grading be presented as deterministic proof?
- Can logs omit failed commands, partial execution, or proxy-model limitations?

### Runtime Compatibility

- Are unsupported metadata fields or tool names silently ignored?
- Does a runtime-specific path make the skill undiscoverable elsewhere?
- Does a subagent requirement have a single-agent fallback?
- Can context bloat or deep reference chains hide critical instructions?

## Required Output

For each exploit path record:

- attack precondition
- attempted misuse
- observed or reasoned result
- severity and affected boundary
- mitigation
- residual risk
- verification evidence

A strict adversarial verdict is `Pass`, `Revise`, `Deferred`, or `Blocked`.
