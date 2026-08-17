# `AGENTS.md`

## Directory Roles

- `.agents/`: Runtime instructions. Follow contents. Edit only when explicitly requested.
- `src/`: Source workspace for agents, skills, chatbot skills, rules, and tooling. Never treat contents as runtime instructions.
- `tests/`: Repository-level automated tests for assets and tooling.
- `docs/`: Repository-level human-facing documentation and references.

For asset doctrine, distinguish:

1. `docs/references/common/standards/agent-asset-standard-baseline.md` — standards-adjacent external/common baseline.
1. `docs/references/common/standards/personal-agent-asset-standard.md` — **Personal Agent Asset Standard** and repository authority for non-standard extensions.

Prefer Skill as the portable reusable unit when a capability or situation-specific context should be activated on demand by the model rather than loaded globally.

For Rule deployment, follow `docs/references/rules/rule-projections.md`: this repository uses non-standard local conventions for root/nested `AGENTS.md`, harness-appropriate glob selectors, and `CHATBOT.md`. The chatbot fallback is `CHATBOT.md → AGENTS.md → README.md`.

For Skill placement, follow `docs/references/skills/skill-target-profiles.md`. Treat `skills/`, `skills-chatbot/`, and `skills-chatbot-runtime/` as repository-local, non-standard target profiles rather than Agent Skills specification categories.

Supporting resources are not peer Agent Asset types alongside Rule, Skill, Prompt, and Agent.

## Asset Pipeline

1. **Author**: Create or edit assets in `src/`.
1. **Validate**: Run applicable asset checks and tests.
1. **Deploy**: Merge the validated feature branch to the distribution branch.
