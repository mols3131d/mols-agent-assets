# Common Agent Asset Principles RPI Research

## Goal

Improve `docs/references/agent-assets/common/design-principles.md` and `instruction-authoring.md` as durable, asset-type-independent design references without turning them into a workflow guide, vendor manual, or pattern catalog.

## Current ownership

- `design-principles.md` owns cross-asset design judgment: Standard First / Local Delta Only, YAGNI, SRP, DRY, KISS, Progressive Disclosure, guardrails, and human comprehension.
- `instruction-authoring.md` owns how a chosen behavior is expressed as an instruction: trigger/action/constraint/validation, control calibration, and review questions.
- `docs/references/agent-assets/README.md` says common references own asset-type-independent durable design meaning, while recurring solution shapes belong to the Patterns library and repository workflow belongs to `docs/development/`.
- Skill-specific discovery/body/package semantics remain under `docs/references/agent-assets/skills/` and should not be copied into these common documents.

## External evidence

Current official guidance converges on a few durable ideas:

- Agent Skills: spend context on what the agent would otherwise get wrong; use coherent units, moderate detail, defaults rather than menus, control proportional to task fragility, progressive disclosure, and real execution/evaluation to justify retained instructions.
- OpenAI current model guidance: leaner prompts can improve both task performance and token efficiency; state each instruction once; keep examples only when they encode a real requirement or measured gap; define outcome, success criteria, hard constraints and stopping behavior; avoid unnecessary absolute rules and detailed step-by-step process when the exact path does not matter.
- Anthropic current prompting guidance: be clear and direct, add context when it materially improves judgment, use examples when they resolve ambiguity or encode target behavior, and calibrate prescriptiveness to task fragility rather than making every instruction equally rigid.
- GitHub Copilot current custom-instruction behavior shows that multiple instruction sources can be combined and that some surfaces do not define a general precedence order. Local prose therefore must not invent precedence that the runtime does not guarantee; conflicts should preferably be removed or scoped out.

## Findings

1. **The two documents need a sharper boundary.** `design-principles.md` should decide whether local agent-asset structure/instruction is justified and which owner/mechanism should hold it. `instruction-authoring.md` should only govern expression after that decision.
1. **Context cost should be an explicit design test, not a new slogan-principle.** It is already implied by KISS and Progressive Disclosure, but current official guidance makes the operational test clearer: retained context should prevent a real failure, preserve an invariant, or reduce material uncertainty.
1. **Mechanism choice is missing from the design gate.** A deterministic schema, permission, selector, validator, host setting, or source/target contract can be a stronger owner than prose. Prompting should not become the default way to encode mechanically enforceable behavior.
1. **Local Delta needs evidence, not speculation.** YAGNI should make clear that hypothetical future compatibility or imagined model failure is not enough; use observed requirements, accepted policy, real failure modes, or credible invariants.
1. **DRY needs concern-specific authority wording.** One concern should have one authoritative owner, but different concerns can legitimately have different authorities. Avoid implying one universal authority for an entire asset.
1. **`instruction-authoring.md` currently risks invented precedence.** “If conflict is possible, state scope and precedence” is too broad because some runtimes combine instruction sources without a guaranteed general precedence model. Prefer narrow scope and conflict removal; state precedence only when an applicable authority/runtime actually defines or permits it.
1. **Instruction force should match invariance.** `must`/`never`/`only` should be reserved for real invariants, safety/permission boundaries, required contracts, or fragile sequences. Defaults plus escape conditions are better for ordinary preferences.
1. **Stop/fallback behavior is under-specified.** Complex instructions should make failure, missing evidence, escalation, abstention, retry, or handoff observable when those outcomes matter.
1. **Examples should not silently become hidden rules.** Add examples only when they materially resolve ambiguity, encode a required format/behavior, or address a measured gap; keep the normative rule explicit and examples representative rather than exhaustive.
1. **Repetition is not authority.** State each behavioral rule once at its owning scope. Repeated emphasis increases context cost and can distort behavior.
1. **Formal eval workflow remains out of scope.** These references may require observable success criteria and representative review, but repository testing/eval mechanics remain under `docs/development/`.

## Preserve

- Existing priority order: Standard First / Local Delta Only → YAGNI → SRP → DRY → KISS → Progressive Disclosure.
- KISS means removing accidental complexity, not minimizing file count, stages, options, or prose length mechanically.
- Human comprehension remains a first-class design constraint.
- Durable rationale/invariants are preserved; ordinary change history remains in Git.

## Uncertainty

Vendor-specific instruction inheritance, precedence, discovery and runtime semantics change over time. The common documents should state only vendor-neutral design meaning and route exact semantics to the current authoritative source.