# Multi-Skill Routing Spec

## Purpose
Define requirements for multi-skill selection, sequence planning, and loading multiple sub-skills within routing skills (such as agent-asset-studio).

## Requirements

### Requirement: Multi-Skill Selection and Sequence Planning
The `agent-asset-studio` routing skill MUST identify and select all relevant sub-skills from `sub-skills/INDEX.csv` when a user's request involves multiple task categories. The skill SHALL instruct the agent to plan and outline a sequential flow of these sub-skills to resolve the request organically.

#### Scenario: User requests a new skill, naming check, and compression
- **WHEN** the user asks to create a new skill, ensure it follows naming conventions, and then compress it
- **THEN** the routing skill SHALL evaluate the triggers/keywords in `sub-skills/INDEX.csv`, select `agent-skill.md`, `asset-naming.md`, and `compress.md`, and present a sequential plan to execute them.

### Requirement: Multiple Sub-Skill Loading
The routing skill SHALL permit the agent to read and load the instructions/context of multiple matching sub-skills instead of restricting the context to a single sub-skill.

#### Scenario: Loading multiple matched sub-skills
- **WHEN** multiple sub-skills are identified as relevant to the user request
- **THEN** the routing skill SHALL instruct the agent to read the instructions of all matched sub-skills.
