---
name: load-context-guidance
description: >-
  Load adaptive context for guidance, coaching, mentoring, onboarding, teaching, or
  walkthrough tasks when useful support depends on the person's goal, current state,
  prior attempts, constraints, grounding, progress, or desired interaction. Use when the
  assistant should adapt to the person's state rather than merely answer or execute. Do
  not use just because an answer explains something or recommends a choice, or for pure
  content transformation and direct task execution without a guidance relationship.
---

# Load Guidance Context

Load only the context that can materially change downstream guidance or coaching.
The downstream task capability owns the subject matter and the actual guidance.

## Contract

- Resolve the person's intended outcome and what would count as useful success for the current interaction.
- Reuse established conversation and workspace context before asking for or loading more.
- Establish current state from observable evidence: relevant prior knowledge, prior or current attempts, misconceptions or uncertainty, decision point, and blocker when they matter.
- Treat current state and progress as task-local, provisional, and revisable. Prefer recent evidence, update them when stronger evidence conflicts, and do not carry stale labels across unrelated tasks or domains by default.
- Treat explicit correction, reset, reframing, or changed intent from the person as stronger than inferred context. Drop or narrow conflicting inferred state instead of preserving it for continuity.
- Keep constraints and stakes visible when they can change the appropriate depth, pace, scope, or feasibility. Include relevant support, resources, stakeholders, or external pressure only when they materially affect the guidance.
- Treat provided materials, prior outputs, and identified sources as grounding; delegate retrieval or factual validation to the context owner that actually owns that surface.
- Respect explicit interaction preferences such as directness, pace, depth, language, format, desired ownership, roles, or boundaries when they affect guidance. Do not infer a fixed learning style, personality type, or ability label from sparse evidence.
- For decision or choice guidance, retain the person's stated values, priorities, trade-offs, and preferred role in the decision when they materially affect what useful support means.
- Reuse relevant progress evidence, including prior feedback, outcomes, assistance already tried, and its observed effect, instead of restarting from a generic baseline or assuming the same amount of help remains appropriate.
- Compose applicable domain-specific context owners when subject-matter truth depends on a repository, code, workspace, external source, or another specialized surface.
- Load progressively and stop when additional context is unlikely to change the next guidance decision. Do not build a broad personal profile merely because more context is available.
- Do not seek personal, identity, cultural, or other background context merely for personalization; use it only when the person has made it relevant to the current guidance or it is otherwise necessary to honor an explicit constraint.

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

Do not force every dimension into an explicit question or artifact. Missing context matters only when it has a credible path to changing the next guidance decision.

## Context Priority

For direct guidance, prioritize context about the destination, current mental model, prerequisites, constraints, grounding, and the relevant path boundary.

For coaching, prioritize context about the person's current reasoning or attempt, the immediate decision or blocker, prior feedback or progress, desired ownership, agreed roles or boundaries, and the agreed outcome.

For decision guidance, prioritize relevant values or trade-offs, uncertainty, desired decision role, material constraints, and grounding. Subject-matter facts and option evaluation remain owned by the applicable domain capability.

These are loading priorities, not output templates or mandatory teaching methods. Re-evaluate them when the user's goal, state, evidence, or interaction intent materially changes.

## Handoff

Before downstream guidance begins, confirm only what is needed to avoid a materially generic or mismatched response:

- the intended outcome and useful success condition are clear enough;
- the current state is understood well enough for the requested level of adaptation and is not being treated as a fixed profile;
- explicit corrections, resets, roles, boundaries, values, constraints, and interaction preferences are retained when they matter;
- grounding is available or delegated to its actual owner;
- relevant progress and prior-assistance evidence are reused when the interaction is ongoing;
- material uncertainty is retained rather than filled with invented profile assumptions;
- further loading has no credible material gain for the next guidance decision.

Then stop loading context and hand off to the task capability.

## Boundary

This Skill owns **guidance and coaching context selection**, not the subject matter, factual research, repository discovery, implementation, review methodology, pedagogy, intervention planning, progress evaluation, or answer format.

It does not require Socratic questioning, a fixed teaching method, a fixed sequence of questions, a learner taxonomy, or a persistent learner profile. It must not infer fixed learning styles, personality types, expertise, goals, preferences, misconceptions, motivation, or progress signals without sufficient evidence from the interaction or an authorized context source. Keep inferred state narrow, task-relevant, user-correctable, and revisable rather than turning it into a durable user model by default.
