# mols-agent-assets

Repository for developing, validating, and managing AI agent assets.

Agent Assets representable through AgentsMesh live in an **isolated native workspace** at `src/agentsmesh/`. Its configuration is `src/agentsmesh/agentsmesh.yaml`; canonical Rules, Skills, and Agents live under `src/agentsmesh/.agentsmesh/`. The repository root is not an AgentsMesh runtime workspace.

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
| `src/agentsmesh/` | Isolated native AgentsMesh workspace and projection config |
| `src/agentsmesh/.agentsmesh/` | Canonical AgentsMesh-compatible Rules, Skills, and Agents |
| Other paths under `src/` | Explicit custom/non-standard Agent Asset sources when a real target requires them |
| `.agents/AGENTS.md` | Repository-local guard for this repository itself |
| `tests/` | Repository-level deterministic tests |
| `evals/` | Behavioral/model evals and cross-asset regression contracts |
| `docs/` | Human-facing documentation and references |
| `scripts/` | Repository automation, validation, and synchronization tooling |

Do not use repository-root `.agentsmesh/`, `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/rules/`, or `.agents/skills/` as distribution surfaces. Run native read-only checks directly from `src/agentsmesh/`; copy the whole workspace to a temporary directory only for write-producing generation validation.

Skill specifications use the `agentskills.io` open standard as Tier 1. `docs/references/skills/agent-skills-io/agent-skills-io-specification.md` links official Tier 2 vendor/harness contracts without copying them. `docs/references/skills/agent-assets-skills-standard-personal.md` owns repository-local Skill extensions, while `docs/references/skills/agent-assets-skills-target-profiles.md` owns package shape and target boundaries.

## Basic Workflow

```text
edit src/agentsmesh/.agentsmesh
  → rumdl fmt when Markdown is affected
  → native lint / preview from src/agentsmesh
  → temporary workspace copy only for write-producing validation
  → repository tests / applicable evals
  → review canonical source only
```

The boundary is deliberate: preserve the native AgentsMesh layout while keeping distribution assets separate from repository-root runtime discovery.
