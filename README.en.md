# mols-agent-assets

Repository for developing, validating, and managing AI agent assets.

## Asset Types

| Type | Purpose |
| --- | --- |
| Rule | Persistent policy and constraints |
| Skill | Reusable capability and conditional context |
| Prompt | Current invocation goal and one-off context |
| Agent | Distinct role, authority, tools, and delegation |

`docs/references/agent-asset-standard-baseline.md` owns the standards-adjacent baseline. `docs/references/agent-asset-boundaries.md` is the **Personal Agent Asset Standard** and owns this repository's intentional non-standard extensions and operating conventions.

## Source / Target Profiles

| Directory | Purpose |
| --- | --- |
| `src/agents/` | Subagent and custom agent sources |
| `src/skills/` | Workspace-capable Skill profile |
| `src/skills-chatbot/` | Self-contained single-file chatbot Skill profile under 4,000 tokens |
| `src/skills-chatbot-runtime/` | Chatbot Skill profile using bundled resources or hosted runtime capabilities |
| `src/rules/` | Rule sources |

The three Skill profiles are a **repository-local, non-standard taxonomy**. The same capability may exist in multiple target-specific variants when that preserves independent deployment and lets each harness use the most efficient representation it supports.

Inside directory-based Skill source packages, dot-prefixed directories (`.*`) are non-runtime maintainer surfaces. `.docs/baseline/` preserves durable purpose, requirements, invariants, major decisions, and recovery directives.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agents/` | Local agent runtime instructions |
| `src/` | Asset source workspace |
| `tests/` | Repository-level automated tests |
| `docs/` | Repository-level human-facing documentation and references |
| `scripts/` | Repository automation tools |
