## Context

The `agent-asset-studio` routing skill currently directs agents to route requests to a single sub-skill (or agents default to this behavior). However, complex user requests often require organic cooperation of multiple sub-skills (e.g., creating/improving a skill, naming it, and compressing it). Restricting routing to exactly one sub-skill prevents the agent from executing multi-step tasks.

## Goals / Non-Goals

**Goals:**
- Enable the agent to identify and select multiple sub-skills when a request covers multiple categories in `sub-skills/INDEX.csv`.
- Direct the agent to formulate a sequential plan when multiple sub-skills are needed.
- Instruct the agent to load and read the instructions for all matching sub-skills.

**Non-Goals:**
- Modifying the actual logic of the sub-skills themselves (e.g., `agent-skill.md`, `compress.md`, `asset-naming.md`, `routerize-skills.md`).
- Altering the routing logic of other routing skills (e.g., `openspec-router`).

## Decisions

### Update `src/skills/agent-asset-studio/SKILL.md` instructions
We will revise the instructions under `## Sub Skills` and `## Constraints` in `src/skills/agent-asset-studio/SKILL.md` to:
1. Explicitly guide the agent to match one or more sub-skills from `sub-skills/INDEX.csv`.
2. Explicitly outline a multi-step sequence plan if multiple sub-skills are matched.
3. Explicitly allow loading/reading instructions for all matched sub-skills.

*Alternative Considered*: Keep the routing skill to single-route and require the user to explicitly prompt for each step individually.
*Rationale*: This degrades the agentic capability and user experience, as the user expects a single rich request to be handled completely.

## Risks / Trade-offs

- **[Risk]** Context size increases if multiple sub-skills are read simultaneously.
- **[Mitigation]** The sub-skills in `agent-asset-studio` are relatively small and focused, so loading 2-3 of them will not exceed context limits.
