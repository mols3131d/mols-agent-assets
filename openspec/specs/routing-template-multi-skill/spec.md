# Routing Template Multi-Skill Spec

## Purpose
Define requirements for multi-skill execution within routing skill templates and across all master routing skills in the repository.

## Requirements

### Requirement: Routing Skill Template Multi-Skill Execution
The routing skill templates in `agent-asset-studio` MUST define the `## Sub-Skills` or `## Routing Sub Skills` sections to include:
- Multi-skill routing: If the request spans multiple categories, select and execute matching sub-skills sequentially.
- Workflow: Load instructions for all matched sub-skills → Plan a step-by-step sequence → Execute and report progress.

#### Scenario: Generating a new routing skill
- **WHEN** a developer generates a routing skill using the `agent-asset-studio` tools
- **THEN** the output routing skill's `SKILL.md` SHALL contain the multi-skill routing and workflow instructions.

### Requirement: Multi-Skill Selection across colonies and studios
All master/routing skills (`SKILL.md`) in `src/skills/` MUST support matching, loading, and executing multiple sub-skills sequentially when a user request spans multiple categories, instead of delegating to a single sub-skill.

#### Scenario: Running a multi-category task in Document Studio
- **WHEN** a user requests creating a PRD, then writing a SPEC, and then adding tasks to Kanban
- **THEN** the Document Studio master skill SHALL evaluate `INDEX.csv`, load all relevant sub-skills, plan a sequential workflow, and execute each step while reporting progress.
