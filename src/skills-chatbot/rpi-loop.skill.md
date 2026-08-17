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

Improve the current task with complete **Research → Plan → Implement → Review** loops. A repeated pass counts only when new evidence, a material finding, a changed plan, a counterexample, or a different validation method can improve the result.

## Defaults

```yaml
max_loops: 10
stop_condition: review_has_no_material_findings
```

Follow a user-specified loop count unless blocked. Otherwise stop when Review has no material findings or `max_loops` is reached. If findings remain at the limit, report them.

## Loop

Every completed loop contains all four phases; a phase may be brief but is not skipped.

### Research

Refresh only evidence needed for the current objective or unresolved findings. Investigate high-impact gaps, weak assumptions, contradictions, and counterexamples. Stop when the plan can be grounded well enough to act.

### Plan

Set the current objective, scope, constraints, acceptance conditions, approach, work units, trade-offs, and validation points. Prefer the smallest plan that can resolve the current findings.

### Implement

Perform the requested work against the plan and current evidence. Preserve confirmed constraints and do not claim checks that were not performed.

### Review

Look for remaining material problems in correctness, completeness, consistency, usability, assumptions, edge cases, evidence, and validation. Deduplicate findings and decide whether another loop has a meaningful delta.

## Repeat Gate

Continue only when Review produces at least one actionable, material finding or another concrete reason to change the next pass:

- unresolved finding;
- new evidence;
- changed assumption or plan;
- useful counterexample or perspective;
- different validation method likely to change confidence.

Do not invent findings to keep looping. Cosmetic preference, rereading, restating the same issue, or repeating the same search is not a new loop. Preserve confirmed conclusions unless new evidence justifies reopening them.

## Context and Validation

Activate specialized context only when it materially improves the current phase. Do not preload every possibly relevant Skill or copy another Skill's rules into RPI.

Choose validation that matches the work: source cross-checking for research, tests or code inspection for implementation, source-to-output comparison for transformations, requirement checks for design, or counterexample search for analytical claims.

Improve quality through better evidence, alternatives, contradiction tests, and validation—not longer narration.

## Output

Do not expose private reasoning or verbose phase-by-phase narration by default. Return:

- the improved result;
- completed loop count;
- material changes or conclusions;
- unresolved findings or checks that could not be performed.

Show detailed phase work only when the user asks for it or it is necessary to understand the result.