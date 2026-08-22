---
name: load-context-guidance
description: >-
  Load baseline context for guidance, coaching, mentoring, onboarding, teaching, or
  walkthrough tasks where the goal is to help a person understand, decide, practice, or
  make progress. Use when support should adapt to the person's goal, current understanding
  or attempt, constraints, evidence, and next useful feedback point. Do not use for ordinary
  factual answers, pure content transformation, or tasks where the assistant should simply
  execute the work without a guidance relationship.
---

# Load Guidance Context

Load only the context that can materially change how a person should be guided or coached.
The downstream task capability owns the subject matter and the actual work.

## Contract

- Resolve the person's intended outcome and the next useful result, not an abstract learner profile.
- Reuse established conversation and workspace context before asking for or loading more.
- Infer current understanding, current attempt, and relevant constraints from observable evidence when possible.
- Separate observed facts from assumptions and expose uncertainty that can change the guidance.
- Infer whether the person wants direct orientation, coaching and feedback, or a mix from the request and interaction.
- Match depth to demonstrated understanding, task stakes, and the current decision rather than a fixed beginner or expert label.
- Preserve agency: do not withhold a useful answer merely to force discovery, and do not take over work when the person wants to reason, practice, or decide.
- Load progressively. Start with the smallest context sufficient for the next useful intervention and deepen only when more context can change it.
- Compose applicable domain-specific context owners when subject-matter truth depends on a repository, code, workspace, external source, or another specialized surface.

## Context Surface

Resolve only the dimensions that affect the current guidance:

| Context | What to establish |
| --- | --- |
| Goal | What the person wants to understand, decide, practice, or accomplish |
| Current state | Existing mental model, current attempt, decision point, or blocker |
| Constraints | Time, scope, tools, required fidelity, risk, or other relevant limits |
| Evidence | Sources or observations that the guidance may rely on |
| Interaction intent | Direct guide, coaching/feedback, or a useful mix |
| Feedback point | The next answer, action, check, or observation that can show progress |

Do not force every dimension into an explicit question or artifact. Stop loading when the missing context is unlikely to change the next useful guidance.

## Guidance Focus

When direct guidance dominates, prioritize the destination, mental model, prerequisites, orientation, and the shortest useful path forward.

When coaching dominates, prioritize the person's current reasoning or attempt, the decision or blocker in front of them, and the smallest feedback or prompt that can advance their own work.

These are context priorities, not fixed output templates or mandatory teaching methods. Shift between them when the user's intent changes.

## Handoff

Before downstream guidance begins, confirm that:

- the intended outcome is clear enough to act on;
- the current state is understood well enough to avoid generic or mismatched guidance;
- material claims can be traced to appropriate evidence or are marked uncertain;
- applicable domain context has been loaded by its owner when needed;
- no additional context has a credible path to changing the next useful intervention.

Then stop loading context and hand off to the task capability.

## Boundary

This Skill owns **guidance and coaching context selection**, not the subject matter, factual research, repository discovery, implementation, review methodology, or answer format.

It does not require Socratic questioning, a fixed pedagogy, a fixed sequence of questions, or a learner taxonomy. It must not invent expertise, goals, preferences, or progress signals that are not supported by the interaction or available evidence.
