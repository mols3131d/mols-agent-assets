# Subagent Orientation Pattern Research

## Goal

Improve `docs/references/patterns/context-engineering/subagent-orientation.md` as a reusable pattern capsule without turning it into a mandatory taxonomy, vendor-specific guide, or implementation procedure.

## Evidence

- The pattern library requires self-contained capsules with clear core and boundaries while leaving nonessential filenames, tools, formats, and workflows flexible.
- Agent Asset design principles prioritize Standard First, YAGNI, SRP, DRY, KISS, and Progressive Disclosure.
- The current pattern correctly treats `Role-oriented` and `Capability-oriented` as an orientation continuum rather than exclusive subagent types.
- The current document mixes two related but distinct concerns:
  - **Responsibility orientation** — what primarily defines the subagent: role/judgment boundary or bounded capability.
  - **Execution/context boundary** — whether work happens in shared or isolated context and what crosses the handoff.
- Capability-oriented work often benefits from isolation because investigation and tool output can stay out of the parent context, but role-oriented work can also be isolated and capability-oriented work can sometimes run in shared context.
- Agent Skills are an open, portable asset format. Some runtimes add isolated execution on top of Skills; VS Code currently documents experimental `context: fork`, which runs a Skill in a dedicated subagent context and returns only the final result.
- Therefore Skill and Subagent are not clean competing asset categories: a Subagent may use Skills, and a Skill may be executed inline or in an isolated runtime boundary when the harness supports it.

## Findings

1. Preserve the `Role-oriented ↔ Capability-oriented` continuum as the pattern's primary orientation concept.
2. Add a separate `Shared ↔ Isolated` execution/context dimension rather than redefining Capability-oriented as isolation.
3. Keep context isolation as a strong reason to introduce a Capability-oriented Subagent, especially for bounded work with noisy intermediate context.
4. Treat handoff as the boundary contract: pass the minimum sufficient result, evidence, uncertainty, blocker, and side-effect/verification state needed by the caller.
5. Reframe Skill comparison around **where a capability executes and what context crosses the boundary**, not `Skill vs Subagent` as mutually exclusive choices.
6. Describe forked Skill execution as an implementation option/example, not part of the pattern core. Vendor-specific semantics stay with the vendor authority.
7. Avoid claiming Subagent formats are more portable than Skills. The vendor-neutral part is the architectural idea of isolated delegated execution plus handoff, not a common Subagent schema.

## Uncertainty

- Runtime-specific isolation, context inheritance, tool permissions, persistence, and handoff semantics vary and should remain outside this pattern.
- `context: fork` is currently experimental and should be cited only as a current example, not as a durable invariant.
