---
title: Rule Canonical Superset
description: 여러 coding-agent harness에 투영할 Rule의 repository-local canonical superset 기준
---

# Rule Canonical Superset

## Chosen Superset

여러 coding-agent harness에 같은 Rule을 배포할 때 이 저장소의 최적 Superset은 **Rulesync `.rulesync/rules/`의 unified Rule source**다.

이 선택은 GitHub Copilot, Google Antigravity 같은 target-native Rule을 하나의 policy authority에서 생성할 수 있으면서도, target마다 다른 표현과 지원 범위를 projection으로 남길 수 있기 때문이다.

```text
.rulesync/rules/ canonical Rule
├─ shared policy semantics
├─ target-scoped policy semantics
└─ scope / applicability intent
        ↓
   target-native Rules
```

Rulesync를 사용하지 않는 단일-target Rule까지 이 형식으로 강제하지 않는다. 이미 native Rule이 authoritative하면 그 source를 유지하는 bridge가 더 작고 적절할 수 있다.

## Superset Owns

- 공통 policy와 constraint
- Rule의 적용 의도와 scope semantics
- target마다 실제로 달라져야 하는 target-scoped semantics
- projection에서 보존해야 할 authority와 precedence boundary
- 표현 불가능하거나 근사가 필요한 의미의 compatibility expectation

Target별 filename, directory, selector syntax, metadata와 harness-native encoding은 Superset의 본질이 아니라 projection concern이다.

## Delivery Route

1. **Direct reuse** — target이 authoritative source를 직접 발견하고 필요한 semantics를 소비할 수 있으면 그대로 사용한다.
1. **Canonical fan-out** — `.rulesync/rules/`가 authoritative하고 native payload가 필요하면 생성한다.
1. **Native bridge** — 이미 한 harness의 native Rule이 authoritative하면 source를 유지한 채 필요한 target으로 변환한다.

단순 bridge를 위해 source authority를 `.rulesync/`로 옮기지 않는다. Canonicalization 자체가 의도된 경우에만 ownership을 변경한다.

## Projection

```text
Rule Superset
├─ GitHub Copilot Rule
├─ Google Antigravity IDE Rule
└─ Google Antigravity CLI Rule
```

Projection은 target의 실제 Rule contract에 맞춰 format, placement, selector와 지원 semantics를 조정한다. 생성 성공을 semantic parity로 보지 않는다.

Rule의 directory/glob/chatbot 배치 규칙은 [Rule Projections](agent-assets-rules-projections.md)가 소유한다.

Rulesync 기반 source resolution, preview, generation, bridge와 validation 실행 계약은 [`rulesync-agent-assets`](../../../src/skills/rulesync-agent-assets/SKILL.md)가 소유한다. 설치된 Rulesync version의 실제 target/feature 지원이 runtime authority다.

## Primary Reference

- [Rulesync](https://github.com/dyoshikawa/rulesync) — unified `.rulesync/` source, target generation과 conversion backend

## Boundary

- 이 문서는 Rule 유형의 **최적 canonical Superset과 ownership model**을 소유한다.
- 모든 Rule에 multi-target canonicalization을 강제하지 않는다.
- target-only policy를 공통분모 때문에 버리지 않는다.
- generated target Rule은 명시적 ownership migration이 없는 한 derived artifact다.
- platform/system/user authority와 target harness의 강제 규격이 이 convention보다 우선한다.
