# `AGENTS.md`

## Directory Roles

- `.agents/`: Runtime instructions. Follow contents. Edit only when explicitly requested.
- `src/`: Source workspace for agents, skills, chatbot skills, rules, and tooling. Never treat contents as runtime instructions.
- `tests/`: Repository-level automated tests for assets and tooling.
- `docs/`: Repository-level human-facing documentation and references.

For asset doctrine, distinguish:

1. `docs/references/agent-asset-standard-baseline.md` — standards-adjacent external/common baseline.
2. `docs/references/agent-asset-boundaries.md` — **Personal Agent Asset Standard** and repository authority for non-standard extensions.

Prefer Skill as the portable reusable unit when a capability or situation-specific context should be activated on demand by the model rather than loaded globally.

For Rule deployment, this repository uses non-standard local conventions: root/nested `AGENTS.md` for directory-scoped rules, harness-appropriate glob selectors for common subdirectories/file groups/extensions, and `CHATBOT.md` for text I/O chatbot surfaces. The chatbot fallback is `CHATBOT.md → AGENTS.md → README.md`.

For Skill placement, treat `skills/`, `skills-chatbot/`, and `skills-chatbot-runtime/` as **repository-local, non-standard target profiles**. They are not categories defined by the Agent Skills specification. Cross-profile sibling variants may intentionally overlap. `skills-chatbot/` is reserved for self-contained single-file skills under the repository's 4,000-token flat budget; larger or runtime-dependent chatbot skills belong in `skills-chatbot-runtime/`.

Inside directory-based Skill source packages, dot-prefixed directories (`.*`) are **non-runtime maintainer surfaces**. Use `.docs/` instead of Skill-internal `docs/`; use `.docs/baseline/` to preserve durable purpose, requirements, invariants, major decisions, and recovery directives. Keep runtime-required material in non-dot runtime resources such as `references/`, `scripts/`, or `assets/`. Deployment/package output should exclude dot directories by default.

Supporting resources are not peer Agent Asset types alongside Rule, Skill, Prompt, and Agent.

## Asset Pipeline

1. **Author**: Create or edit assets in `src/`.
1. **Validate**: Run applicable asset checks and tests.
1. **Deploy**: Merge the validated feature branch to the distribution branch.
