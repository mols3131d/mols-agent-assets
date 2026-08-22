# Agent Skills Specification

Agent Skills 관련 **official source registry**입니다. Specification의 field·path·validation 세부사항은 local snapshot으로 복제하지 않습니다.

## Authority

1. **Rulesync canonical contract** — Rulesync-managed source일 때의 canonical representation → [Rulesync](../../references/tooling/rulesync.md)
1. **Agent Skills open standard** — portable Agent Skills contract가 실제로 적용될 때
1. **Target/harness official contract** — discovery, activation, permissions, packaging, host metadata 등 target-specific behavior
1. **Repository convention** — 위 source가 소유하지 않는 local authoring 관행 → [Skill Authoring Conventions](skill-authoring-conventions.md)

Vendor 문서가 registry에 있다는 사실만으로 이 저장소의 support나 Agent Skills 호환을 추정하지 않습니다.

## Open Standard

- [Specification](https://agentskills.io/specification)
- [Quickstart](https://agentskills.io/skill-creation/quickstart)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Client implementation](https://agentskills.io/client-implementation/adding-skills-support)
- [Documentation index](https://agentskills.io/llms.txt)

## Official Target / Harness References

| Ecosystem | Official reference |
| --- | --- |
| Anthropic / Claude | [Claude Platform Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [Claude Code Skills](https://code.claude.com/docs/en/skills) |
| Microsoft / GitHub | [Microsoft Agent Framework — Agent Skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills), [GitHub Copilot — About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |
| Google | [Gemini CLI — Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md), [Antigravity Skills](https://codelabs.developers.google.com/getting-started-with-antigravity-skills) |
| OpenAI / ChatGPT & Codex | [Build skills](https://developers.openai.com/codex/skills) |
| xAI / Grok | [Grok shell Skill reference](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-shell/README.md#skills) |

Target-specific 세부사항이 필요하면 실제 target 하나를 먼저 고른 뒤 해당 official source만 읽습니다. 이 registry는 repository vendor support matrix가 아닙니다.

## Official Skill-Creator References

- Anthropic — [`skill-creator`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- Microsoft — [`skill-creator`](https://github.com/microsoft/skills/blob/main/.github/skills/skill-creator/SKILL.md) for its Microsoft/Azure scope
- Google — Gemini CLI built-in [`skill-creator`](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/skills/builtin/skill-creator/SKILL.md)
- OpenAI — [`skill-creator`](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md)

Creator Skill은 target-specific authoring guidance이며 portable specification의 authority가 아닙니다. 공식 creator를 확인하지 못한 target은 해당 target의 official authoring guide를 사용합니다.
