# mols-agent-assets

Repository for developing, validating, and managing AI agent assets.

Agent Assets representable through AgentsMesh use `src/agentsmesh/` as their canonical source. This path is intentionally not named `.agentsmesh/`: distribution assets stored by this library must not be auto-discovered as repository-local runtime configuration.

## Asset Types

| Type | Purpose |
| --- | --- |
| Rule | Persistent policy and constraints |
| Skill | Reusable capability and conditional context |
| Prompt | Current invocation goal and one-off context |
| Agent | Distinct role, authority, tools, and delegation |

`docs/references/common/standards/agent-assets-standard-baseline.md` owns the standards-adjacent baseline. `docs/references/common/standards/agent-assets-standard-personal.md` owns this repository's intentional non-standard extensions and operating conventions.

## Source Boundary

| Directory | Role |
| --- | --- |
| `src/agentsmesh/` | Canonical AgentsMesh-compatible Rules, Skills, Agents, and projection config |
| Other paths under `src/` | Explicit custom/non-standard Agent Asset sources when a real target requires them |
| `.agents/AGENTS.md` | Repository-local guard for this repository itself |
| `tests/` | Repository-level deterministic tests |
| `evals/` | Behavioral/model evals and cross-asset regression contracts |
| `docs/` | Human-facing documentation and references |
| `scripts/` | Repository automation, validation, and synchronization tooling |

Do not use repository-root `.agentsmesh/`, `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/rules/`, or `.agents/skills/` as distribution surfaces. When native AgentsMesh validation or projection is needed, stage `src/agentsmesh/` into a temporary workspace and keep generated runtime surfaces outside this repository.

Skill specifications use the `agentskills.io` open standard as Tier 1. `docs/references/skills/agent-skills-io/agent-skills-io-specification.md` links official Tier 2 vendor/harness contracts without copying them. `docs/references/skills/agent-assets-skills-standard-personal.md` owns repository-local Skill extensions, while `docs/references/skills/agent-assets-skills-target-profiles.md` owns package shape and target boundaries.

## Basic Workflow

```text
edit src/agentsmesh
  → rumdl fmt when Markdown is affected
  → stage a temporary AgentsMesh workspace when native validation is needed
  → repository tests / applicable evals
  → review canonical source only
```

The boundary is deliberate: this repository develops Agent Assets; it must not implicitly consume every asset it stores.
