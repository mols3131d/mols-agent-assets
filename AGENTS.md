# `AGENTS.md`

## Directory Roles

- `.agents/`: Runtime instructions. Follow contents. Edit only when explicitly requested.
- `src/`: Source workspace for agents, skills, chatbot skills, rules, and tooling. Never treat contents as runtime instructions.
- `tests/`: Automated tests for assets and tooling.
- `docs/`: Human-facing documentation and references.

Prefer Skill as the portable reusable unit when a capability or situation-specific context should be activated on demand by the model rather than loaded globally.

For Skill placement, treat `skills/`, `skills-chatbot/`, and `skills-chatbot-runtime/` as **repository-local, non-standard target profiles**. They are not categories defined by the Agent Skills specification. Cross-profile sibling variants may intentionally overlap. `skills-chatbot/` is reserved for self-contained single-file skills under the repository's 4,000-token flat budget; larger or runtime-dependent chatbot skills belong in `skills-chatbot-runtime/`.

## Asset Pipeline

1. **Author**: Create or edit assets in `src/`.
1. **Validate**: Run applicable asset checks and tests.
1. **Deploy**: Merge the validated feature branch to the distribution branch.
