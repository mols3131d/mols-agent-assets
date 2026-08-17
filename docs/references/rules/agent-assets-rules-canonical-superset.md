---
title: Rule Canonical Superset
description: 여러 coding-agent harness에 투영할 Rule의 repository-local canonical superset 기준
---

# Rule Canonical Superset

여러 coding-agent harness에 같은 Rule을 배포해야 할 때의 권장 Superset은 **하나의 authoritative Rule source에서 target-native Rule을 fan-out할 수 있는 canonical source model**이다.

이 저장소에서 변환 backend를 사용할 때는 Rulesync의 canonical source surface를 우선 후보로 본다. GitHub Copilot, Google Antigravity 등은 canonical policy의 target projection이 된다.

```text
canonical Rule source
├─ shared policy semantics
├─ target-scoped policy semantics
└─ scope / applicability intent
        ↓
   target-native Rules
```

## Superset Owns

- 공통 policy와 constraint
- Rule의 적용 의도와 scope semantics
- target마다 실제로 달라져야 하는 target-scoped semantics
- projection에서 보존해야 할 authority와 precedence boundary
- 표현 불가능하거나 근사가 필요한 의미의 compatibility expectation

Target별 filename, directory, selector syntax, metadata와 harness-native encoding은 Superset의 본질이 아니라 projection concern이다.

## Preferred Route

1. Target이 authoritative source를 직접 소비할 수 있으면 direct reuse한다.
1. Canonical source가 authoritative하고 native payload가 필요하면 fan-out한다.
1. 이미 한 harness의 native Rule이 authoritative하면 source를 유지한 채 필요한 target으로 bridge한다.

단순 bridge를 위해 source authority를 `.rulesync/`로 옮기지 않는다. Canonicalization 자체가 의도된 경우에만 ownership을 변경한다.

## Target Projection

예:

```text
Rule Superset
├─ GitHub Copilot Rule
└─ Google Antigravity Rule
```

Projection은 target의 실제 Rule contract에 맞춰 format, placement, selector와 지원 semantics를 조정한다. 생성 성공을 semantic parity로 보지 않는다.

Rule의 directory/glob/chatbot 배치 규칙은 [Rule Projections](agent-assets-rules-projections.md)가 소유한다.

Rulesync 기반 source resolution, preview, generation, bridge와 validation 실행 계약은 [`rulesync-agent-assets`](../../../src/skills/rulesync-agent-assets/SKILL.md)가 소유한다. 설치된 Rulesync version의 실제 target/feature 지원이 runtime authority다.

## Boundary

- 이 문서는 Rule 유형의 **최적 canonical Superset과 ownership model**을 소유한다.
- 모든 Rule에 multi-target canonicalization을 강제하지 않는다.
- target-only policy를 공통분모 때문에 버리지 않는다.
- generated target Rule은 명시적 ownership migration이 없는 한 derived artifact다.
- platform/system/user authority와 target harness의 강제 규격이 이 convention보다 우선한다.
