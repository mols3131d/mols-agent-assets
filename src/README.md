# Source Workspace (`src/`)

`src/` is the source workspace for AI agent assets.

| Directory | Role |
| --- | --- |
| `agents/` | Subagents and custom agents |
| `skills/` | Workspace-capable agent skills |
| `skills-chatbot/` | Self-contained single-file chatbot skills under the 4,000-token flat budget |
| `skills-chatbot-runtime/` | Bundled/runtime chatbot skills for larger or runtime-dependent capabilities |
| `rules/` | Reusable behavioral rules |
| `scripts/` | Development and validation tooling |

Skills are the preferred portable unit for reusable capabilities and situation-specific context that a model can activate on demand.

> `skills/`, `skills-chatbot/`, and `skills-chatbot-runtime/` are **repository-local, non-standard target profiles**. They are not categories defined by the Agent Skills specification.

The three profiles are not a hierarchy. The same capability may exist in multiple profiles so each harness can use the most efficient form it supports. Cross-profile overlap is intentional when it preserves target-specific optimization and independent deployment.
