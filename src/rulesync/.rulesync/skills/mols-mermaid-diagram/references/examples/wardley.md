# Wardley Map

> `wardley-beta`의 현재 syntax와 target renderer 지원은 Mermaid 공식 문서에서 확인한다. Wardley Mapping 자체의 의미는 Mermaid 문법보다 Wardley Mapping의 domain model을 우선한다.

**누구를 위해 어떤 need를 충족하고, 그 value chain의 capability가 서로 어떻게 의존하며, 각 capability가 evolution axis 어디에 있는가**를 함께 분석하는 것이 핵심이면 Wardley Map을 사용한다. Runtime architecture, generic dependency graph, project roadmap 또는 임의의 2D positioning chart로 사용하지 않는다.

## Basic: Value Chain And Evolution

```mermaid
wardley-beta
    title Data Product Value Chain

    anchor Analyst [0.95, 0.90]
    component Trusted Dataset [0.82, 0.72]
    component Transformation [0.62, 0.55]
    component Source Data [0.42, 0.80]
    component Compute [0.20, 0.92]

    Analyst -> Trusted Dataset
    Trusted Dataset -> Transformation
    Transformation -> Source Data
    Transformation -> Compute
```

이 예제는 source-backed strategic model이 Analyst를 anchor로 두고, 아래 capability가 위 capability를 실현하는 dependency chain을 가진다는 전제다. Edge를 runtime call, network connection 또는 execution order로 읽지 않는다.

## Coordinate Semantics

Mermaid Wardley coordinate는 일반적인 `(x, y)`가 아니라 **`[visibility, evolution]`** 순서다.

- 첫 값 `visibility`: `0.0–1.0`, 아래에서 위로 갈수록 user/value-chain에서 더 visible하다.
- 둘째 값 `evolution`: `0.0–1.0`, 왼쪽에서 오른쪽으로 갈수록 더 evolved/industrialised한 위치다.
- `0.62`, `0.55` 같은 숫자는 정밀 측정값처럼 보이기 쉽지만, Wardley position이 judgment/model estimate라면 그 불확실성을 숨기지 않는다.
- viewport를 맞추거나 label overlap을 피하려고 component coordinate를 이동하지 않는다. Label offset이나 canvas composition을 먼저 조정한다.
- vertical order를 조직 seniority, runtime layer, priority 또는 cost로 해석하지 않는다.
- horizontal position을 delivery progress, calendar time 또는 product maturity percentage로 해석하지 않는다.

## Value-Chain Dependencies

Wardley Map의 value chain은 user/need와 capability를 **dependency relationship**으로 연결한다.

- 위 component가 아래 component에 의존해 user need를 실현한다는 model이 있을 때 link를 둔다.
- architecture에서 `A calls B`, `A deploys on B`, `A sends event to B`라는 사실만으로 Wardley dependency를 자동 생성하지 않는다.
- edge direction을 보기 좋은 layout용 화살표로 바꾸지 않는다. Dependency meaning이 불명확하면 먼저 source model을 정리한다.
- 같은 component name을 다른 identity에 재사용하지 않는다. Mermaid의 internal builder는 name/id로 node를 resolve·merge하므로 stable unique identity를 유지한다.
- 여러 map에서 같은 capability를 비교할 때 이름만 같고 scope가 다른 entity를 하나의 identity처럼 취급하지 않는다.

## Position Is A Strategic Model, Not A Fact Table

Wardley Map은 landscape에 대한 model이다.

- visibility와 evolution의 근거가 interview, workshop judgment, market evidence 또는 explicit scenario 중 무엇인지 해석에 중요하면 companion prose에서 밝힌다.
- 서로 다른 시점이나 scenario의 좌표를 한 map에 현재 사실처럼 섞지 않는다.
- disagreement가 중요한 경우 평균 좌표 하나로 숨기기보다 competing map/scenario 또는 annotation으로 드러낸다.
- exact quantitative comparison이 필요한 경우 좌표를 metric처럼 사용하지 말고 source table/chart를 함께 둔다.

## Evolution And Strategic Decorators

`evolve`, sourcing decorator와 `inertia`는 현재 topology보다 강한 strategic claim이다.

```mermaid
wardley-beta
    title Reliability Platform Strategy

    anchor Operator [0.94, 0.90]
    component Incident Console [0.82, 0.68] (build)
    component Detection Engine [0.68, 0.52] (build)
    component Metadata Catalog [0.55, 0.74] (buy)
    component Compute Platform [0.25, 0.94] (market)
    component Legacy Scheduler [0.48, 0.38] (inertia)

    Operator -> Incident Console
    Incident Console -> Detection Engine
    Detection Engine -> Metadata Catalog
    Detection Engine -> Compute Platform
    Detection Engine -> Legacy Scheduler

    evolve Detection Engine 0.70
    evolve Legacy Scheduler 0.62
    note "Replace bespoke scheduling dependency" [0.42, 0.48]
```

- `evolve Component N`은 해당 component의 **target evolution position**을 나타내는 trend다. 완료일, delivery milestone 또는 확정 roadmap promise를 뜻하지 않는다.
- `evolve`가 future hypothesis인지 approved strategic intent인지 source에 맞게 설명한다.
- `(build)`, `(buy)`, `(outsource)`, `(market)`은 source-backed sourcing strategy일 때만 사용한다. 현재 procurement status와 future recommendation을 같은 표식으로 섞지 않는다.
- `(inertia)`는 change resistance에 대한 strategic observation이다. 단지 오래된 system이라는 이유로 자동 부여하지 않는다.
- note와 annotation은 reasoning을 보조하지만 component position이나 relationship을 대신하지 않는다.

## Pipelines And Evolution Stages

Pipeline은 같은 value-chain visibility를 공유하면서 evolution position이 다른 related component를 표현할 때 유용하다.

- arbitrary peer group을 한 줄로 정렬하려는 layout trick으로 사용하지 않는다.
- pipeline child의 shared visibility가 실제 strategic model에 맞는지 확인한다.
- custom evolution stage label/boundary는 map의 해석 기준 자체를 바꾼다. 단순 미관이나 viewport 때문에 canonical/current source axis를 바꾸지 않는다.
- 서로 다른 activity/practice/data/knowledge evolution vocabulary를 하나의 label set으로 평탄화하면 meaning이 손실되는지 확인한다.

## Scenario Discipline

Current landscape와 proposed move를 구분한다.

- 현재 위치, predicted movement와 sourcing decision을 하나의 확정 사실처럼 섞지 않는다.
- as-is와 to-be가 모두 중요하면 별도 map 또는 명확한 scenario annotation을 사용한다.
- `evolve` arrow가 있다고 해서 해당 evolution이 반드시 일어나거나 일정 안에 완료된다고 주장하지 않는다.
- accelerator/deaccelerator 같은 advanced marker를 쓰는 경우에도 실제 source strategic hypothesis가 있을 때만 사용한다.

## Viewport And Labels

Wardley Map은 2차원 position 자체가 load-bearing information이므로 portrait preference보다 coordinate fidelity가 우선한다.

- canvas를 좁히기 위해 coordinate를 재배치하지 않는다.
- label collision은 label offset, shorter display label, note 분리 또는 larger readable canvas로 해결한다.
- custom `size`는 target artifact가 명시적 canvas를 요구하거나 readability가 실제로 개선될 때만 사용한다.
- component가 너무 많아 dependency와 position을 동시에 읽기 어렵다면 user need/scenario별 map split을 검토한다.

## Renderer-Sensitive Review

Wardley Map은 syntax validity와 **landscape-model fidelity**를 따로 검증한다.

1. Map이 실제 user/need anchor와 capability value chain을 설명하는가.
1. 모든 component identity가 stable·unique하고 link가 의도한 component를 resolve하는가.
1. 모든 link가 runtime connectivity가 아니라 source-backed value-chain dependency인가.
1. 모든 coordinate를 `[visibility, evolution]` 순서로 해석했는가.
1. Visibility와 evolution position의 evidence/assumption basis가 필요한 수준으로 드러나는가.
1. `evolve`를 date, schedule 또는 guaranteed outcome으로 오해하지 않았는가.
1. Sourcing decorator와 inertia가 실제 strategic observation/decision에 근거하는가.
1. Pipeline의 shared visibility와 custom evolution stage가 실제 model semantics를 보존하는가.
1. Layout/viewport를 맞추려고 coordinate를 움직이지 않았는가.
1. Current landscape와 future scenario가 구분되는가.
1. 너무 복잡하면 dependency를 삭제하거나 좌표를 왜곡하기보다 map scope를 좁혔는가.

문제가 있으면 좌표를 미세 조정해 그럴듯한 map을 만들지 않는다. User/need, dependency와 evolution reasoning을 먼저 고친다.

## Portable Fallback

Target renderer가 Wardley를 지원하지 않으면 **anchor/user need, capability identity, value-chain dependency, visibility/evolution position, sourcing/inertia와 scenario status**를 보존하는 table을 사용한다. Positioning 자체가 핵심이면 static map artifact 또는 Wardley-native tool을 검토하고, runtime topology가 핵심이면 Architecture/C4/Flowchart로 전환한다.
