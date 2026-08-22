---
name: load-context-guidance
description: >-
  Load adaptive context for guidance, coaching, mentoring, onboarding, teaching, or
  walkthrough tasks when how the assistant should support the person materially depends
  on their goal, current state, constraints, grounding, interaction preferences, or
  progress. Do not use for ordinary explanation, recommendation, content transformation,
  or direct task execution when the task can be completed without adapting how the person
  is supported.
---

# Load Guidance Context

Load only the context that can materially change downstream guidance or coaching.
The downstream task capability owns the subject matter and the actual guidance.

## Contract

- Reuse established conversation and workspace context before asking for or loading more.
- Treat inferred current state and progress as task-local, provisional, and revisable. Explicit correction, reset, reframing, or changed intent outranks inference; prefer newer stronger evidence when context conflicts.
- Keep context narrow and task-relevant. Do not build a broad persistent profile or infer fixed learning styles, personality types, ability labels, or other unsupported user attributes.
- Treat provided materials, prior outputs, observations, and identified sources as grounding; delegate retrieval or factual validation to the context owner that owns that surface.
- Compose applicable domain-specific context owners when subject-matter truth depends on a repository, code, workspace, external source, or another specialized surface.
- Load progressively and stop when additional context has no credible path to changing the next guidance decision.

## Context Surface

Resolve only the dimensions that affect the current guidance:

| Context | What to establish |
| --- | --- |
| Goal and success | What the person wants to understand, decide, practice, or accomplish; what would count as useful success now; relevant values, priorities, or trade-offs when the task is a decision |
| Current state | Relevant mental model, prior knowledge, attempts, uncertainty or misconception, decision point, or blocker |
| Constraints | Time, deadline, scope, tools, required fidelity, stakes, support/resources, external pressure, or other relevant limits |
| Grounding | Materials, prior outputs, observations, or identified sources downstream guidance should take into account |
| Interaction | Direct guidance, coaching/feedback, or a useful mix; desired ownership or initiative; explicit roles, boundaries, pace, depth, language, or format preferences when relevant |
| Progress | Relevant prior feedback, outcomes, changes, unresolved gaps, assistance already tried, and observed effects that show movement from an earlier state |

Do not force every dimension into an explicit question or artifact. Missing context matters only when it can materially change the next guidance decision.

## Handoff

Hand off once the smallest relevant subset of the context surface is sufficient to avoid materially generic or mismatched guidance, required domain context is available or delegated to its owner, and material uncertainty remains explicit. Do not delay downstream guidance merely to complete the context surface.

## Boundary

This Skill owns **guidance and coaching context selection**, not the subject matter, factual research, repository discovery, implementation, review methodology, pedagogy, intervention planning, option evaluation, progress evaluation, or answer format.

It does not define a teaching method, coaching method, learner taxonomy, or persistent user model.
