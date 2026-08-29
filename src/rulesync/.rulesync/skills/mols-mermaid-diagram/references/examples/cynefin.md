# Cynefin Diagram

> `cynefin-beta`의 현재 syntax와 renderer 지원은 Mermaid 공식 문서를 확인한다. Cynefin framework의 의미는 Mermaid 문법보다 Cynefin의 current domain model과 source context를 우선한다.

상황이 어떤 **system/context**에 놓여 있는지 sense-making하고 그에 맞는 decision approach를 선택하는 것이 핵심이면 Cynefin diagram을 사용한다. Task 종류를 영구적으로 분류하는 taxonomy나 일반 priority matrix로 사용하지 않는다.

## Basic: Contextual Sense-Making

```mermaid
cynefin-beta
    title Data Platform Decisions

    complex
        "Discover a new data product"
        "Investigate emergent user behavior"

    complicated
        "Tune distributed query performance"

    clear
        "Rotate an expired credential"
        "Run a documented backfill"

    chaotic
        "Stop active data corruption"

    confusion
        "Unclassified production anomaly"
```

이 예제의 item은 **현재 context에서의 판단**이라는 전제다. `Rotate an expired credential`이 언제나 Clear인 것이 아니며, runbook·authority·failure mode가 불명확하면 같은 label도 다른 domain일 수 있다.

## Domain Meaning Is Contextual

Mermaid는 `complex`, `complicated`, `clear`, `chaotic`, `confusion`을 fixed keyword로 제공하지만 domain assignment는 source-backed sense-making judgment다.

- **Clear**: cause/effect와 대응이 충분히 명확해 standard/best practice를 적용할 수 있는 context.
- **Complicated**: cause/effect는 알 수 있지만 expertise나 analysis가 필요한 context.
- **Complex**: pattern이 interaction을 통해 emerge하며 hindsight에서 더 잘 보이는 context.
- **Chaotic**: 즉시 안정화 action이 필요하고 아직 유효한 cause/effect relation을 전제로 할 수 없는 context.
- **Confusion**: 어느 domain인지 아직 판단하지 못했거나 source framing이 의도적으로 not-knowing 상태를 유지하는 context.

Cynefin literature에서는 central domain을 Confused/Aporetic 등 더 세밀하게 다루기도 한다. Mermaid keyword가 `confusion`이라는 이유로 framework의 용어 차이를 지우지 않는다. 그 distinction이 load-bearing하면 companion prose에서 명시한다.

## Do Not Treat Domains As Intrinsic Task Types

- 같은 activity도 constraints, knowledge, urgency와 environment가 달라지면 다른 domain에 놓일 수 있다.
- team이나 system을 통째로 `complex`, `chaotic` 같은 label로 낙인찍지 않는다. 판단 대상 context를 구체적으로 적는다.
- domain assignment가 workshop hypothesis인지, observed operating condition인지, agreed decision framing인지 필요하면 주변 설명에서 밝힌다.
- 여러 사람이 domain에 이견이 있다면 diagram 하나의 정답처럼 평균내지 않고 uncertainty 또는 competing interpretation을 드러낸다.

## Transitions Represent Domain Movement

Mermaid transition은 서로 다른 domain 사이의 movement를 표현한다.

```mermaid
cynefin-beta
    title Incident Sensemaking And Learning Loop

    complex
        "Probe unknown failure mode"
        "Run safe recovery experiments"

    complicated
        "Analyze repeated pattern"
        "Review architecture constraint"

    clear
        "Apply codified runbook"
        "Execute verified rollback"

    chaotic
        "Contain active corruption"
        "Disable unsafe publisher"

    confusion
        "Conflicting telemetry"

    confusion --> chaotic : "Impact confirmed"
    confusion --> complex : "Safe probe defined"
    chaotic --> complex : "Impact stabilized"
    complex --> complicated : "Repeatable pattern identified"
    complicated --> clear : "Runbook and guardrail verified"
    clear --> complicated : "Exception breaks the rule"
    clear --> chaotic : "Control failure causes collapse"
```

- transition label은 domain movement를 정당화하는 evidence, condition 또는 learning을 설명한다.
- Mermaid transition은 **특정 item identity를 source와 destination에 bind하지 않는다.** `Conflicting telemetry` 하나가 정확히 어느 transition을 탔는지 추적해야 하면 before/after diagram이나 companion table로 identity를 보존한다.
- transition을 workflow step, runtime dependency 또는 guaranteed lifecycle로 해석하지 않는다.
- source에 movement evidence가 없는데 “성숙하면 Complex → Complicated → Clear” 같은 선형 경로를 자동 추가하지 않는다.
- `clear --> chaotic` 같은 catastrophic movement는 실제 scenario risk를 설명할 때만 사용한다.

## Domain Placement Is Fixed Presentation

Renderer는 domain declaration order와 무관하게 domain의 위치를 고정한다.

- declaration order를 priority, maturity 또는 transition order로 해석하지 않는다.
- Complex/Complicated/Clear/Chaotic의 화면 위치 자체를 custom organizational quadrant로 재정의하지 않는다.
- boundary waviness, color와 domain area size는 framework presentation이며 item volume·risk magnitude·probability를 뜻하지 않는다.
- theme/config를 바꿔도 domain assignment와 transition meaning이 유지되어야 한다.

## Confusion And Density

Mermaid renderer의 central Confusion area는 작고 표시 가능한 item 수가 제한적이다.

- Confusion에 많은 item을 backlog처럼 쌓지 않는다. 아직 판단되지 않은 context를 빠르게 surface하고 다음 sense-making으로 넘기는 용도로 사용한다.
- 현재 renderer는 Confusion의 일부 item만 직접 보여주고 나머지를 overflow badge로 요약할 수 있으므로 item identity가 중요하면 실제 target render를 확인한다.
- 네 main domain도 long list가 overflow될 수 있다. item count를 줄이기 위해 서로 다른 context를 한 label로 합치지 말고 scenario/team/time slice별 split을 검토한다.

## Empty Domains And Completeness

Domain이 비어 있다고 해서 그 종류의 work/context가 조직에 존재하지 않는다고 결론내리지 않는다.

- diagram scope가 workshop sample인지 complete inventory인지 구분한다.
- 일부 domain만 선언해도 framework position은 고정되므로 absence를 evidence로 과해석하지 않는다.
- complete portfolio analysis가 필요하면 source table과 함께 coverage를 검증한다.

## Self-Loops And Repeated Context

Self-loop transition은 current Mermaid implementation에서 의미 없는 relation으로 취급되어 생략된다.

- domain 안에서 상태가 계속 유지된다는 사실을 self-loop arrow로 표현하지 않는다.
- 같은 domain에 머무르면서 context가 변하는 과정이 핵심이면 item label/prose 또는 별도 process representation을 사용한다.
- item의 temporal history를 Cynefin transition만으로 추적하지 않는다.

## Viewport And Renderer Review

Cynefin은 fixed framework geometry를 사용한다.

- portrait viewport를 맞추기 위해 domain geometry나 framework relation을 재배치하지 않는다.
- item label을 읽을 수 없게 축소하기보다 scope를 줄이거나 companion table을 사용한다.
- visual regression이 중요한 artifact라면 boundary/config seed 등 renderer-sensitive presentation을 target에서 확인하되, seed나 waviness를 domain fact로 취급하지 않는다.

## Renderer-Sensitive Review

Cynefin Diagram은 syntax validity와 **sense-making fidelity**를 따로 검증한다.

1. 각 item이 task의 영구 속성이 아니라 구체적인 current context를 나타내는가.
1. Domain assignment가 source-backed judgment이며 필요한 uncertainty가 드러나는가.
1. Mermaid keyword `confusion`과 source framework의 Confused/Aporetic 의미 차이를 필요 이상으로 평탄화하지 않았는가.
1. Transition이 실제 domain movement/evidence를 나타내며 workflow나 runtime edge로 과해석되지 않는가.
1. Transition을 특정 item movement처럼 보이게 하면서 item identity 근거를 잃지 않았는가.
1. Source 없이 linear maturity path나 catastrophic transition을 추가하지 않았는가.
1. Declaration/render position, color와 boundary geometry를 priority·magnitude·probability로 해석하지 않았는가.
1. Confusion overflow와 main-domain density 때문에 item identity가 숨겨지지 않는가.
1. Empty domain이나 partial diagram을 complete organizational inventory처럼 해석하지 않았는가.
1. Exact history/process가 필요한데 Cynefin framework가 그 역할을 대신하고 있지 않은가.

문제가 있으면 domain label을 억지로 확정하지 않는다. Context와 evidence를 더 좁히거나 uncertainty를 유지한 채 다른 representation을 병행한다.

## Portable Fallback

Target renderer가 Cynefin을 지원하지 않으면 **context/item, assigned domain, decision rationale, confidence/uncertainty와 domain movement evidence**를 보존하는 table을 사용한다. Exact workflow나 lifecycle이 핵심이면 Flowchart/State/Timeline 등 해당 relation을 직접 표현하는 type으로 전환한다.
