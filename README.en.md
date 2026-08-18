# mols-agent-assets

Repository for developing, validating, and managing AI agent assets.

Portable coding-agent assets use **AgentsMesh directly** for multi-harness distribution. This repository owns Agent Asset semantics, quality contracts, tests, and evals; AgentsMesh owns canonical coding-agent configuration and target projection.

## Asset Types

| Type | Purpose |
| --- | --- |
| Rule | Persistent policy and constraints |
| Skill | Reusable capability and conditional context |
| Prompt | Current invocation goal and one-off context |
| Agent | Distinct role, authority, tools, and delegation |

`docs/references/common/standards/agent-assets-standard-baseline.md` owns the standards-adjacent baseline. `docs/references/common/standards/agent-assets-standard-personal.md` owns this repository's intentional non-standard extensions and operating conventions.

## Source / Target Profiles

| Directory | Authority |
| --- | --- |
| `.agentsmesh/rules/` | Canonical portable coding-agent Rules |
| `.agentsmesh/skills/` | Canonical portable coding-agent Skills |
| `src/agents/` | Target-specific Agents not safely representable by the current Tier A AgentsMesh contract |
| `src/skills-chatbot/` | Self-contained hosted-chatbot Skill profile |
| `src/skills-chatbot-runtime/` | Bundled/runtime hosted-chatbot Skill profile |
| `src/prompts/` | Explicit Prompt sources |
| `src/rules/` | Hosted-chatbot-specific Rules outside AgentsMesh only |

`agentsmesh.yaml` selects active coding-agent targets and features. Generated Copilot and Antigravity files are derived distribution artifacts and must not be hand-edited.

Skill specifications use the `agentskills.io` open standard as Tier 1. `docs/references/skills/agent-skills-io/agent-skills-io-specification.md` links official Tier 2 vendor/harness contracts without copying them. `docs/references/skills/agent-assets-skills-standard-personal.md` owns repository-local Skill extensions and `docs/references/skills/agent-assets-skills-target-profiles.md` owns target-profile details.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agentsmesh/` | Portable coding-agent canonical assets and AgentsMesh lock |
| `.github/skills/`, `.github/copilot-instructions.md` | Generated GitHub Copilot projection |
| `.agents/rules/`, `.agents/skills/` | Generated Antigravity projection |
| `src/` | Target-specific/hosted profiles outside AgentsMesh plus tooling |
| `tests/` | Repository-level automated tests |
| `evals/` | Cross-asset evaluation contracts when present |
| `docs/` | Human-facing documentation and references |
| `scripts/` | Repository automation tools |

## Basic Workflow

```text
edit .agentsmesh/
  → agentsmesh lint
  → agentsmesh generate
  → agentsmesh check / generate --check
  → repository tests / applicable evals
```

Do not force profiles that AgentsMesh cannot faithfully represent into its canonical model. Keep explicit separate authority where target semantics differ.
