# Swimlanes Diagram

> `swimlane-beta`는 새롭고 version-sensitive한 Mermaid type이다. 현재 syntax와 renderer 지원은 Mermaid 공식 문서와 target renderer에서 확인한다.

Process의 다음 단계뿐 아니라 **각 step을 누가/무엇이 책임지고 어디서 responsibility handoff가 일어나는지**가 핵심이면 Swimlanes를 사용한다. Ownership이 중요하지 않으면 regular Flowchart가 더 단순하고, exact message chronology가 핵심이면 Sequence Diagram이 더 직접적이다.

## Mermaid Model: Flowchart Semantics + Lane Layout

현재 Mermaid Swimlanes는 별도 relationship grammar를 만들지 않고 **Flowchart parser, DB와 renderer semantics를 재사용하면서 swimlane layout을 적용**한다.

- node와 edge syntax/identity는 Flowchart와 같은 책임을 가진다.
- top-level `subgraph`가 lane으로 렌더링된다.
- lane은 ownership/partition을 읽기 위한 layout structure지만, 실제 owner 의미는 source가 뒷받침해야 한다.
- Flowchart feature가 parsing된다는 사실만으로 Swimlane layout에서 모든 advanced presentation이 동일하게 안정적이라고 가정하지 않는다. Beta type이므로 actual target render를 확인한다.

## Basic: Ownership Handoffs

```mermaid
swimlane-beta
    subgraph customer [Customer]
        request[Request service]
        receive[Receive update]
    end

    subgraph support [Support]
        triage[Triage request]
        answer[Send answer]
    end

    subgraph engineering [Engineering]
        investigate[Investigate issue]
        fix[Prepare fix]
    end

    request -->|Request received| triage
    triage -->|Known issue| answer
    triage -->|Code change required| investigate
    investigate --> fix --> answer
    answer --> receive
```

각 node가 실제 owner lane에 있다는 전제다. Cross-lane edge는 responsibility가 바뀌는 handoff이며, artifact·message·condition이 해석에 중요하면 source-backed label로 드러낸다.

## One Partition Criterion Per Level

한 diagram의 top-level lane은 하나의 partition criterion을 사용한다.

- team 기준이면 모든 lane을 team/role ownership으로 나눈다.
- system 기준이면 모든 lane을 responsible system으로 나눈다.
- actor와 internal team, process phase, status를 같은 lane level에서 섞지 않는다.
- source에서 one step에 joint ownership이 있더라도 보기 좋은 placement를 위해 임의로 한 owner만 선택하지 않는다. Primary owner convention을 명시하거나 shared responsibility를 companion table로 보존한다.
- phase를 lane으로 사용할 수는 있지만 ownership이 핵심이 아니라면 regular Flowchart의 stage grouping이 더 직접적인지 먼저 검토한다.

## Lane Membership Is A Semantic Claim

Node를 특정 lane에 넣는 것은 그 step의 responsibility를 주장하는 것으로 읽힌다.

- layout을 맞추기 위해 node를 다른 lane으로 옮기지 않는다.
- 같은 task를 여러 lane에 복제해 shared ownership처럼 보이게 하지 않는다. Duplicate occurrence가 실제 process occurrence인지 먼저 확인한다.
- lane label은 stable owner identity를 유지하고, display wording 변경과 owner 변경을 구분한다.
- top-level subgraph가 lane이므로 nested grouping을 추가했다고 두 번째 independent ownership axis가 생긴다고 가정하지 않는다.

## Cross-Lane Handoffs

- cross-lane arrow의 existence와 direction은 실제 process/handoff에 근거해야 한다.
- 문서, approval result, ticket, event 같은 전달물이 중요한 handoff라면 edge label로 남긴다.
- 단지 다음 node가 다른 lane에 있다는 이유만으로 별도 coordination step을 발명하지 않는다.
- 같은 lane의 연속 step은 responsibility가 유지된다는 presentation이지만 조직 exclusivity나 sole accountability까지 자동으로 뜻하지 않는다.
- handoff count를 team performance metric이나 friction score로 해석하지 않는다.

## Decisions Belong Where They Are Made

Decision node는 실제 decision authority를 가진 lane에 둔다.

```mermaid
swimlane-beta
    accTitle: Data incident recovery governance
    accDescr: Operations packages evidence, engineering proposes and executes recovery, review approves risk, and audit records the outcome.

    subgraph operations [Operations]
        detect[Detect incident]
        triage[Triage impact]
        verify[Verify service recovery]
        close[Close incident]
    end

    subgraph engineering [Engineering]
        investigate[Investigate cause]
        plan[Prepare recovery plan]
        execute[Execute recovery]
        rollback[Rollback change]
    end

    subgraph review [Review]
        assess{Risk acceptable?}
        release{Recovery verified?}
    end

    subgraph audit [Audit]
        record[Record evidence and decision]
    end

    detect --> triage
    triage -->|Evidence package| investigate
    investigate --> plan
    plan -->|Recovery proposal| assess
    assess -->|Revise| investigate
    assess -->|Approved plan| execute
    execute -->|Execution result| verify
    verify -->|Healthy| release
    verify -->|Regression| rollback
    rollback -->|Rollback evidence| investigate
    release -->|Approved closure| record --> close
    release -->|More evidence required| verify
```

- decision branch label은 실제 condition/outcome을 보존한다.
- reviewer가 승인하는데 engineering lane에 diamond를 두는 식으로 ownership을 단순화하지 않는다.
- retry/revision/rollback edge는 실제 process loop일 때만 둔다.
- decision authority가 joint/conditional이라면 lane 하나로 숨기지 말고 rule/table 또는 separate approval model을 검토한다.

## Direction And Lane Order Are Presentation

`swimlane-beta` 뒤에는 `TB`, `TD`, `BT`, `LR`, `RL` direction을 지정할 수 있고 생략하면 current renderer는 `TB`를 사용한다.

- direction은 layout 선택이지 chronology를 새로 만드는 명령이 아니다. Actual order는 edge가 소유한다.
- lane의 화면상 위/아래·좌/우 순서를 organization hierarchy, priority, escalation level 또는 trust boundary로 해석하지 않는다.
- viewport를 맞추려고 edge direction이나 lane owner를 바꾸지 않는다.
- direction 변경으로 cross-lane path가 읽기 어려워지면 actual target render를 비교하고, 필요하면 process slice를 나눈다.

## Flowchart Shapes And Edge Styles

Swimlanes는 Flowchart-style node shape와 edge syntax를 사용할 수 있다.

- rectangle/circle/diamond 차이가 domain meaning을 갖는다면 source/local convention이 뒷받침해야 한다.
- dotted/thick edge를 handoff certainty, SLA 또는 severity처럼 임의 해석하지 않는다.
- stable node id를 사용하고 같은 id를 다른 task/entity에 재사용하지 않는다.
- advanced Flowchart styling/interaction이 핵심이면 beta Swimlane target에서 실제 렌더링과 trust boundary를 별도로 검증한다.

## Viewport And Density

Lane과 cross-lane handoff가 늘어날수록 arrow tracing 비용이 빠르게 커진다.

- 한 화면에서 handoff를 여러 번 되짚어야 하면 scenario, phase 또는 exception path별 split을 검토한다.
- lane 수를 줄이려고 실제 owner를 합치거나 cross-lane edge를 same-lane flow로 바꾸지 않는다.
- long process는 happy path와 exception/recovery path를 분리할 수 있지만, split 사이의 owner·handoff term을 일치시킨다.
- portrait viewport preference 때문에 lane semantics를 훼손하지 않는다. Wide ownership interaction이 본질적이면 readability를 우선한다.

## Renderer-Sensitive Review

Swimlanes는 syntax validity와 **ownership/handoff fidelity**를 따로 검증한다.

1. Ownership/responsibility가 실제로 diagram 선택의 핵심 질문인가.
1. 모든 top-level lane이 하나의 partition criterion을 일관되게 사용하는가.
1. 각 node가 실제 responsible owner/system lane에 있는가.
1. Cross-lane edge가 실제 handoff이고 source/destination이 올바른가.
1. Handoff label이 필요한 artifact·condition을 보존하는가.
1. Decision node가 실제 decision authority lane에 있고 branch condition이 source-backed인가.
1. Revision/rollback loop를 layout 때문에 발명하지 않았는가.
1. Direction과 lane screen order를 hierarchy·priority·chronology로 과해석하지 않았는가.
1. Flowchart-style shape/edge presentation을 ownership/status fact로 승격하지 않았는가.
1. Beta renderer에서 lane placement, cross-lane edge, label과 accessibility가 actual target에서 읽히는가.
1. Diagram이 너무 복잡하면 owner나 handoff를 삭제하기보다 scenario/phase별 split을 검토했는가.

문제가 있으면 lane을 재배치해 책임을 맞추지 않는다. Source ownership model과 process handoff를 먼저 고친다.

## Portable Fallback

Target renderer가 Swimlanes를 지원하지 않으면 **step order, owner/lane identity, decision authority와 cross-owner handoff**를 보존하는 grouped Flowchart 또는 ownership table로 전환한다. Exact message order가 핵심이면 Sequence Diagram을 사용한다.
