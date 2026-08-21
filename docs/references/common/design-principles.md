---
title: Agent Asset Design Principles
description: 에이전트 자산을 추가, 분리, 중복 제거, 단순화할 때 적용하는 공통 판단 순서
---

# Agent Asset Design Principles

목표는 규칙을 늘리는 것이 아니라 **행동 신뢰성과 authority를 보존하면서 local context를 최소화하는 것**입니다.

## 판단 순서

1. **Standard First / Local Delta Only** — 표준, 도구, target contract 또는 충분히 확립된 default가 이미 행동을 결정하면 local 문서에 다시 설명하지 않습니다. Local source는 deviation, extension, ambiguity resolution만 소유합니다.
1. **YAGNI** — 지금 실제 요구가 없는 구조·호환성·metadata를 만들지 않습니다.
1. **SRP** — trigger, permission, lifecycle 또는 변경 이유가 다르면 책임 분리를 검토합니다.
1. **DRY** — 같은 의미의 authoritative owner를 둘 이상 만들지 않습니다.
1. **KISS** — 필요한 책임, 정보, 경계와 검증을 유지하면서 현재 문제 해결에 기여하지 않는 복잡성을 제거합니다. 파일·단계·option 수나 문서 길이가 적다는 이유만으로 더 단순하다고 판단하지 않습니다.
1. **Progressive Disclosure** — discovery → core → conditional detail 순으로 필요한 context만 노출합니다.

앞 단계에서 제거할 수 있는 문제를 뒤 단계의 abstraction으로 해결하지 않습니다.

## Local Delta

Local rule이나 reference를 추가하기 전에 다음 중 하나인지 확인합니다.

- **Deviation** — upstream/default와 의도적으로 다르게 행동해야 합니다.
- **Extension** — upstream에 없는 repository-specific behavior나 boundary가 필요합니다.
- **Ambiguity resolution** — upstream만으로 이 repository에서 결정을 하나로 복원할 수 없습니다.

셋 중 어느 것도 아니면 작성하지 않는 것이 기본입니다. Upstream detail이 판단에 필요하면 authoritative source를 링크하거나 작업 시점에 확인하고, 그 내용을 local prose로 복제하지 않습니다.

관련 표준 가이드: [Agent Skills — Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)

## Guardrails

- "업계 상식"이라고 가정해 실제 target/version 차이나 중요한 local exception을 숨기지 않습니다.
- YAGNI를 이유로 이미 존재하는 비가역적 위험이나 required guard를 방치하지 않습니다.
- DRY 때문에 runtime 독립성을 깨거나 hidden dependency를 만들지 않습니다.
- KISS를 이유로 필요한 validation, safety guard 또는 중요한 boundary를 제거하지 않습니다.
- Progressive Disclosure로 detail을 분리해도 load condition과 critical gotcha는 발견 가능한 곳에 남깁니다.
- Source만으로 복구하기 어려운 durable rationale과 invariant는 보존하고, 작업 로그와 재생성 가능한 상태는 Git history에 맡깁니다.

## Human Comprehension

AI가 자산을 빠르게 만들수록 maintainer가 **무엇이 authoritative하고 왜 존재하는지 이해하는 속도**가 병목이 될 수 있습니다. 이를 더 많은 설명으로 해결하지 않습니다. 불필요한 owner, 책임 경계와 탐색 경로를 만들지 않고, 필요한 것은 명확하게 유지합니다.

관련 배경: [Understanding is the New Bottleneck](https://wikidocs.net/blog/@jaehong/23176/)

## Review

- 이것이 local deviation, extension 또는 ambiguity resolution인가?
- 이것이 없으면 현재 실제 문제가 생기는가?
- 하나의 책임을 여러 파일이 소유하거나 여러 책임이 한 파일에 섞였는가?
- 정책 변경 시 authoritative location이 하나로 명확한가?
- 더 단순하게 만들어도 행동과 안전성이 유지되는가?
- 아직 detail을 읽지 않은 agent도 언제 추가 context가 필요한지 알 수 있는가?
