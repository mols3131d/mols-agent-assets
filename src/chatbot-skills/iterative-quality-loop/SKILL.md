---
name: iterative-quality-loop
description: >-
  Improve a difficult task through repeated Research → Plan → Implement → Review
  loops with distinct workflows and explicit validation. Use when the user asks
  for higher-quality reasoning, deep research or review, multiple review passes,
  iterative improvement, adversarial checks, or repeated loops rather than a
  single-pass answer.
metadata:
  - target:
      - "OpenAI ChatGPT"
---

# Iterative Quality Loop

Improve the current task through complete Research → Plan → Implement → Review
loops. Each workflow must perform a distinct cognitive function. Repeating the
same analysis does not count as another workflow or loop.

## Defaults

```yaml
max_loops: 10
stop_condition: review_has_no_actionable_findings
```

- If the user specifies a loop count, perform exactly that many loops unless blocked.
- If the user specifies a different maximum or stop condition, use it.
- Otherwise stop when Review returns no actionable findings or `max_loops` is reached.
- If the maximum is reached with findings remaining, report the unresolved findings.

## Loop

Each loop contains four phases.

### 1. Research

Build or refresh the evidence needed for the current loop.

1. **Discover** — inspect the problem, context, relevant sources, and missing information.
1. **Investigate** — examine the highest-impact questions in depth.
1. **Challenge** — search for contradictions, counterexamples, weak assumptions, and missed perspectives.
1. **Synthesize** — combine the evidence into conclusions that can drive planning.

On later loops, start from unresolved Review findings and new evidence instead of repeating broad research without cause.

### 2. Plan

Convert Research into a bounded execution plan.

1. **Frame** — define the current objective, scope, constraints, and acceptance conditions.
1. **Design** — choose the approach and important trade-offs.
1. **Decompose** — turn the approach into concrete work units and validation points.
1. **Verify Plan** — check for missing requirements, unsupported assumptions, unnecessary work, and weak validation.

Prefer the smallest plan that can resolve the current findings.

### 3. Implement

Perform the actual task. Implementation may be code, writing, analysis, design, editing, or another requested output.

1. **Execute** — perform the planned core work.
1. **Integrate** — reconcile the work with existing context, artifacts, constraints, and prior results.
1. **Refine** — improve correctness, clarity, KISS, DRY, and fitness for the requested use.
1. **Validate** — test or inspect the result against the plan, evidence, and acceptance conditions.

Do not claim a validation was performed when the required tool, source, or execution was unavailable.

### 4. Review

Independently search for remaining material problems.

1. **Quality Review** — check correctness, completeness, consistency, and usability.
1. **Adversarial Review** — attack assumptions, edge cases, failure modes, and alternative interpretations.
1. **Evidence Review** — verify that claims, conclusions, and changes are supported by available evidence.
1. **Decision Review** — deduplicate findings, determine which are actionable, and decide whether another loop is required.

## Finding Contract

A Review finding must be:

- specific enough to act on;
- material to the requested outcome;
- supported by evidence or a clearly identified reasoning gap; and
- not merely a repetition of an already resolved finding.

Do not invent findings to keep the loop running. Cosmetic preferences and unsupported possibilities are not actionable findings unless the task explicitly makes them relevant.

## Loop Contract

A loop counts only when all applicable phases are completed and the Review uses genuinely distinct checks.

The following do not count as additional loops:

- rereading without a new question or lens;
- restating the same findings;
- rewriting the same review in different words;
- repeating the same search or analysis without new evidence;
- claiming validation without performing it.

Review findings become the primary inputs to the next loop. Preserve confirmed conclusions and avoid reopening them without new evidence.

## Reasoning and Validation

Increase reasoning effort by testing alternatives, contradictions, assumptions, and evidence rather than by producing longer explanations. Keep private reasoning private; report conclusions, evidence, decisions, and validation results needed to understand the outcome.

Choose validation appropriate to the task, such as:

- source cross-checking for research;
- implementation and test inspection for code;
- source-to-output comparison for rewriting or documentation;
- requirement and constraint checks for design;
- counterexample search for analytical claims.

## Output

Keep loop reporting compact. For each completed loop, expose only what helps the user evaluate progress:

```markdown
## Loop <n>

### Research
<new evidence or changed understanding>

### Plan
<material plan decisions>

### Implement
<what changed>

### Review
- <actionable finding or `No actionable findings`>
```

After the final loop, provide the improved result and note any unresolved findings or validation that could not be performed.
