---
title: Instruction Authoring
description: 모델이 최소 해석으로 trigger, action, 자유도와 validation을 복원하도록 behavioral instruction을 작성하는 원칙
---

# Instruction Authoring

좋은 instruction은 모델이 **언제 무엇을 해야 하는지 불필요하게 추론하지 않게** 합니다.

## Rules

- Local behavior를 바꾸지 않는 upstream/default/common-practice 재진술은 쓰지 않습니다. Local delta 판정은 [Design Principles](design-principles.md)가 소유합니다.
- Required action을 직접 씁니다. 설명만으로 행동을 암시하지 않습니다.
- Trigger, action, constraint와 validation을 가능한 한 가까이 둡니다.
- Default를 하나 두고 대안은 default를 벗어나는 실제 조건이 있을 때만 노출합니다.
- 같은 개념에는 같은 용어를 사용합니다.
- 충돌 가능성이 있으면 scope와 precedence를 명시합니다.
- Format이 계약일 때만 example이나 template으로 고정합니다.
- 실패 비용이 낮은 열린 문제는 goal/criteria 중심, 순서 오류 비용이 큰 작업은 exact step/guardrail 중심으로 씁니다.
- Validation은 관찰 가능한 결과로 씁니다.

기본 형태는 다음으로 충분합니다.

```text
Condition → Action → Constraint / Validation
```

`필요하면 관련 문서를 보고 적절히 처리한다`처럼 condition과 expected action을 모델에게 다시 추론시키는 표현은 피합니다.

## Freedom

| 상황 | 기본 형태 |
| --- | --- |
| 여러 접근이 유효하고 실패 비용이 낮음 | goal + heuristics + success criteria |
| 선호 경로가 있으나 변형 가능 | default procedure + escape condition |
| 순서·선택 오류 비용이 큼 | exact steps + constraint + validation gate |

## Review

각 instruction에서 다음을 복원할 수 있어야 합니다.

- 이것이 실제 local delta인가?
- 언제 적용되는가?
- default action은 무엇인가?
- 예외나 금지가 실제 행동을 어떻게 바꾸는가?
- 성공 또는 실패를 무엇으로 확인하는가?

행동을 바꾸지 않는 설명은 제거 후보입니다. Conditional detail은 [Design Principles](design-principles.md)의 Progressive Disclosure를 따릅니다.

## Sources

- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [GitHub: Custom instructions for Copilot code review](https://docs.github.com/en/copilot/tutorials/customize-code-review)
- [OpenAI: Key Guidelines for Writing Instructions for Custom GPTs](https://help.openai.com/en/articles/9358033-key-guidelines-for-writing-instructions-for-custom-gpts)
