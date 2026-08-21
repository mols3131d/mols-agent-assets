# Semantic Asset Roles

에이전트 자산을 vendor spec, filename, extension 같은 **표현 형식이 아니라 의미와 책임으로 바라보고 조합하는** 패턴입니다.

핵심은 taxonomy를 만드는 것이 아니라, 서로 다른 책임을 가진 자산을 작은 의미 모듈처럼 재사용하는 데 있습니다.

## Core

자산의 표현 형식과 의미 역할은 별개의 축으로 볼 수 있습니다.

```text
representation
→ Skill / Rule / prompt / document / command / vendor-native asset / ...

semantic role
→ Knowledge / Workflow / Constraint or Control / Evaluation / ...
```

같은 semantic role을 여러 representation으로 구현할 수 있고, 같은 representation도 서로 다른 semantic role을 가질 수 있습니다.

따라서 `Skill이므로 Workflow`, `Rule이므로 Control`처럼 spec 자체를 의미 유형으로 간주하지 않습니다.

Role은 자산 안에 어떤 종류의 문장이 들어 있는지가 아니라 **그 자산이 주로 어떤 책임을 소유하고 어떤 이유로 변경되는가**를 기준으로 이해할 수 있습니다. Workflow 안에 domain 설명이 조금 있다고 해서 곧바로 Knowledge asset이 되는 것은 아닙니다.

## Typical Roles

역할은 닫힌 taxonomy가 아니라 **조합을 이해하기 위한 대표적인 의미 단위**입니다.

| Role | Typical responsibility |
| --- | --- |
| Knowledge | 작업을 이해하거나 판단하는 데 필요한 지식, 맥락, 원칙, reference |
| Workflow | 목표를 달성하기 위한 절차나 의사결정 흐름 |
| Constraint / Control | 범위, 권한, invariant, guardrail처럼 행동을 제한하거나 조정하는 의미 |
| Evaluation | 완료, 품질, acceptance, validation 같은 판단 기준 |

필요하면 다른 역할을 추가하거나 위 역할을 더 넓게 해석할 수 있습니다. 모든 자산을 반드시 하나의 role로 분류할 필요도 없습니다.

## Composition

이 패턴의 중심은 **분류보다 composition**입니다.

작은 Workflow들을 더 큰 Workflow로 엮고, 각 단계에서 필요한 Knowledge, Control, Evaluation 자산을 상황에 맞게 사용할 수 있습니다.

```text
release workflow
├─ research workflow
│  └─ product knowledge
├─ change workflow
│  ├─ implementation knowledge
│  └─ relevant control
└─ review workflow
   └─ evaluation criteria
```

큰 Workflow가 작은 Workflow와 supporting asset을 조합하는 형태가 대표적이지만, 실제 composition owner는 harness, router, entrypoint 또는 다른 orchestration asset일 수도 있습니다.

Knowledge는 여러 Workflow에서 재사용 가능한 판단 재료로 남기고, Constraint나 Evaluation은 필요한 단계에서 선택적으로 결합하는 구성이 흔히 유용합니다. 이는 고정 dependency rule이 아니라 책임과 재사용 경계를 이해하기 위한 대표적인 방향입니다.

## Module Boundaries

자산을 모듈처럼 조합하려면 형식적인 interface보다 **무엇을 기대하고 무엇을 제공하는지**가 이해 가능해야 합니다.

예를 들어 다음 정도의 semantic boundary가 도움이 될 수 있습니다.

- Knowledge — 언제 관련되고 어떤 판단 재료를 제공하는가
- Workflow — 어떤 목표를 받고 어떤 결과나 handoff를 만드는가
- Constraint / Control — 언제 적용되고 무엇을 제한하거나 조정하는가
- Evaluation — 무엇을 어떤 기준으로 판단하는가

이를 별도 schema나 공통 field로 만들 필요는 없습니다. 자연어 책임과 입력·출력 관계가 충분히 명확하다면 그것으로도 조합 가능한 경계가 될 수 있습니다.

## Conditional Use

의미 역할을 분리하면 **필요한 자산만 필요한 상황에 결합**하기 쉬워집니다.

```text
if Python task
→ use Python knowledge

if documentation task
→ use documentation knowledge

if repository mutation is needed
→ apply relevant control
```

같은 Workflow가 상황에 따라 다른 Knowledge를 사용할 수도 있고, 하나의 Knowledge를 여러 Workflow가 공유할 수도 있습니다.

실제 discovery와 loading 방식은 metadata, index, entrypoint, Skill routing 등 환경에 따라 달라질 수 있습니다. 필요한 context를 언제 로드할지는 [Progressive Context Routing](progressive-context-routing.md) 같은 별도 패턴과 조합할 수 있습니다.

## Granularity

Semantic role은 자산을 무조건 작게 쪼개기 위한 규칙이 아닙니다.

하나의 자산이 여러 책임을 자연스럽게 함께 소유할 수도 있습니다. 다만 서로 독립적으로 재사용하거나 조건부로 로드할 가치가 있는 책임이 반복해서 섞인다면 분리를 고려할 수 있습니다.

예를 들어 여러 Workflow 안에 같은 domain 지식이 반복된다면 그 지식을 별도 Knowledge asset으로 두는 편이 재사용과 context locality에 도움이 될 수 있습니다.

반대로 한 번만 쓰이는 짧은 지식을 별도 asset으로 분리해 dependency만 늘릴 필요는 없습니다.

## Representation

Semantic role을 별도 schema로 표현할 필요는 없습니다.

필요하다면 directory, filename, frontmatter, metadata, routing index, catalog 등으로 드러낼 수 있고, 구조 없이 자산의 책임만 명확히 해도 됩니다.

중요한 것은 저장 형식을 통일하는 것이 아니라 **무엇을 재사용하고 무엇이 무엇을 조합하는지 이해하기 쉬워지는가**입니다.

## Boundary

이 패턴은 에이전트 자산의 새로운 표준 type system을 정의하지 않습니다.

핵심은 **자산의 규격과 의미 역할을 분리해서 보고, 재사용 가치가 있는 의미 단위를 모듈처럼 조합하는 것**입니다.
