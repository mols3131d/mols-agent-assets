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
The downstream task capability owns the subject matter and the actual guidance.

## Contract

- Resolve the person's intended outcome and the next useful result, not an abstract or persistent learner profile.
- Reuse established conversation and workspace context before asking for or loading more.
- Infer current understanding, current attempt, decision point, and relevant constraints from observable evidence when possible.
- Separate observed facts from assumptions and retain uncertainty that can change the guidance.
- Resolve whether the interaction is primarily direct guidance, coaching and feedback, or a useful mix.
- Compose applicable domain-specific context owners when subject-matter truth depends on a repository, code, workspace, external source, or another specialized surface.
- Load progressively and stop when additional context is unlikely to change the next useful guidance decision.

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

Do not force every dimension into an explicit question or artifact. Missing context matters only when it has a credible path to changing the next guidance decision.

## Context Priority

For direct guidance, prioritize context about the destination, current mental model, prerequisites, orientation, and relevant path forward.

For coaching, prioritize context about the person's current reasoning or attempt, the immediate decision or blocker, prior feedback, and the next observable feedback point.

These are loading priorities, not output templates or mandatory teaching methods. Re-evaluate them when the user's intent materially changes.

## Handoff

Before downstream guidance begins, confirm that:

- the intended outcome is clear enough to guide against;
- the current state is understood well enough to avoid generic or mismatched support;
- material claims have an appropriate evidence source or retained uncertainty;
- applicable domain context has been loaded by its owner when needed;
- further loading has no credible material gain for the next guidance decision.

Then stop loading context and hand off to the task capability.

## Boundary

This Skill owns **guidance and coaching context selection**, not the subject matter, factual research, repository discovery, implementation, review methodology, pedagogy, or answer format.

It does not require Socratic questioning, a fixed teaching method, a fixed sequence of questions, or a learner taxonomy. It must not invent expertise, goals, preferences, or progress signals that are not supported by the interaction or available evidence.
