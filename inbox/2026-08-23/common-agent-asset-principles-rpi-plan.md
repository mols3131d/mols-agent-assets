# Common Agent Asset Principles RPI Plan

Based on `common-agent-asset-principles-rpi-research.md`.

## Goal

Strengthen the two common references while keeping them small, vendor-neutral, and clearly separated by responsibility.

## Changes

1. `design-principles.md`
   - preserve the existing six-principle order;
   - make need/evidence and concern-specific ownership explicit inside existing principles rather than adding another named principle;
   - add a compact mechanism-selection rule so prose instructions are not used where a stronger deterministic/native owner exists;
   - make context cost an application test of KISS + Progressive Disclosure;
   - tighten guardrails and add a clear boundary to `instruction-authoring.md`, Patterns, and runtime/source authority;
   - remove weak or nonessential background sourcing if it does not carry a design decision.
1. `instruction-authoring.md`
   - sharpen the behavior contract around condition, action, boundary and observable verification/stop behavior;
   - state each instruction once and separate normative rules from explanatory context;
   - calibrate force and procedure detail to failure cost/fragility;
   - avoid invented precedence; prefer narrow scope and conflict removal, using precedence only when the governing runtime/authority supports it;
   - define defaults, escape/fallback conditions, and true invariants;
   - clarify when examples/templates are useful without letting examples become hidden authority;
   - keep formal eval and runtime-specific semantics outside this document.
1. Re-read both together for DRY and responsibility leakage, then review against current official Agent Skills, OpenAI, Anthropic, and GitHub guidance.

## Acceptance

- A reader can tell which document answers “should this local asset/instruction exist and where?” versus “how should this chosen instruction be written?”
- The six design principles remain recognizable and in the established priority order.
- KISS is not reduced to fewer words/files/steps.
- Local instructions require a real local delta or credible invariant rather than speculative future need.
- Concern-specific authority and stronger native/deterministic mechanisms are not displaced by prose.
- Instruction force, specificity, defaults, conflicts, fallback/stop behavior, examples, and validation have clear rules without becoming a prompt-engineering textbook.
- No vendor-specific precedence, file path, frontmatter, or runtime behavior is defined as a common invariant.
- No new schema, pattern, asset type, or supporting reference is introduced without a demonstrated need.