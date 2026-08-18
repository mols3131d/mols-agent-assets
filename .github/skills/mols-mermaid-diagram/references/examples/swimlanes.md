# Swimlanes Diagram

> Mermaid v11.16.0+의 `swimlane-beta` 문법이다. renderer 지원을 확인한다.

단계뿐 아니라 **각 단계의 책임 주체와 handoff**가 핵심이면 swimlane을 사용한다.

## Basic: Ownership Handoffs

```mermaid
swimlane-beta LR
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

## Advanced: Approval, Revision And Rollback Across Owners

결정 node는 실제 owner lane에 두고, cross-lane edge에는 전달 artifact와 조건을 표시한다. 승인, 수정 요청, 실행 실패와 rollback까지 ownership이 끊기지 않게 만든다.

```mermaid
swimlane-beta LR
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

이 예시는 네 owner, 두 decision gate, revision loop, failure recovery와 audit handoff를 결합한다.

## Rules

- lane은 team, actor, system, phase 중 **한 가지 ownership 기준**만 사용한다.
- ownership이 중요하지 않으면 일반 flowchart를 사용한다.
- message 시간 순서가 핵심이면 sequence diagram을 사용한다.
