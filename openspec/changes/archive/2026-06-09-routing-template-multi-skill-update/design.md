## Context

Newly generated routing skills and existing routing skills in `src/skills` do not have multi-skill execution enabled by default; they still direct agents to pick and read exactly one sub-skill. We need to standardize all routing skills and generators to use the multi-skill workflow.

## Goals / Non-Goals

**Goals:**
- Update `agent-asset-studio` routing skill templates to output the multi-skill routing instructions.
- Update all existing routing skills in `src/skills` (`code-builder-colony`, `code-reviewer-colony`, `document-studio`, `openspec-router--private`) to support matching and executing multiple sub-skills sequentially.

**Non-Goals:**
- Changing the actual execution logic of sub-skills.

## Decisions

### 1. Update routing skill templates
We will modify the templates in `src/skills/agent-asset-studio/scripts/routerize_skills.py` and `src/skills/agent-asset-studio/scripts/templates/skill.py` to contain:
- Multi-skill routing: If the request spans multiple categories, select and execute matching sub-skills sequentially.
- Workflow: Load instructions for all matched sub-skills → Plan a step-by-step sequence → Execute and report progress.

### 2. Update existing routing skills
We will modify:
- `src/skills/code-builder-colony/SKILL.md`
- `src/skills/code-reviewer-colony/SKILL.md`
- `src/skills/document-studio/SKILL.md`
- `src/skills/openspec-router--private/SKILL.md`
Each file will have its routing/constraints sections updated to allow multi-skill selection and sequential execution.

## Risks / Trade-offs

- **[Risk]** Slightly increases context size for other routing skills if they read multiple sub-skills.
- **[Mitigation]** The sub-skills of these colonies are modular and small, so the context increase is negligible compared to the benefit of single-run complete task execution.
