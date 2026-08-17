---
title: LLM-Readable Instructions
description: 에이전트가 최소 해석으로 올바른 행동을 선택하도록 지침을 작성하는 원칙
---

# LLM-Readable Instructions

LLM-readable instruction은 문장을 기계적으로 짧게 만드는 것이 아니라 **의도, 조건, 행동, 자유도, 검증 기준을 모델이 안정적으로 복원하게 하는 것**이다.

> 필요한 정보는 구체적으로 쓰고, 불필요한 해석과 선택은 줄이며, task의 위험에 맞는 자유도를 준다.

## Core Rules

1. **행동을 직접 쓴다.** 설명만 하지 말고 무엇을 하거나 하지 않아야 하는지 명확히 쓴다.
2. **조건과 행동을 연결한다.** trigger와 instruction을 가까이 두어 적용 시점을 추측하게 하지 않는다.
3. **구체적인 default를 둔다.** 여러 방법이 가능해도 선호 경로가 있다면 기본값을 제시하고 escape condition만 적는다.
4. **task fragility에 맞춰 specificity를 조절한다.** 안전하고 열린 문제에는 판단 여지를 주고, 오류 비용이 큰 작업에는 정확한 순서와 constraint를 준다.
5. **모델이 이미 아는 일반론을 반복하지 않는다.** project-specific fact, non-obvious gotcha, required procedure처럼 실제 행동을 바꾸는 정보에 context를 쓴다.
6. **같은 개념에는 같은 용어를 쓴다.** 의미 차이가 없는데 문체를 위해 용어를 바꾸지 않는다.
7. **충돌과 우선순위를 암시하지 않는다.** 동시에 적용될 수 있는 지침은 scope와 precedence가 분명해야 한다.
8. **형식이 중요하면 보여준다.** prose 설명보다 짧은 template이나 example이 더 명확한 경우 이를 사용한다.
9. **실제 실행으로 다듬는다.** 지침의 품질은 문장만 보고 판단하지 말고 task, trace, eval에서 확인한다.

## Instruction Shape

단계적 행동에는 다음 형태가 유용하다.

```text
Condition → Action → Constraint or Validation
```

예:

```text
API가 non-200 response를 반환하면 references/api-errors.md를 읽는다.
해당 오류 유형의 recovery procedure를 적용하고 다시 검증한다.
```

다음처럼 trigger와 성공 조건이 없는 표현은 피한다.

```text
필요하면 관련 문서를 보고 적절히 처리한다.
```

## Calibrate Freedom

| 상황 | 권장 자유도 | 지침 형태 |
| --- | --- | --- |
| 여러 접근이 유효하고 실패 비용이 낮음 | High | goal, heuristics, success criteria |
| 선호 패턴이 있지만 일부 변형 가능 | Medium | default procedure + 제한된 선택지 |
| 순서 오류나 잘못된 선택의 비용이 큼 | Low | exact steps, tool/script, validation gate |

정확한 지침이 항상 좋은 것도, 자유로운 지침이 항상 좋은 것도 아니다. **필요 이상으로 자유도를 제한하거나 열어 두지 않는다.**

## Stable Vocabulary

같은 개념에 같은 이름을 쓴다.

```text
권장: Rule → Rule → Rule
비권장: Rule → Policy → Guideline → Instruction
```

실제로 다른 개념이라면 다른 용어를 사용하고 그 경계를 정의한다.

## Defaults and Exceptions

정상 경로를 먼저 정의한다.

```text
Use pdfplumber for text extraction.
For scanned PDFs that require OCR, use the OCR workflow instead.
```

모든 대안을 동등하게 나열하면 모델이 불필요한 선택을 해야 한다. 예외는 **언제 default를 벗어나는지**를 설명해야 한다.

## Positive and Negative Instructions

가능하면 원하는 행동을 먼저 쓴다.

```text
변경 전에 현재 파일을 읽는다.
```

금지 자체가 중요한 guardrail이면 부정형을 유지한다.

```text
실행하지 않은 validation을 통과했다고 표현하지 않는다.
```

목표는 긍정형 문장 자체가 아니라 **행동 경계를 가장 분명하게 만드는 표현**이다.

## Examples and Templates

예시는 다음 경우에 가치가 높다.

- output contract를 prose보다 정확하게 보여줄 수 있다.
- boundary case의 차이를 명확히 한다.
- 모델이 반복해서 같은 형식을 잘못 해석한다.

이미 명확한 규칙을 장황하게 다시 설명하는 예시는 제거한다.

## What LLM-Readable Is Not

- 모든 문장을 한 줄로 압축하는 것이 아니다.
- 자연어를 전부 schema나 pseudo-code로 바꾸는 것이 아니다.
- 모든 edge case를 선제적으로 명시하는 것이 아니다.
- 같은 의무를 여러 표현으로 반복 강조하는 것이 아니다.
- 강한 모델에게 일반 상식을 다시 가르치는 것이 아니다.

좋은 instruction은 사람도 빠르게 이해할 수 있고 모델도 적은 불필요한 추론으로 행동을 선택할 수 있어야 한다.

## Review Test

다음 질문을 순서대로 확인한다.

1. 이 지침이 없으면 모델이 실제로 무엇을 잘못하는가?
2. 언제 적용되는지 명확한가?
3. default action이 있는가?
4. task 위험에 비해 자유도가 너무 높거나 낮지 않은가?
5. 결과나 validation 기준을 확인할 수 있는가?
6. 실제 task나 eval에서 지침이 행동을 개선했는가?

근거가 없는 instruction은 삭제 또는 실험 후보로 둔다.

## Research Basis

- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) — defaults over menus, procedures, gotchas, validation loop, real execution 기반 refinement를 권고한다.
- [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — context 비용과 task fragility에 따른 degree of freedom을 강조한다.
- [GitHub: Using custom instructions to unlock Copilot code review](https://docs.github.com/en/copilot/tutorials/customize-code-review) — 짧고 focused한 instruction, 명확한 structure, imperative directive를 권고한다.
- [OpenAI: Key Guidelines for Writing Instructions for Custom GPTs](https://help.openai.com/en/articles/9358033-key-guidelines-for-writing-instructions-for-custom-gpts) — 복잡한 지침을 단계화하고 trigger/instruction pair로 분리하는 방식을 제안한다.
