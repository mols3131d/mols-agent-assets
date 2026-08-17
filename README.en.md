# mols-agent-assets

Repository for developing, validating, and managing AI agent assets.

## Asset Types

| Type | Purpose |
| --- | --- |
| Rule | Persistent policy and constraints |
| Skill | Reusable capability and conditional context |
| Prompt | Current invocation goal and one-off context |
| Agent | Distinct role, authority, tools, and delegation |

`docs/references/common/standards/agent-assets-standard-baseline.md` owns the standards-adjacent baseline. `docs/references/common/standards/agent-assets-standard-personal.md` owns this repository's intentional non-standard extensions and operating conventions.

## Source / Target Profiles

| Directory | Purpose |
| --- | --- |
| `src/agents/` | Subagent and custom agent sources |
| `src/skills/` | Workspace-capable Skill profile |
| `src/skills-chatbot/` | Self-contained single-file chatbot Skill profile under 4,000 tokens |
| `src/skills-chatbot-runtime/` | Chatbot Skill profile using bundled resources or hosted runtime capabilities |
| `src/rules/` | Rule sources |

`docs/references/skills/agent-assets-skills-target-profiles.md` owns the Skill profile details. `docs/references/rules/agent-assets-rules-projections.md` owns Rule projections and chatbot fallback behavior.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agents/` | Local agent runtime instructions |
| `src/` | Asset source workspace |
| `tests/` | Repository-level automated tests |
| `docs/` | Repository-level human-facing documentation and references |
| `scripts/` | Repository automation tools |
