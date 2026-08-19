# mols-agent-assets

Repository for developing, validating, and managing AI agent assets.

Use `.agentsmesh/` as the canonical source for Agent Assets that AgentsMesh can faithfully represent. This repository owns asset semantics, quality contracts, tests, and evals; AgentsMesh owns canonical representation and active target projection.

## Asset Types

| Type | Purpose |
| --- | --- |
| Rule | Persistent policy and constraints |
| Skill | Reusable capability and conditional context |
| Prompt | Current invocation goal and one-off context |
| Agent | Distinct role, authority, tools, and delegation |

`docs/references/common/standards/agent-assets-standard-baseline.md` owns the standards-adjacent baseline. `docs/references/common/standards/agent-assets-standard-personal.md` owns this repository's intentional non-standard extensions and operating conventions.

## Source and Generated Surfaces

| Directory | Role |
| --- | --- |
| `.agentsmesh/` | Canonical source for Rules, Skills, and Agents representable by the current AgentsMesh contract |
| `src/` | Repository-local custom or non-standard exception surface intentionally outside AgentsMesh |
| AgentsMesh-managed paths under `.github/` and `.agents/` | Generated projections for active targets |

There is currently no required custom Agent Asset under `src/`. Do not create a parallel source there for assets AgentsMesh can represent.

`agentsmesh.yaml` selects active coding-agent targets and features. Current Copilot and Antigravity projections are derived from `.agentsmesh/` and must not be hand-edited.

Skill specifications use the `agentskills.io` open standard as Tier 1. `docs/references/skills/agent-skills-io/agent-skills-io-specification.md` links official Tier 2 vendor/harness contracts without copying them. `docs/references/skills/agent-assets-skills-standard-personal.md` owns repository-local Skill extensions, while `docs/references/skills/agent-assets-skills-target-profiles.md` owns package shape and target boundaries.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agentsmesh/` | Canonical Agent Assets and AgentsMesh lock |
| `.github/copilot-instructions.md`, `.github/skills/`, `.github/agents/` | Generated GitHub Copilot projection |
| `.agents/rules/`, `.agents/skills/` | Generated Antigravity projection |
| `src/` | Intentional custom/non-standard Agent Asset exception surface |
| `tests/` | Repository-level deterministic tests |
| `evals/` | Behavioral/model evals and cross-asset regression contracts |
| `docs/` | Human-facing documentation and references |
| `scripts/` | Repository automation, synchronization, and development tooling |

## Basic Workflow

```text
edit canonical source
  → rumdl fmt when Markdown is affected
  → agentsmesh lint / generate when applicable
  → agentsmesh check / generate --check when applicable
  → repository tests / applicable evals
```

Keep assets AgentsMesh cannot represent as explicit `src/` exceptions only when a real requirement exists. Do not pre-create future taxonomy or empty structure for hypothetical exceptions.
