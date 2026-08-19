---
title: Agent Asset 설계 원칙
description: 에이전트 자산을 추가, 분리, 중복 제거, 단순화할 때 적용하는 공통 판단 순서
---

# Agent Asset 설계 원칙

원칙은 체크리스트를 늘리기 위한 것이 아니라 **불필요한 자산과 context를 줄이면서 책임과 행동을 선명하게 유지하기 위한 판단 도구**다.

## 판단 순서

새 자산·규칙·분기·추상화를 만들거나 기존 구조를 손볼 때 다음 순서로 본다.

1. **YAGNI** — 지금 필요한가?
1. **SRP** — 하나의 책임인가?
1. **DRY** — 같은 지식의 정본 소유자는 누구인가?
1. **KISS** — 같은 신뢰성을 더 적은 복잡도로 만들 수 있는가?
1. **Progressive Disclosure** — 필요한 context만 필요한 시점에 노출되는가?

앞 단계에서 제거할 수 있는 것을 뒤 단계의 추상화로 해결하지 않는다.

## 원칙별 책임

| 원칙 | 담당하는 판단 | 담당하지 않는 판단 |
| --- | --- | --- |
| [YAGNI](agent-assets-principles-yagni.md) | 현재 필요성, 성급한 기능 추가 | 책임 분리 방식 |
| [SRP](agent-assets-principles-srp.md) | 책임, 변경 이유 | 중복 제거 자체 |
| [DRY](agent-assets-principles-dry.md) | 지식 소유권, drift | 무조건적인 중앙화 |
| [KISS](agent-assets-principles-kiss.md) | 최소 충분 복잡도 | 미래 요구 판단 |
| [Progressive Disclosure](agent-assets-principles-progressive-disclosure.md) | context 로딩 경계 | 기능 책임 분리 |

## 충돌 시 원칙

원칙이 충돌해 보이면 **행동 신뢰성과 안전성을 먼저 보존**한다.

- DRY 때문에 runtime 독립성이 깨지면 정본 소유자는 하나로 두되 필요한 최소 제약은 로컬에 반복할 수 있다.
- KISS 때문에 중요한 검증이나 안전 장치를 삭제하지 않는다.
- YAGNI 때문에 비가역적 위험을 방치하지 않는다.
- Progressive Disclosure 때문에 트리거 자체를 숨기지 않는다.

원칙은 결과를 자동으로 결정하는 규칙이 아니다. 각 원칙이 소유하는 질문만 사용하고, 다른 원칙의 책임까지 확장하지 않는다.
