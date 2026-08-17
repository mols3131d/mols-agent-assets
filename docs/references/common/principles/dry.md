---
title: DRY
description: 에이전트 자산에서 같은 지식의 authoritative owner를 명확히 해 semantic drift를 막는 원칙
---

# DRY

에이전트 자산에서 DRY는 같은 문장을 없애는 것이 아니라 **같은 지식이 여러 곳에서 독립적으로 진화하지 않게 하는 것**이다.

> 하나의 의미에는 가능한 한 하나의 authoritative owner를 둔다.

## Rules

- textual duplication보다 semantic duplication을 찾는다.
- canonical owner가 의미를 정의하고 소비 자산은 행동에 필요한 최소 적용만 가진다.
- 정책이 바뀔 때 수정해야 할 authoritative location이 하나로 명확해야 한다.
- runtime이 원본을 읽을 수 없으면 독립 실행에 필요한 최소 제약은 반복할 수 있다.
- 짧은 반복을 없애려고 hidden dependency나 깊은 reference chain을 만들지 않는다.

## Drift Test

다음이 모두 참이면 통합을 우선한다.

1. 두 위치가 같은 지식을 정의한다.
2. 하나가 바뀌면 다른 하나도 의미상 함께 바뀌어야 한다.
3. authoritative owner를 하나로 정할 수 있다.
4. 중앙화가 runtime 독립성이나 context 효율을 해치지 않는다.

4가 실패하면 **owner는 하나로 유지하고 최소 로컬 적용만 허용**한다.

## Boundary

DRY는 책임이 다른 자산을 문장이 비슷하다는 이유로 합치지 않는다. 책임 경계는 [SRP](srp.md)가 결정한다.

아직 반복되지 않은 것을 공통 abstraction으로 만드는 문제는 [YAGNI](yagni.md)가 먼저 판단한다.

## Anti-Patterns

- 같은 policy table을 여러 자산이 각각 authoritative하게 소유한다.
- 정책 변경마다 여러 파일을 수동 동기화한다.
- 원본과 사본 중 무엇이 authoritative한지 알 수 없다.
- 몇 줄 중복을 없애기 위해 shared layer나 양방향 reference를 추가한다.

## Sources

- [The Pragmatic Programmer Tips: DRY](https://pragprog.com/tips/)
- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Agent Skills Specification](https://agentskills.io/specification)
