# Source Workspace (`src/`)

`src/` is the source workspace for AI agent assets.

| Directory | Role |
| --- | --- |
| `agents/` | Subagents and custom agents |
| `skills/` | Workspace-capable agent skills |
| `skills-chatbot/` | Flat natural-language chatbot skills |
| `skills-chatbot-runtime/` | Hosted chatbot skills with bundled/runtime capabilities |
| `rules/` | Reusable behavioral rules |
| `scripts/` | Development and validation tooling |

The three Skill directories are **target profiles, not a hierarchy**. The same capability may exist in multiple profiles so each harness can use the most efficient form it supports. Cross-profile overlap is therefore intentional when it preserves target-specific optimization and independent deployment.
