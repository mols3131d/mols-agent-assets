---
title: LLM-Readable Instructions
description: 모델이 최소 해석으로 적용 조건, 행동, 자유도와 검증 기준을 복원하도록 지침을 작성하는 원칙
---

# LLM-Readable Instructions

좋은 instruction은 모델이 **언제 무엇을 해야 하는지**를 불필요하게 추론하지 않게 한다.

## Authoring Rules

1. **행동을 직접 쓴다.** 설명만 두지 말고 required action을 명시한다.
2. **trigger와 action을 가까이 둔다.** 조건, 행동, validation을 한 흐름으로 읽을 수 있게 한다.
3. **default를 하나 둔다.** 대안은 default를 벗어나는 조건이 있을 때만 노출한다.
4. **같은 개념에는 같은 용어를 쓴다.** 문체를 위해 동의어를 섞지 않는다.
5. **scope와 precedence를 명시한다.** 동시에 적용될 수 있는 instruction의 충돌을 모델에게 추측시키지 않는다.
6. **형식이 계약이면 예시나 template을 보여준다.** prose보다 정확할 때만 사용한다.
7. **실패 비용에 맞춰 자유도를 조절한다.** 열린 문제는 goal/criteria 중심, 취약한 작업은 exact step/guardrail 중심으로 쓴다.
8. **validation을 관찰 가능하게 쓴다.** 실행하지 않은 검증을 추정하지 않게 한다.

## Preferred Shape

```text
Condition → Action → Constraint / Validation
```

예:

```text
API가 non-200 response를 반환하면 references/api-errors.md를 읽는다.
해당 recovery procedure를 적용한 뒤 같은 request를 다시 검증한다.
```

다음처럼 조건과 결과가 빠진 표현은 피한다.

```text
필요하면 관련 문서를 보고 적절히 처리한다.
```

## Freedom

| Situation | Instruction style |
| --- | --- |
| 여러 접근이 유효하고 실패 비용이 낮음 | goal + heuristics + success criteria |
| 선호 경로가 있지만 일부 변형 가능 | default procedure + escape condition |
| 순서나 선택 오류의 비용이 큼 | exact steps + constraint + validation gate |

## Editing Test

각 instruction에 대해 묻는다.

- 언제 적용되는가?
- default action은 무엇인가?
- 금지나 예외가 실제 행동을 바꾸는가?
- 같은 개념을 다른 이름으로 부르고 있지 않은가?
- 성공 또는 실패를 확인할 수 있는가?

행동을 바꾸지 않는 설명은 [KISS](../principles/agent-assets-principles-kiss.md)에 따라 제거 후보로 본다. 조건부 상세 context는 [Progressive Disclosure](../principles/agent-assets-principles-progressive-disclosure.md)에 따라 분리한다.

## Sources

- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [GitHub: Using custom instructions to unlock Copilot code review](https://docs.github.com/en/copilot/tutorials/customize-code-review)
- [OpenAI: Key Guidelines for Writing Instructions for Custom GPTs](https://help.openai.com/en/articles/9358033-key-guidelines-for-writing-instructions-for-custom-gpts)
