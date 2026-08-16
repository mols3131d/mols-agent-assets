# Upstream Sources

최신 플랫폼 규칙이 중요한 작업에서는 원문을 다시 확인한다. 이 파일은 복사 원본이 아니라 비교·검증을 위한 출처 인덱스다.

## Primary Sources

| Source | URL | Primary Value |
| --- | --- | --- |
| OpenAI Skill Creator | <https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md> | 간결성, 자유도 조절, progressive disclosure, 기본 생성·검증 흐름 |
| Microsoft Skill Creator | <https://github.com/microsoft/skills/tree/main/.github/skills/skill-creator> | 최신 공식 근거 우선, token budget, hero workflow, 효율·보안 검증 |
| Anthropic Skill Creator | <https://github.com/anthropics/skills/tree/main/skills/skill-creator> | 평가 사례, 정량·정성 비교, 반복 개선, trigger description 최적화 |

## Selection Rules

- 공통으로 반복되는 원칙은 범용 코어 후보로 본다.
- 특정 제품·SDK·런타임에만 필요한 규칙은 adapter 또는 reference로 격리한다.
- 원문의 구조를 그대로 병합하지 않는다. 대상 스킬의 목적, 위험도, 사용 빈도에 맞춰 재구성한다.
- 외부 원칙이 `DIRECTIVE.md`와 충돌하면 인간 기준선을 우선한다.
- 최신성에 민감한 내용은 링크를 다시 열고 날짜·버전·범위를 확인한다.

## Adopted Synthesis

| Principle | Source Influence | Application |
| --- | --- | --- |
| Context efficiency | OpenAI, Microsoft, Anthropic | 핵심 흐름은 `SKILL.md`, 세부는 직접 링크된 references로 분리 |
| Degrees of freedom | OpenAI, Microsoft | 취약한 작업만 스크립트와 강한 제약 사용 |
| Evidence freshness | Microsoft | API·SDK·플랫폼 사실은 공식 최신 자료 검증 |
| Evaluation loop | Anthropic | 대표 사례로 개선 전후를 비교하고 실패 시 재개선 |
| Trigger quality | OpenAI, Anthropic | description에 기능과 호출 상황을 함께 명시 |
| Deterministic tools | OpenAI, Anthropic | 반복·기계 검증은 scripts로 구현 |

## Deliberate Deviations

- `docs/`를 패키지에 포함한다. 이는 이 스킬의 인간 의도 복구 요구사항이 일반적인 최소 패키징 관례보다 우선하기 때문이다.
- `DIRECTIVE.md`와 `WORKING.md`를 모든 대상 스킬에 의무화한다.
- 기존 스킬 개선을 신규 생성보다 우선한다.
