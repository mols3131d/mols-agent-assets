# v2.1 Adversarial Review

## Initial Verdict

`Revise`

## Attack Findings Closed

### A21-001 — High — Invariant paths could resolve through a symlink

Required paths and file checks now reject symlinks and resolved paths outside the
approved root.

### A21-002 — High — Host validation could persist a secret printed by a command

Captured stdout and stderr now pass through the same redaction patterns used by
the package scanner. Raw matching values are not written to reports.

### A21-003 — Medium — Standalone structural audit did not reject symlinks

The audit rejects symlinks before directory and resource inspection.

### A21-004 — Medium — Structural warnings did not stop direct packaging

Skill and bundle packaging now block structural warnings unless the caller uses a
specific escape hatch after reviewing the exact finding.

## Residual Risk

- secret scanning is heuristic and does not replace an approved repository secret scanner;
- literal invariants do not prove semantic equivalence;
- runtime activation remains Deferred until executed by the target host;
- argv plans are trusted project policy and still require explicit execution authority.

## Closure Verdict

`Pass` for deterministic scope; live runtime behavior remains `Deferred`.
