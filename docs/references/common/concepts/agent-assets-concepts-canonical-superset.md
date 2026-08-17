---
title: Canonical Superset Agent Assets
description: Agent Asset 유형에 공통되는 canonical superset과 target projection 관계
---

# Canonical Superset Agent Assets

**Canonical Superset**은 같은 Agent Asset을 여러 target harness에 배포할 때 지원 대상 전체의 의도된 의미를 보존하는 source authority다.

Superset은 새 Agent Asset 유형도, 모든 target의 최소 공통분모도 아니다. Rule, Skill, Prompt, Agent 각각은 자기 유형에 맞는 최적 Superset을 별도로 정의한다.

```text
canonical superset
├─ shared semantics
├─ target-scoped semantics
└─ compatibility boundaries
        ↓
   target projections
```

## Common Doctrine

- **One authority** — 관리 대상 의미의 canonical authority는 하나만 둔다.
- **Full intent** — target 차이를 삭제해 공통분모로 축소하지 않는다.
- **Native projection** — target payload는 해당 harness의 native schema와 idiom에 맞춘다.
- **Visible loss** — unsupported, omitted, approximated semantics를 숨기지 않는다.
- **Derived output** — generated projection은 명시적 ownership migration이 없는 한 source authority가 아니다.
- **Target validation** — projection은 실제 target contract에 대해 검증한다.

Canonical source와 target projection에 필요한 의미가 함께 존재하는 것 자체는 DRY 위반이 아니다. 문제는 같은 의미가 여러 독립 authority로 갈라져 서로 다르게 진화하는 경우다.

## Delivery Route

여러 target을 지원해도 항상 별도 projection을 만들지는 않는다.

1. **Direct reuse** — target이 canonical source를 그대로 소비할 수 있으면 재사용한다.
1. **Canonical fan-out** — target-native payload가 필요하면 Superset에서 projection한다.
1. **Native bridge** — 이미 native asset이 authoritative하면 source를 유지한 채 다른 target으로 bridge한다.

## Type-Specific Supersets

각 유형 문서가 실제 Superset format, ownership과 projection boundary를 소유한다.

- [Rule Canonical Superset](../../rules/agent-assets-rules-canonical-superset.md)
- [Skill Canonical Superset](../../skills/agent-assets-skills-canonical-superset.md)
- [Prompt Canonical Superset](../../prompts/agent-assets-prompts-canonical-superset.md)
- [Agent Canonical Superset](../../agents/agent-assets-agents-canonical-superset.md)

## Boundary

이 문서는 네 유형에 공통되는 개념만 소유한다. 유형별 source format, field, package surface, placement와 vendor-specific capability는 각 유형 reference와 target의 공식 contract가 소유한다.

Superset은 여러 target을 실제로 관리할 가치가 있을 때 사용한다. 하나의 target만 필요한 자산에 불필요한 canonical layer나 sibling projection을 만들지 않는다.
