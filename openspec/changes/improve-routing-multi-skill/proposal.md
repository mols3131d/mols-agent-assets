## Why

Currently, the `agent-asset-studio` routing skill constraints or instructions guide agents to route the request to a single sub-skill (or they default to choosing only one sub-skill). However, complex user requests often require the organic cooperation of multiple sub-skills (e.g., creating/improving a skill and naming/compressing it). Limiting agents to a single sub-skill prevents them from fully executing multi-step tasks in the asset studio.

## What Changes

- Update `src/skills/agent-asset-studio/SKILL.md` to explicitly instruct and allow agents to select, load, and execute multiple sub-skills sequentially or organically when the user's request spans multiple domains.
- Clarify routing instructions in `src/skills/agent-asset-studio/SKILL.md` so that the agent reads `sub-skills/INDEX.csv` and can select more than one sub-skill to load and execute.
- Ensure the agent evaluates all relevant sub-skills and outlines a step-by-step plan if multiple sub-skills are required.

## Capabilities

### New Capabilities

- `multi-skill-routing`: Allows the agent-asset-studio skill to identify, coordinate, and execute multiple sub-skills for a single, complex task.

### Modified Capabilities

<!-- None since openspec/specs is currently empty -->

## Impact

- `src/skills/agent-asset-studio/SKILL.md`: Routing instructions and constraints will be updated.
- Agent routing behavior when using `agent-asset-studio` skill.
