# User Journey

사용자가 목표를 완료하는 단계와 각 단계의 경험 점수, 관련 actor를 보여줄 때 `journey`를 사용한다.

## Basic: Single Actor Journey

```mermaid
journey
    title Incident review journey
    section Detect
        Receive alert: 3: Operator
        Open evidence: 4: Operator
    section Decide
        Understand impact: 2: Operator
        Approve recovery: 4: Operator
    section Resolve
        Confirm result: 5: Operator
```

## Advanced: Multiple Actors, Pain Points And Recovery

여러 actor를 사용할 때는 책임뿐 아니라 경험 저하가 발생하는 handoff와 회복 지점을 함께 보여준다. score는 정밀 KPI가 아니라 상대적 경험 신호다.

```mermaid
journey
    title Governed data access journey
    section Request
        Describe business need: 4: Analyst
        Classify requested data: 2: Analyst, Steward
        Correct missing context: 1: Analyst, Steward
    section Risk Review
        Check sensitivity: 3: Steward, Security
        Resolve policy exception: 1: Analyst, Security
        Approve conditions: 4: Security
    section Provision
        Create scoped role: 3: Platform
        Verify least privilege: 2: Platform, Security
        Deliver access guide: 4: Platform, Analyst
    section Use And Recover
        Run first query: 5: Analyst
        Report denied field: 2: Analyst, Steward
        Adjust approved scope: 4: Steward, Platform
        Confirm usable access: 5: Analyst, Platform
```

이 예시는 네 단계, 네 actor, low-score pain point, policy exception과 recovery loop를 결합한다.

## Rules

- score는 정밀 metric이 아니라 경험의 상대적 신호다.
- system call 순서를 설명하려면 sequence diagram을 사용한다.
- 실제 정량 만족도 비교가 목적이면 chart와 source table을 사용한다.
