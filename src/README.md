# Source Workspace (`src/`)

`src/` is the source workspace for AI agent assets.

| Directory | Role |
| --- | --- |
| `agents/` | Subagents and custom agents |
| `skills/` | Workspace-capable agent skills |
| `skills-chatbot/` | Self-contained single-file chatbot skills under the 4,000-token flat budget |
| `skills-chatbot-runtime/` | Bundled/runtime chatbot skills for larger or multi-resource capabilities |
| `rules/` | Reusable behavioral rules |
| `scripts/` | Development and validation tooling |

The three Skill directories are **target profiles, not a hierarchy**. The same capability may exist in multiple profiles so each harness can use the most efficient form it supports. Cross-profile overlap is therefore intentional when it preserves target-specific optimization and independent deployment.
