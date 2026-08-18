# Validation Guidance

Use this reference for deterministic evidence. Validation does not decide whether
a semantic design is good.

## Structural Checks

A releasable runtime asset should have no:

- nested discoverable `SKILL.md` below its root;
- symlinks, path escapes, cache directories, or build output;
- empty directories or zero-byte resources;
- broken local links or missing referenced files;
- invalid script syntax.

Review warnings for unreferenced resources, executable scripts absent from the
operation map, placeholder filenames, and scripts with no test evidence.

## Runtime Profiles

Use the narrowest explicit runtime or schema profile. Do not assume metadata or
discovery rules are portable between hosts. A validator may prove static
conformance to a profile; it cannot prove runtime behavior.

A Studio profile validates only the named runtime or specification contract. It
does not prove conformance to a project-owned Skill convention unless that
convention is exactly the same contract.

## Project-Owned Checks

Use the project's existing authoritative checks and invocation mechanism. Do not
invent or require a Studio-specific project profile solely to run validation.
Execute commands only with explicit authority and a bounded working directory, and
record the exact command, exit state, and relevant output.

If project conventions are machine-checkable but no validator exists, report the
deterministic gap rather than treating semantic review as executed validation.

If a required check cannot run, report `Deferred` with a concrete rerun condition.
If it was simply not selected or attempted, report `Not run`. Neither state is
`Pass` evidence.

## Packaging Closure

Before distribution, run applicable static validation, structural hygiene, and
likely secret scanning. Package only accepted source; exclude caches, backups,
temporary workspaces, secrets, and unrelated work artifacts. Reproducible
packaging should produce stable content and manifests from identical accepted
source.
