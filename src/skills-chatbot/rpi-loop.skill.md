---
name: rpi-loop
description: >-
  Improve a difficult task through repeated Research → Plan → Implement → Review
  loops with explicit validation and finding-driven iteration. Use when the user asks
  for deeper reasoning, iterative improvement, multiple review passes, adversarial
  checks, or an RPI loop rather than a single-pass answer.
metadata:
  - target:
      - "OpenAI ChatGPT"
---

# RPI Loop

Use complete **Research → Plan → Implement → Review** loops to improve the current
task. Repetition without a new finding, evidence gap, perspective, or validation method
does not count as another loop.

## Defaults

```yaml
max_loops: 10
stop_condition: review_has_no_material_findings
```

- If the user specifies a loop count, follow it unless blocked.
- Otherwise stop when Review has no material findings or `max_loops` is reached.
- If the limit is reached with findings remaining, report them instead of hiding them.

## Loop

Every completed loop contains all four phases. A phase may be brief when little work is
needed, but it is not skipped.

### Research

Refresh only the evidence needed for the current problem or unresolved findings.
Discover missing information, investigate high-impact questions, challenge weak
assumptions or counterexamples, and synthesize conclusions that can drive the plan.

### Plan

Define the current objective, scope, constraints, acceptance conditions, approach,
trade-offs, work units, and validation points. Prefer the smallest plan that can resolve
the current findings.

### Implement

Perform the actual requested work, integrate it with existing context and constraints,
then validate it against the plan and available evidence. Do not claim checks that were
not actually performed.

### Review

Search for remaining material problems in correctness, completeness, consistency,
usability, assumptions, edge cases, evidence, and validation. Deduplicate findings and
decide whether another loop is justified.

## Context Composition

RPI coordinates the loop; it does not need to own every domain rule.

At each phase, activate a specialized Skill only when its context materially improves the
current phase. Examples include external-research context for evidence gathering,
engineering-decision context for design trade-offs, or writing context for a reader-facing
deliverable.

- Do not preload every possibly relevant Skill.
- Do not restate a specialized Skill's rules inside RPI.
- Let the specialized Skill remain the canonical owner of its domain procedure or lens.
- Drop phase-specific context when it is no longer relevant instead of carrying it through
  the whole loop by default.
- If no specialized Skill is needed, use the model's normal capability rather than
  inventing an extra routing layer.

## Loop Discipline

A Review finding must be actionable, material, relevant to the requested outcome, and
supported by evidence or a clearly identified reasoning gap.

A later loop requires at least one meaningful delta:

- unresolved finding;
- new evidence;
- changed assumption or plan;
- new perspective or counterexample;
- different validation method.

Do not invent findings to keep looping. Cosmetic preference, rereading, restating the
same issue, or repeating the same search does not create a new loop.

Preserve confirmed conclusions unless new evidence justifies reopening them.

## Validation

Choose validation that fits the task: source cross-checking for research, tests or code
inspection for implementation, source-to-output comparison for rewriting, requirement
checks for design, or counterexample search for analytical claims.

Increase reasoning quality through better evidence, alternatives, contradiction tests, and
validation—not through longer narration.

## Output

Do not expose private reasoning or verbose phase-by-phase narration by default. Return:

- the improved result;
- completed loop count;
- material changes or conclusions;
- unresolved findings or checks that could not be performed.

Show detailed per-phase work only when the user requests it or it is necessary to
understand the result.
