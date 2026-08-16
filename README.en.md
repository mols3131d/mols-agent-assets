# mols-agent-assets

Repository for developing, validating, and managing AI agent assets.

## Asset Types

| Type | Purpose |
| --- | --- |
| `agents` | Subagent and custom agent definitions |
| `skills` | Workspace-capable agent skills |
| `skills-chatbot` | Self-contained single-file chatbot skills under 4,000 tokens |
| `skills-chatbot-runtime` | Chatbot skills using bundled resources or hosted runtime capabilities |
| `rules` | Reusable behavioral rules |

The three Skill profiles may contain target-specific variants of the same capability. Cross-profile semantic overlap is allowed when it preserves independent deployment and lets each harness use the most efficient representation it supports.

## Repository Structure

| Directory | Purpose |
| --- | --- |
| `.agents/` | Local agent runtime instructions |
| `src/` | Asset source workspace |
| `tests/` | Automated tests |
| `docs/` | Human-facing documentation and references |
| `scripts/` | Repository automation tools |
