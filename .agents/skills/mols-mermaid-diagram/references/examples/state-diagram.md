# State Diagram

incident나 workflow가 어떤 상태를 거쳐 이동하는지 보여줄 때 `stateDiagram-v2`를 사용한다.

```mermaid
stateDiagram-v2
    [*] --> Detected
    Detected --> Investigating
    Investigating --> Mitigated: risk reduced
    Investigating --> Escalated: evidence missing
    Mitigated --> Resolved
    Resolved --> [*]
```

## Advanced: Choice, Fork And Concurrent Regions

```mermaid
stateDiagram-v2
    state evidence_check <<choice>>
    [*] --> Received
    Received --> evidence_check
    evidence_check --> Rejected: incomplete
    evidence_check --> Approved: complete

    state Approved {
        [*] --> Execute
        state Execute <<fork>>
        Execute --> Backfill
        Execute --> Audit
        Backfill --> Join
        Audit --> Join
        state Join <<join>>
        Join --> Verified
    }

    Rejected --> [*]
    Approved --> [*]
```

## Splitting A Large State Diagram Package

큰 state diagram은 상태를 임의로 반으로 자르지 않고, 같은 수준의 lifecycle 책임을 가진 네 상태 영역을 package로 분리한다.

### Before: Four Equal Areas In One Diagram

네 영역의 상태와 전체 전이를 한 diagram에서 먼저 보여준다.

```mermaid
stateDiagram-v2
    state Source {
        [*] --> Received
        Received --> Registered
    }
    state Transform {
        [*] --> Normalizing
        Normalizing --> Enriched
    }
    state Quality {
        [*] --> Checking
        Checking --> Approved
        Checking --> Rejected
    }
    state Delivery {
        [*] --> Packaging
        Packaging --> Published
    }

    Registered --> Normalizing
    Enriched --> Checking
    Approved --> Packaging
    Rejected --> Normalizing
```

### After: Overview

네 영역 사이의 주요 상태 전이만 overview로 남긴다.

```mermaid
stateDiagram-v2
    [*] --> Source
    Source --> Transform
    Transform --> Quality
    Quality --> Delivery: approved
    Quality --> Transform: rejected
    Delivery --> [*]
```

### After: Four Detail Diagrams

overview의 네 영역을 각각 하나의 detail state diagram으로 확장한다. 영역을 합치거나 lifecycle의 중간 상태를 임의로 잘라내지 않는다.

#### Source Detail

```mermaid
stateDiagram-v2
    [*] --> Received
    Received --> Registered
    Registered --> [*]
```

#### Transform Detail

```mermaid
stateDiagram-v2
    [*] --> Normalizing
    Normalizing --> Enriched
    Enriched --> [*]
```

#### Quality Detail

```mermaid
stateDiagram-v2
    [*] --> Checking
    Checking --> Approved: checks pass
    Checking --> Rejected: checks fail
    Approved --> [*]
    Rejected --> [*]
```

#### Delivery Detail

```mermaid
stateDiagram-v2
    [*] --> Packaging
    Packaging --> Published
    Published --> [*]
```
