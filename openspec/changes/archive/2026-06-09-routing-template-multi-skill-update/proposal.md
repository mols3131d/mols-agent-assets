## Why

Currently, newly generated routing skills do not include the multi-skill routing instructions and constraints by default. In addition, existing routing skills in the repository still instruct agents to pick and read exactly one sub-skill. We need to update both the templates and the existing routing skills to natively support multi-skill routing and sequential execution.

## What Changes

- Modify routing templates in `agent-asset-studio` scripts (`routerize_skills.py` and `templates/skill.py`) to output multi-skill routing guidelines.
- Modify existing routing skills in `src/skills` (`code-builder-colony`, `code-reviewer-colony`, `document-studio`, and `openspec-router--private`) to support multi-skill routing and sequential execution.

## Capabilities

### New Capabilities

- `routing-template-multi-skill`: Ensures that newly generated and existing routing skills support sequential multi-skill routing and execution.

### Modified Capabilities

- `multi-skill-routing`: Updates the existing capability to apply broadly to all routing skills in the project.

## Impact

- `src/skills/agent-asset-studio/scripts/routerize_skills.py`
- `src/skills/agent-asset-studio/scripts/templates/skill.py`
- `src/skills/code-builder-colony/SKILL.md`
- `src/skills/code-reviewer-colony/SKILL.md`
- `src/skills/document-studio/SKILL.md`
- `src/skills/openspec-router--private/SKILL.md`
