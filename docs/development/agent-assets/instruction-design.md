---
title: Instruction Design
description: Agent instruction의 적용 조건·행동·권한·검증·중단을 명확히 표현하고 구체성을 선택할 때 사용합니다.
---

# Instruction Design

Instruction으로 표현할 행동을 선택한 뒤에는 **언제, 무엇을, 어떤 권한으로 수행하며 어떻게 끝내는지** 복원할 수 있게 작성합니다. Instruction 자체가 필요한지는 [Agent Asset Design Principles](design-principles.md)가 결정합니다.

## 행동 계약

```text
Condition → Behavior → Boundary → Validation / Stop
```

- **Condition** — 적용·비적용 조건
- **Behavior** — 필요한 결과와 필수 행동
- **Boundary** — 보존·금지 사항, 재량과 권한
- **Validation / Stop** — 관찰할 성공·실패와 fallback·인계·중단 조건

모든 요소를 정형식으로 나열할 필요는 없습니다. 결과만 중요하면 절차를 강제하지 않고, 순서·경로 자체가 계약일 때만 정확한 단계를 씁니다.

## 작성과 구체성

- 필수 행동은 직접 명시합니다. 설명·예시만으로 행동을 암시하거나 `적절히 처리한다`처럼 결정을 독자에게 떠넘기지 않습니다.
- 같은 행동은 정본 한 곳에서 정의합니다. Generated projection은 별도 정본이 아닙니다. 규칙과 설명용 맥락을 구분하고, 관련 조건·행동·예외·검증은 가까이 둡니다.
- 기본 경로는 하나로 정하고 대안은 실제 분기 조건이 있을 때만 둡니다. 금지만 제시해 다음 행동을 막지 않도록 허용되는 fallback이나 중단도 함께 명시합니다.
- `must`·`never`·`only`는 불변조건, 권한·안전 경계, 필수 계약에 사용합니다. 선호는 기본값과 벗어날 조건으로 표현합니다. 용어는 일관되게 유지합니다.

| 행동의 실패 비용 | 적절한 구체성 |
| --- | --- |
| 낮고 여러 방법이 유효함 | 결과·제약·성공 기준 |
| 선호 경로가 있으나 변형 가능 | 기본 절차와 예외 조건 |
| 순서·선택 오류의 영향이 큼 | 정확한 단계·금지 경계·검증 게이트 |

필요 없는 상세 절차를 강제하지 않으며, 정확한 경로나 순서가 계약인 경우 일반적인 모범 사례에 맡기지 않습니다.

## 범위·권한·충돌

Instruction을 의도한 대상에만 적용합니다. 다만 같은 owner·activation 아래 항상 함께 쓰이는 행동은 한 문서에 둘 수 있습니다. **파일 위치나 문구는 실행 권한을 만들지 않습니다.**

범위·precedence·permission은 실제 표준, 작성 프레임워크, 런타임 또는 프로젝트의 계약을 따릅니다. 부수 효과가 있다면 계속 실행할 수 있는 조건과 승인·인계·중단 경계를 명시합니다. 충돌을 해결할 권한이나 확실한 precedence가 없으면 임의로 승자를 정하지 말고 범위를 분리하거나 문제를 드러낸 뒤 인계·중단합니다. 작성 원본과 생성물의 관계는 [Source Authority](../source-authority.md)를 따릅니다.

## 맥락과 예시

항상 로드되는 instruction에는 실제 판단을 바꾸는 정보만 둡니다. 조건부 자료를 분리했다면 언제 읽는지 진입점에서 알 수 있게 합니다.

이유(rationale)는 예외 판단을 개선할 때, 예시(example)는 결과 형태·대표적인 edge case·관찰된 실패를 명확히 할 때만 사용합니다. 어느 것도 숨은 규칙이나 필수 행동을 대신하지 않습니다. 형식이 계약이면 template을 쓰되, 런타임의 schema·structured output이 직접 강제할 수 있다면 그 방법을 우선합니다.

## 검증과 종료

성공·실패를 가르는 **관찰 가능한 상태나 근거**를 명시합니다. 검증 실패, 근거 부족, 권한 부족은 구분하고 각각 필요한 retry·fallback·판단 유보·인계·중단을 선택합니다. 횟수 제한은 실제로 필요할 때만 고정합니다. 오류를 보지 못했다는 사실만으로 성공으로 간주하지 않습니다.

Repository의 deterministic validation, behavioral evaluation과 근거 수준은 [Development](../README.md)의 해당 정본이 소유합니다. 대상별 instruction path·상속·precedence·metadata 계약은 공식 source framework와 runtime에서 확인합니다.

## Sources

- [Agent Skills — Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Anthropic — Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [GitHub — Adding repository custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [OpenAI — Model guidance](https://developers.openai.com/api/docs/guides/latest-model)
