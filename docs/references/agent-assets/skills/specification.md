---
description: Agent Skills 작업에서 공통 표준, 작성 프레임워크, 대상별 확장과 creator guidance의 현재 공식 원본을 concern별로 찾는 registry입니다.
---

# Agent Skills Specification

이 문서는 Agent Skills의 **로컬 명세 복제본이 아니라 공식 원본 라우터**입니다. Field, path, limit, discovery, invocation과 runtime behavior를 여기서 다시 정의하지 않습니다.

작성 원본과 결정별 권한은 [작성 원본과 권한](../../../development/source-authority.md)이 소유합니다. 이 문서는 Skill 작업에서 필요한 concern에 따라 읽을 원본만 좁힙니다.

## Source Resolution

| Concern | Read first |
| --- | --- |
| 사람이 관리하는 작성 원본 | 실제 작성 프레임워크의 current contract. Rulesync 작성 원본이면 [Rulesync](../../tooling/rulesync.md) |
| 공통 Skill package와 `SKILL.md` contract | [Agent Skills Specification](https://agentskills.io/specification) |
| Skill 작성 품질, `description` tuning과 eval guidance | Agent Skills creator documentation |
| 대상별 discovery, invocation, permissions, metadata와 packaging | 실제 target/harness의 official documentation |
| mols의 재사용 Skill 추가 관행 | [Skill Authoring Conventions](skill-authoring-conventions.md) |
| Repository verification과 behavioral evidence | [Testing](../../../development/testing.md), [Evaluation](../../../development/evaluation.md) |

구체적인 작업에서는 실제 작성 프레임워크와 대상을 먼저 식별합니다. 대상이 여러 개라면 각 계약을 독립적으로 확인하고 **여러 vendor의 field와 behavior를 합친 local superset을 공통 contract처럼 만들지 않습니다.**

한 대상이 지원하는 field나 invocation behavior를 다른 대상에도 적용된다고 추정하지 않습니다. 대상별 확장은 `SKILL.md` frontmatter뿐 아니라 sidecar config, package location, runtime setting 등 다른 surface에 있을 수 있습니다. 정확한 표현과 source-to-target mapping은 해당 작성 프레임워크와 대상 계약을 따릅니다.

## Open Standard

공통 contract를 확인할 때는 specification을 우선하고, 작성 품질이나 evaluation 방법이 필요할 때 creator guidance를 추가로 봅니다.

- [Specification](https://agentskills.io/specification)
- [Quickstart](https://agentskills.io/skill-creation/quickstart)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)
- [Client implementation](https://agentskills.io/client-implementation/adding-skills-support)
- [`skills-ref` validation library](https://github.com/agentskills/agentskills/tree/main/skills-ref)
- [Documentation index](https://agentskills.io/llms.txt)

Creator guidance는 작성 품질을 높이는 자료이지 specification field를 새로 만드는 authority가 아닙니다.

## Official Target / Harness References

| Ecosystem | Official reference |
| --- | --- |
| Anthropic / Claude | [Claude Platform Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [Claude Code Skills](https://code.claude.com/docs/en/skills) |
| Microsoft / GitHub | [Microsoft Agent Framework — Agent Skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills), [GitHub Copilot — About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), [Adding agent skills for Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) |
| Google | [Gemini CLI — Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md), [Creating Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/creating-skills.md), [Antigravity Skills](https://codelabs.developers.google.com/getting-started-with-antigravity-skills) |
| OpenAI / ChatGPT & Codex | [Build skills](https://learn.chatgpt.com/docs/build-skills) |
| xAI / Grok | [Grok shell Skill reference](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-shell/README.md#skills) |

대상별 세부사항이 필요하면 실제 대상 하나를 고른 뒤 해당 official source에서 필요한 concern만 읽습니다. Registry에 vendor가 있다는 사실은 이 repository의 projection support, compatibility 또는 test coverage를 의미하지 않습니다.

## Official Skill-Creator References

Creator Skill은 작성 workflow와 대상별 guidance를 얻기 위한 source입니다. 공통 specification이나 대상 runtime contract보다 높은 authority로 취급하지 않습니다.

- Anthropic — [`skill-creator`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- Microsoft — [`skill-creator`](https://github.com/microsoft/skills/blob/main/.github/skills/skill-creator/SKILL.md) for its Microsoft/Azure scope
- Google — Gemini CLI built-in [`skill-creator`](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/skills/builtin/skill-creator/SKILL.md)
- OpenAI — [`skill-creator`](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md)

공식 creator를 확인하지 못한 대상은 해당 대상의 official authoring documentation을 사용합니다.

## Boundary

이 registry는 Agent Skills specification, vendor documentation 또는 creator Skill의 내용을 다시 설명하지 않습니다. 정확한 field semantics, limits, path, precedence, invocation과 runtime behavior는 작업 시점의 applicable authoritative source에서 확인합니다.
