---
title: Agent Asset DRY Principle
description: 에이전트 자산에서 같은 지식의 독립적 복제와 drift를 막기 위한 소유권 원칙
---

# Agent Asset DRY Principle

에이전트 자산에서 DRY는 **같은 문장을 없애는 것**이 아니라, 같은 지식이 여러 곳에서 서로 다른 진실로 진화하지 않게 하는 것이다.

> 하나의 의미에는 가능한 한 하나의 명확한 authoritative owner를 둔다.

## Core Rules

1. **문장이 아니라 지식의 중복을 찾는다.** 표현이 달라도 같은 정책, 계약, 판단 기준을 독립적으로 정의하면 semantic duplication이다.
2. **정의와 로컬 적용을 구분한다.** canonical owner가 의미를 정의하고, 소비 자산은 현재 행동에 필요한 최소 제약만 적용할 수 있다.
3. **변경 권한을 하나로 만든다.** 지식이 바뀔 때 어디를 수정해야 하는지가 명확해야 한다.
4. **의도적 중복은 독립성을 위해서만 허용한다.** runtime context가 분리되어 원본을 읽을 수 없다면 핵심 제약을 로컬에 반복할 수 있다.
5. **DRY를 위해 결합도를 높이지 않는다.** 짧은 반복을 없애려고 hidden dependency, 깊은 reference chain, 공용 abstraction을 만들지 않는다.
6. **아직 반복되지 않은 것을 추상화하지 않는다.** 예상 재사용은 DRY의 근거가 아니다.

## Knowledge Ownership

다음 세 가지를 구분한다.

| 종류 | 의미 | 처리 |
| --- | --- | --- |
| Definition | 정책이나 지식의 authoritative 의미 | canonical owner 한 곳에서 관리 |
| Local application | 다른 자산이 실제 행동에 필요한 부분 | 최소한으로 유지 |
| Independent copy | 원본과 독립적으로 수정될 수 있는 복제 | 가능한 한 제거 |

`Local application`은 원본 전체의 복사가 아니다. 예를 들어 repository policy가 destructive action의 승인 원칙을 정의한다면, 삭제 Skill에는 그 workflow에 필요한 승인 행동만 남길 수 있다.

## Drift Test

중복이 보이면 묻는다.

1. 두 내용이 같은 지식을 정의하는가?
2. 하나가 바뀌면 다른 하나도 의미상 반드시 바뀌어야 하는가?
3. authoritative owner를 한 곳으로 정할 수 있는가?
4. 중앙화가 runtime 독립성이나 context 효율을 해치지 않는가?

1~3이 `Yes`이고 4가 `No`라면 통합한다. 4가 `Yes`라면 **canonical ownership은 하나로 유지하되 최소한의 로컬 적용**을 허용한다.

## What DRY Is Not

- 같은 단어나 문장이 두 번 등장하면 위반이라는 뜻이 아니다.
- 모든 공통 문장을 shared file로 옮기라는 뜻이 아니다.
- 모든 자산이 runtime에 canonical reference를 읽어야 한다는 뜻이 아니다.
- 서로 다른 책임을 문장이 비슷하다는 이유로 합치라는 뜻이 아니다.
- 미래 재사용을 예상해 base asset을 만들라는 뜻이 아니다.

## Anti-patterns

- 같은 policy table을 여러 Rule과 Skill이 각각 소유한다.
- 한 정책을 수정할 때 여러 파일을 수동 동기화해야 한다.
- 원본과 사본 중 무엇이 authoritative한지 알 수 없다.
- 몇 줄의 반복을 없애려고 새로운 router나 inheritance 구조를 만든다.
- project-specific 지식을 범용 Skill 내부의 독립 사본으로 유지한다.
- 양방향 reference로 ownership을 흐린다.

## Review Question

> **이 지식의 의미가 바뀌면 authoritative하게 수정해야 할 곳이 하나로 명확한가?**

아니라면 ownership을 정리한다. 다만 그 해결책이 자산의 self-contained behavior를 깨면 정의와 최소 로컬 적용을 분리한다.

## Research Basis

- [The Pragmatic Programmer Tips: DRY](https://pragprog.com/tips/) — DRY를 textual repetition이 아니라 knowledge의 single authoritative representation으로 정의한다.
- [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) — 실제 프로젝트 지식에서 reusable pattern을 추출하고 불필요한 context를 제거하도록 권고한다.
- [Agent Skills Specification](https://agentskills.io/specification) — core instructions와 on-demand references를 분리하는 구조적 근거를 제공한다.
