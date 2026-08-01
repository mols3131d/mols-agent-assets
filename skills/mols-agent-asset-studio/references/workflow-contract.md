# Workflow Contract

## Inputs

Resolve or infer:

- target assets and target runtime
- requested mode and acceptance criteria
- source write boundary
- project conventions and authoritative instructions
- evidence location, if durable reports are requested
- execution permissions for scripts, hooks, network, and external systems

Ask only when an unresolved choice materially changes write authority, safety, or
the user-visible contract. Otherwise select the narrowest safe assumption and
record it.

## Mode Authority

| Mode | Source writes | Required gates |
| --- | ---: | --- |
| `inspect` | No | inventory, analysis |
| `create` | Approved new targets | author, general review, classify, evaluate, validate |
| `improve` | Approved existing targets | baseline, author, general review, classify, evaluate, validate |
| `refactor` | Approved existing targets | baseline, invariants, author, general review, regression evidence, validate |
| `replace` | Approved replacement boundary | rollback, baseline intent, architecture, author, both reviews, evaluate, validate |
| `consolidate` | Approved source and destination assets | rollback, overlap evidence, authority comparison, migration plan, author, both reviews, route evaluation, validate |
| `review` | No source writes | general review; adversarial review when applicable |
| `validate` | No source writes | deterministic checks |
| `evaluate` | Evidence writes only | test design, execution, grading, analysis |
| `package` | Package output only | accepted-source check, manifest, reproducibility, archive verification |

## Lifecycle

1. **Scope**
   - Select mode, target set, artifact type, runtime, acceptance criteria, and
     write boundary.
   - Identify destructive, external, credentialed, or publication actions.
1. **Recovery readiness**
   - For rename, replace, consolidation, broad refactor, or destructive work,
     establish a rollback point before mutation. Use Git when available; otherwise
     create a bounded snapshot with a cleanup policy.
1. **Baseline**
   - For existing assets, capture current purpose, triggers, outputs, dependencies,
     safety constraints, runtime-specific metadata, and known checks.
   - Do not mistake current text for desired behavior; user and project policy win.
1. **Research**
   - Inspect already-known project files first.
   - Research external facts only when freshness or an unresolved technical claim
     can change architecture or acceptance.
   - Prefer official specifications and vendor documentation.
1. **Architecture**
   - Choose the minimum asset set using `artifact-types.md`.
   - Reuse or extend existing assets before creating competing assets. For
     overlapping assets, apply `consolidation.md` and choose Merge, Compose,
     Route, Keep separate, or Deprecate.
   - Define context-loading boundaries and deterministic resources.
1. **Author**
   - For behavior-preserving work, capture literal and ordered invariants before
     editing and verify them after the mutation.
   - Apply one coherent mutation batch inside the approved boundary.
   - Keep reusable detail in references, deterministic operations in scripts, and
     output materials in assets or templates.
1. **General Review**
   - Review the complete candidate in fresh context using `review-rubric.md`.
   - Provide purpose, requirements, source files, and canonical criteria—not the
     author's persuasion or private reasoning.
1. **Correction**
   - Apply all accepted findings in one batch.
   - Run targeted closure against finding IDs; repeat full review only if
     architecture, authority, safety, or acceptance changed.
1. **Adversarial Review**
   - Required for Major changes, imported content, executable resources,
     security-bearing assets, replacement, consolidation, publication, or explicit
     strict mode.
   - Use `adversarial-review.md`; assume malformed input and misuse.
1. **Behavior Evaluation**
   - For behavior-bearing Major changes, run with-skill and baseline or prior-skill
     cases where the runtime permits.
    - Consolidation includes clear positive, near-miss, collision, multi-workflow,
      and ambiguous route cases.
    - Minor and Medium changes may be satisfied-and-skipped with a specific
      non-behavior reason.
1. **Validation**
   - Run final-state runtime schema, structural hygiene, link, script, declared
     host, invariant, and package checks.
    - Execute project-owned commands only from validated argv-based plans with
      explicit execution authority. Record each command and actual result.
1. **Resolve**
   - Return one overall outcome using the resolver below.
1. **Package**
   - Package only accepted source. Generate a manifest and verify archive
     integrity. Do not include caches, secrets, temporary workspaces, or backups.
    - Normalize ZIP metadata and ordering so identical accepted source produces
      byte-identical archives.

## Change Classification

Use the highest class that applies.

| Class | Rule | Behavior gate |
| --- | --- | --- |
| Minor | Formatting, comments, link repair, metadata alignment with no trigger or action change | Satisfied-and-skipped |
| Medium | Clarifies or reorganizes existing behavior without changing model actions, outputs, authority, or safety | Satisfied-and-skipped with regression evidence |
| Major | Adds, removes, or materially changes triggers, actions, outputs, tools, hooks, authority, routing, stage gates, safety, or runtime behavior | Execute behavior evaluation |

## Reviews

- General review is required for every mutating mode.
- Adversarial review is required by step 9 conditions.
- A reviewer owns findings only; the author owns source corrections.
- Findings use `Critical`, `High`, `Medium`, or `Low` severity and include evidence,
  impact, and acceptance evidence.
- `Pass` requires no open Critical, High, or acceptance-blocking Medium finding.

## Outcome Resolver

Apply the first matching outcome:

| Outcome | Condition |
| --- | --- |
| `Blocked` | Target, authority, safety, or decision-critical scope is too ambiguous |
| `Deferred` | A required capability, permission, runtime, or check cannot run now and has a concrete rerun condition |
| `Revise` | An actionable review finding, failed check, unmet criterion, or partial authoring remains |
| `Pass` | All required gates completed or were legitimately skipped, checks passed, and acceptance criteria are met |

## Iteration Rules

- Iterate on evidence-backed findings, not a ceremonial cycle count.
- Correct coherent finding sets together, then run targeted closure.
- Do not repeat the same failed approach without new evidence.
- Stop `Deferred` when the environment prevents a required gate.
- Stop `Blocked` before unapproved destructive, credentialed, external, or
  out-of-bound actions.
