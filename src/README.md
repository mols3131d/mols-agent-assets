# Source Workspace (`src/`)

`src/` is the source workspace for AI agent assets.

| Directory | Role |
| --- | --- |
| `agents/` | Subagents and custom agents |
| `skills/` | Workspace-capable agent skills |
| `skills-chatbot/` | Self-contained single-file chatbot skills under the 4,000-token flat budget |
| `skills-chatbot-runtime/` | Bundled/runtime chatbot skills for larger or runtime-dependent capabilities |
| `rules/` | Reusable behavioral Rule sources and repository-local projections |
| `scripts/` | Development and validation tooling |

The peer Agent Asset types used by this repository are **Rule, Skill, Prompt, and Agent**. Supporting resources are not peer asset types.

Asset doctrine is intentionally split into two documents:

1. [`agent-asset-standard-baseline.md`](../docs/references/agent-asset-standard-baseline.md) — standards-adjacent external/common baseline.
1. [`agent-asset-boundaries.md`](../docs/references/agent-asset-boundaries.md) — **Personal Agent Asset Standard**, authoritative for this repository's non-standard extensions.

Skills are the preferred portable unit for reusable capabilities and situation-specific context that a model can activate on demand.

> `skills/`, `skills-chatbot/`, and `skills-chatbot-runtime/` are **repository-local, non-standard target profiles**. They are not categories defined by the Agent Skills specification.

The three profiles are not a hierarchy. The same capability may exist in multiple profiles so each harness can use the most efficient form it supports. Cross-profile overlap is intentional when it preserves target-specific optimization and independent deployment.

Inside a directory-based Skill source package, dot-prefixed directories (`.*`) are the repository-local **non-runtime maintainer surface**. Use `.docs/` instead of Skill-internal `docs/`; reserve `.docs/baseline/` for durable purpose, requirements, invariants, major decisions, and recovery directives. Keep runtime-required resources in non-dot surfaces such as `references/`, `scripts/`, or `assets/`.

Rule deployment also uses repository-local conventions: root/nested `AGENTS.md` for directory scope, target-appropriate glob selectors for common subdirectories/file groups/extensions, and `CHATBOT.md` for text I/O chatbot surfaces with the fallback `CHATBOT.md → AGENTS.md → README.md`. See `rules/README.md` and the Personal Standard.
