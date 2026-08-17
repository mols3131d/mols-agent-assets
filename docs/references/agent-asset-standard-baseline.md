---
title: Agent Asset Standard Baseline
description: 외부 생태계와 공개 규격에 가까운 Agent customization 자산 개념의 최소 baseline
---

# Agent Asset Standard Baseline

이 문서는 여러 agent/chatbot 생태계에서 **표준 또는 표준에 가까운 형태로 확인되는 개념만** 정리한다.

목적은 이 저장소의 개인 규칙을 정당화하는 것이 아니라, 비표준 확장을 설계할 때 출발점이 되는 공통 분모를 제공하는 것이다.

> 하나의 범용 Agent Asset 표준이 모든 플랫폼에 존재하는 것은 아니다. 아래 분류는 공개 specification과 주요 harness의 공통 개념을 최대한 좁게 교집합으로 정리한 **standards-adjacent baseline**이다.

## Baseline Asset Concepts

| 개념 | 일반적 책임 | 대표적인 공개 형태 |
| --- | --- | --- |
| Instruction / Rule | 일정 scope에서 지속 적용되는 policy와 constraint | repository-wide instructions, path-specific instructions, agent instructions |
| Skill | 필요할 때 활성화되는 reusable capability | `SKILL.md` + optional bundled resources |
| Prompt | 특정 invocation에서 재사용하는 task intent와 입력 구조 | prompt files, saved prompts, command-like prompt templates |
| Agent | 독립 role, instructions, tools, authority, handoff/delegation을 가진 runtime actor | custom agents, subagents, agent definitions |

이 네 개를 모든 플랫폼이 동일한 이름과 schema로 지원한다는 의미는 아니다. **책임의 형태가 반복적으로 나타난다**는 의미다.

## Instructions / Rules

주요 coding-agent harness는 지속 지침을 repository-wide, path-specific, agent-specific 같은 scope로 제공한다.

대표적인 예:

- repository-wide custom instructions
- path/glob-specific instructions
- `AGENTS.md` 계열 agent instructions
- personal 또는 organization instructions

파일명, precedence, glob syntax, nested discovery semantics는 플랫폼마다 다르므로 하나의 범용 Rule file format을 가정하지 않는다.

## Skills

Agent Skills specification에서 Skill은 directory 단위 reusable capability다.

```text
skill-name/
├─ SKILL.md          # required
├─ scripts/          # optional
├─ references/       # optional
├─ assets/           # optional
└─ ...
```

핵심 특성:

- metadata를 통해 discovery 가능
- 모델 또는 harness가 relevance를 판단해 activation
- 활성화 시 `SKILL.md` instructions 로드
- 필요할 때 bundled resources를 추가 사용
- progressive disclosure로 context 비용을 제어 가능

공식 Agent Skills guidance는 activated `SKILL.md`를 5,000 tokens 미만으로 유지하는 것을 권장한다. 이는 권장사항이며 이 저장소의 별도 정책과 구분한다.

## Prompts

Prompt는 현재 invocation 또는 반복 가능한 invocation template의 task intent를 표현한다.

플랫폼에 따라 다음처럼 구현될 수 있다.

- 현재 chat/user prompt
- saved prompt
- `*.prompt.md`
- command 또는 workflow prompt template

Prompt는 persistent policy나 독립 runtime actor를 대신하지 않는다.

## Agents

Agent는 일반적으로 다음이 결합된 runtime actor다.

- role / instructions
- tools
- authority / permissions / guardrails
- handoff 또는 delegation
- output responsibility

단순히 instructions가 길거나 specialization 이름이 필요하다는 이유만으로 Agent를 만드는 것은 baseline 개념에서 요구되지 않는다.

## Supporting Resources

`references/`, `scripts/`, `assets/`, docs, evals, tests 등은 독립적인 peer behavioral asset type이라기보다 **다른 자산을 지원하는 resource**로 보는 편이 자연스럽다.

Agent Skills specification에서도 `references/`, `scripts/`, `assets/`는 Skill 내부 optional resources로 정의된다. 어떤 directory를 runtime/non-runtime으로 분류하는지는 여기서 별도 범용 규격으로 정의하지 않는다.

## What This Baseline Does Not Define

다음은 이 baseline의 일부가 아니다.

- `CHATBOT.md`
- `load-context-*` naming
- `skills/`, `skills-chatbot/`, `skills-chatbot-runtime/` 3-profile taxonomy
- flat `.skill.md` projection
- `<4,000 tokens` flat budget
- 이 저장소의 Rule fallback chain
- 이 저장소의 directory/glob Rule projection contract
- Skill 내부 dot-prefixed directory를 non-runtime으로 보는 convention
- `docs/ → .docs/` maintainer-document projection
- `.docs/baseline/*` preservation/recovery baseline

이들은 외부 표준에서 직접 가져온 규격이 아니라 **Personal Agent Asset Standard에서 정의하는 repository-local extensions**다.

## Relationship to Personal Standard

이 문서는 외부 기준에 가까운 **baseline**만 소유한다.

실제 이 저장소에서 어떤 자산 유형과 projection을 사용하고 어떻게 fallback·placement·packaging하는지는 [Agent Asset Boundaries](agent-asset-boundaries.md)의 **Personal Agent Asset Standard**가 소유한다.

Personal Standard가 baseline에서 벗어날 수는 있지만, 그 차이는 의도적인 비표준 확장으로 명시해야 한다.

## Primary Sources

- [Agent Skills Specification](https://agentskills.io/specification)
- [GitHub Copilot: About customizing responses](https://docs.github.com/en/copilot/concepts/prompting/response-customization)
- [GitHub Copilot: Custom instructions support](https://docs.github.com/en/copilot/reference/custom-instructions-support)
- [OpenAI Agents SDK: Agents](https://openai.github.io/openai-agents-python/agents/)
