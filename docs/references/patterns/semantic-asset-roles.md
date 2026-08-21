# Semantic Asset Roles

에이전트 자산을 vendor spec, filename, extension 같은 **표현 형식이 아니라 의미와 책임으로 분류하고 조합하는** 패턴입니다.

이 패턴의 목적은 자산을 고정된 schema로 다시 분류하는 것이 아니라, 여러 자산을 작은 의미 모듈처럼 재사용하고 필요한 상황에 맞게 조합하기 쉽게 만드는 데 있습니다.

## Core

자산에는 서로 다른 두 축이 있을 수 있습니다.

```text
representation
→ Skill / Rule / prompt / document / command / vendor-native asset / ...

semantic role
→ Knowledge / Workflow / Control / Evaluation / ...
```

같은 semantic role은 여러 representation으로 구현될 수 있고, 같은 representation도 서로 다른 semantic role을 가질 수 있습니다.

따라서 `Skill이므로 Workflow`, `Rule이므로 Control`처럼 spec 자체를 의미 유형으로 간주하지 않습니다.

## Typical Roles

아래 역할은 대표적인 예시이며 닫힌 taxonomy가 아닙니다. Repository나 asset system에 필요한 의미 단위가 있으면 다른 역할을 추가할 수 있습니다.

### Knowledge

현재 작업을 이해하거나 판단하는 데 필요한 지식, 맥락, 원칙, reference를 소유합니다.

예:

- domain knowledge
- project architecture context
- coding or documentation guidance
- vendor behavior reference
- reusable decision rationale

Knowledge는 모든 작업에 항상 넣기보다 실제로 필요한 workflow나 상황에서 선택적으로 로드할 수 있습니다.

### Workflow

목표를 달성하기 위한 절차나 작업 흐름을 소유합니다.

작은 Workflow들을 더 큰 Workflow로 조합할 수 있습니다.

```text
large workflow
├─ research workflow
├─ implementation workflow
└─ review workflow
```

큰 Workflow가 모든 세부 절차를 다시 작성하기보다 작은 Workflow를 orchestration하는 식으로 재사용할 수 있습니다.

### Control

작업 범위, 권한, invariant, guardrail처럼 **어떻게 행동할 수 있는가**에 영향을 주는 의미를 소유할 수 있습니다.

실제 runtime permission과 자연어 behavioral guidance가 같은 것은 아니므로, 필요한 경우 이 둘의 authority를 구분합니다.

### Evaluation

완료 여부, 품질, acceptance, validation 같은 판단 기준을 소유할 수 있습니다.

Workflow가 evaluation logic을 매번 복제하기보다 필요한 평가 자산을 재사용할 수 있습니다.

## Composition

Semantic role로 나눈 자산은 task에 맞게 서로 조합할 수 있습니다.

예:

```text
release workflow
├─ research workflow
│  └─ load product knowledge
├─ change workflow
│  ├─ load implementation knowledge
│  └─ apply relevant control
└─ review workflow
   └─ load evaluation criteria
```

같은 Workflow도 상황에 따라 다른 Knowledge를 사용할 수 있습니다.

```text
if Python task
→ load Python knowledge

if documentation task
→ load documentation knowledge

if repository mutation is needed
→ load relevant control
```

이런 구성은 작은 Workflow를 재사용하면서도 task마다 필요한 context만 결합하기 쉽게 합니다.

## Granularity

Semantic role은 asset을 무조건 작게 쪼개기 위한 규칙이 아닙니다.

하나의 자산이 여러 의미를 자연스럽게 함께 소유할 수도 있습니다. 다만 서로 독립적으로 재사용하거나 조건부로 로드할 가치가 있는 책임이 반복해서 섞인다면 별도 모듈로 분리하는 것을 고려할 수 있습니다.

예를 들어 긴 Workflow 안에 여러 domain 지식이 복제되고 있다면, Workflow와 Knowledge를 분리해 필요한 지식만 연결하는 편이 더 재사용 가능할 수 있습니다.

## Representation

Semantic role을 표현하는 방법은 자유롭습니다.

- directory나 filename으로 구분
- frontmatter나 metadata에 role 기록
- routing index에서 분류
- 별도 catalog에서 관계 표현
- 구조 없이 문서 책임만 명확히 유지

특정 path, metadata field 또는 schema를 만들 필요는 없습니다. Semantic classification의 목적은 저장 형식을 통일하는 것이 아니라 **composition과 reuse를 위한 의미 경계를 드러내는 것**입니다.

## Relationship to Routing

Semantic role은 무엇을 선택할지 판단하는 signal로도 사용할 수 있습니다.

예를 들어 Workflow가 현재 단계에 필요한 Knowledge나 Evaluation asset을 가리키고, 실제 loading은 [Progressive Context Routing](progressive-context-routing.md) 같은 방식으로 필요한 시점에 수행할 수 있습니다.

이 패턴은 loading algorithm이나 routing format 자체를 정의하지 않습니다.

## Considerations

- 모든 자산을 하나의 role에 억지로 넣지 않습니다.
- taxonomy가 너무 세밀해져 새로운 schema 관리 작업이 되는 것을 피합니다.
- representation과 semantic role을 혼동하지 않습니다.
- 큰 자산을 분해할 때는 분류의 아름다움보다 실제 reuse, context locality, ownership 이점을 우선합니다.
- 여러 역할을 나누더라도 orchestration owner가 불명확해지지 않도록 합니다.

## Boundary

이 패턴은 에이전트 자산의 표준 type system을 정의하지 않습니다.

핵심은 **자산이 어떤 format인가보다 어떤 의미와 책임을 소유하는가를 별도 축으로 보고, 그 의미 단위를 재사용 가능한 모듈처럼 조합하는 것**입니다.
