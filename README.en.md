# mols-agent-assets

Repository for developing, validating, and managing AI agent assets.

Use **AgentsMesh directly** as the canonical source whenever its current contract can faithfully represent an Agent Asset. This repository owns Agent Asset semantics, quality contracts, tests, and evals; AgentsMesh owns canonical representation and target projection.

## Asset Types

| Type | Purpose |
| --- | --- |
| Rule | Persistent policy and constraints |
| Skill | Reusable capability and conditional context |
| Prompt | Current invocation goal and one-off context |
| Agent | Distinct role, authority, tools, and delegation |

`docs/references/common/standards/agent-assets-standard-baseline.md` owns the standards-adjacent baseline. `docs/references/common/standards/agent-assets-standard-personal.md` owns this repository's intentional non-standard extensions and operating conventions.

## Current Source / Exception Surfaces

| Directory | Role |
| --- | --- |
| `.agentsmesh/` | Canonical source for Agent Assets faithfully representable by the current AgentsMesh contract |
| `src/` | Transitional exception surface for assets not yet migrated to `.agentsmesh/` or not faithfully representable by the current contract |

Current `src/` profiles are compatibility boundaries, not a permanent taxonomy. Prefer `.agentsmesh/` over adding new long-term authority when semantics can be preserved without loss.

`agentsmesh.yaml` selects active coding-agent targets and features. Generated Copilot and Antigravity files are derived distribution artifacts and must not be hand-edited.

Skill specifications use the `agentskills.io` open standard as Tier 1. `docs/references/skills/agent-skills-io/agent-skills-io-specification.md` links official Tier 2 vendor/harness contracts without copying them. `docs/references/skills/agent-assets-skills-standard-personal.md` owns repository-local Skill extensions and `docs/references/skills/agent-assets-skills-target-profiles.md` owns target-profile details.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agentsmesh/` | Canonical Agent Assets and AgentsMesh lock |
| `.github/skills/`, `.github/copilot-instructions.md` | Generated GitHub Copilot projection |
| `.agents/rules/`, `.agents/skills/` | Generated Antigravity projection |
| `src/` | Transitional Agent Asset exceptions outside the current AgentsMesh contract |
| `tests/` | Repository-level automated tests |
| `evals/` | Cross-asset evaluation contracts when present |
| `docs/` | Human-facing documentation and references |
| `scripts/` | Repository automation, synchronization, and development tooling |

## Basic Workflow

```text
edit canonical asset source
  → agentsmesh lint / generate when applicable
  → agentsmesh check / generate --check when applicable
  → repository tests / applicable evals
```

Keep assets that AgentsMesh cannot yet represent faithfully as explicit exceptions without turning those exceptions into permanent taxonomy.
