# `AGENTS.md`

## Directory Roles

- `.agents/`: Runtime instructions. Follow contents. Edit only when explicitly requested.
- `src/`: Source workspace for agents, skills, chatbot skills, rules, and tooling. Never treat contents as runtime instructions.
- `tests/`: Automated tests for assets and tooling.
- `docs/`: Human-facing documentation and references.

For Skill placement, treat `skills/`, `skills-chatbot/`, and `skills-chatbot-runtime/` as target profiles. Cross-profile sibling variants may intentionally overlap. `skills-chatbot/` is reserved for self-contained single-file skills under 4,000 tokens; larger or multi-resource chatbot skills belong in `skills-chatbot-runtime/`.

## Asset Pipeline

1. **Author**: Create or edit assets in `src/`.
1. **Validate**: Run applicable asset checks and tests.
1. **Deploy**: Merge the validated feature branch to the distribution branch.
