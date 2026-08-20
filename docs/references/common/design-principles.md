---
title: Agent Asset Design Principles
description: 에이전트 자산을 추가, 분리, 중복 제거, 단순화할 때 적용하는 공통 판단 순서
---

# Agent Asset Design Principles

목표는 규칙을 늘리는 것이 아니라 **행동 신뢰성과 authority를 보존하면서 구조와 context를 최소화하는 것**입니다.

## 판단 순서

1. **YAGNI** — 지금 실제 요구가 없는 구조·호환성·metadata를 만들지 않습니다.
1. **SRP** — trigger, permission, lifecycle 또는 변경 이유가 다르면 책임 분리를 검토합니다.
1. **DRY** — 같은 의미의 authoritative owner를 둘 이상 만들지 않습니다.
1. **KISS** — 같은 신뢰성을 더 적은 파일·단계·option으로 만들 수 있으면 단순한 쪽을 택합니다.
1. **Progressive Disclosure** — discovery → core → conditional detail 순으로 필요한 context만 노출합니다.

앞 단계에서 제거할 수 있는 문제를 뒤 단계의 abstraction으로 해결하지 않습니다.

## Guardrails

- YAGNI를 이유로 이미 존재하는 비가역적 위험이나 required guard를 방치하지 않습니다.
- DRY 때문에 runtime 독립성을 깨거나 hidden dependency를 만들지 않습니다.
- KISS를 이유로 필요한 validation, safety guard 또는 중요한 boundary를 제거하지 않습니다.
- Progressive Disclosure로 detail을 분리해도 load condition과 critical gotcha는 발견 가능한 곳에 남깁니다.
- Source만으로 복구하기 어려운 durable rationale과 invariant는 보존하고, 작업 로그와 재생성 가능한 상태는 Git history에 맡깁니다.

## Human Comprehension

AI가 자산을 빠르게 만들수록 maintainer가 **무엇이 authoritative하고 왜 존재하는지 이해하는 속도**가 병목이 될 수 있습니다. 이를 더 많은 설명으로 해결하지 않습니다. Owner, 책임 경계와 탐색 경로를 줄이고 명확하게 유지합니다.

관련 배경: [Understanding is the New Bottleneck](https://wikidocs.net/blog/@jaehong/23176/)

## Review

- 이것이 없으면 현재 실제 문제가 생기는가?
- 하나의 책임을 여러 파일이 소유하거나 여러 책임이 한 파일에 섞였는가?
- 정책 변경 시 authoritative location이 하나로 명확한가?
- 더 단순하게 만들어도 행동과 안전성이 유지되는가?
- 아직 detail을 읽지 않은 agent도 언제 추가 context가 필요한지 알 수 있는가?
