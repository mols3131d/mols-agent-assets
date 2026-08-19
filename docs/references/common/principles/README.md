---
title: Agent Asset 설계 원칙
description: 에이전트 자산을 추가, 분리, 중복 제거, 단순화할 때 적용하는 공통 판단 순서
---

# Agent Asset 설계 원칙

이 원칙들은 체크리스트를 늘리기 위한 규칙이 아니라 **불필요한 자산과 context를 줄이면서 책임과 행동을 선명하게 유지하기 위한 판단 도구**입니다.

## 판단 순서

1. **YAGNI** — 지금 실제로 필요한가?
1. **SRP** — 하나의 책임과 변경 이유를 가지는가?
1. **DRY** — 같은 의미의 authoritative owner가 둘 이상 생기는가?
1. **KISS** — 같은 신뢰성을 더 적은 복잡도로 만들 수 있는가?
1. **Progressive Disclosure** — 필요한 context만 필요한 시점에 노출되는가?

앞 단계에서 제거할 수 있는 것을 뒤 단계의 abstraction으로 해결하지 않습니다.

## 핵심 기준

| 원칙 | 적용 기준 |
| --- | --- |
| YAGNI | 현재 요구가 없는 future feature, compatibility layer, metadata를 미리 만들지 않음 |
| SRP | 다른 trigger, permission, lifecycle 또는 변경 이유가 있으면 분리를 검토 |
| DRY | textual duplication보다 semantic duplication을 찾고 가능한 한 authoritative owner를 하나로 둠 |
| KISS | 안전성과 검증을 보존하는 범위에서 structure, branch, option과 문서 수를 최소화 |
| Progressive Disclosure | discovery → core → conditional detail 순으로 필요한 정보만 로드 |

## 예외와 균형

- DRY를 위해 runtime 독립성이 깨지면 owner는 하나로 두고 실행에 필요한 최소 제약만 로컬에 반복할 수 있습니다.
- KISS를 이유로 중요한 validation이나 safety guard를 제거하지 않습니다.
- YAGNI를 이유로 이미 존재하는 비가역적 위험을 방치하지 않습니다.
- Progressive Disclosure로 세부 내용을 분리하더라도 trigger나 critical gotcha는 발견 가능한 위치에 남깁니다.
- 몇 줄 중복을 없애기 위해 hidden dependency나 깊은 reference chain을 만들지 않습니다.

## 빠른 검토 질문

- 이 자산·문서·규칙이 지금 없으면 실제 문제가 생기는가?
- 서로 다른 책임을 한 파일에 몰아넣었거나 같은 책임을 여러 파일이 소유하는가?
- 정책이 바뀔 때 authoritative location이 하나로 명확한가?
- 구조를 줄여도 행동 신뢰성과 안전성이 유지되는가?
- 아직 읽지 않은 agent도 다음 detail이 필요한 조건을 알아차릴 수 있는가?
