# Sequence Diagram

participant가 누구에게 어떤 message를 보내는지가 핵심이면 `sequenceDiagram`을 사용한다.

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Store

    User->>API: Submit request
    API->>Store: Save request
    Store-->>API: Request ID
    API-->>User: Accepted
```

## Advanced: Loop, Parallel Work And Critical Section

```mermaid
sequenceDiagram
    autonumber
    actor Operator
    participant API
    participant Validator
    participant Store

    Operator->>API: Start validation
    par Load contract
        API->>Store: Read contract
        Store-->>API: Contract
    and Scan dataset
        API->>Validator: Profile dataset
        Validator-->>API: Profile
    end

    loop Each rule
        API->>Validator: Evaluate rule
        Validator-->>API: Finding
    end

    critical Publish evidence
        API->>Store: Save report
    option Store unavailable
        API-->>Operator: Retry later
    end
    API-->>Operator: Validation complete
```

## Intermediate: Custom Sequence Numbering

Mermaid 11.15.0 이상에서는 `autonumber <start> <increment>`로 시작값과 증가값을 지정할 수 있다. 번호는 설명 순서를 보조할 때만 사용한다.

```mermaid
sequenceDiagram
    autonumber 10 0.5
    participant Client
    participant API
    participant Worker

    Client->>API: Submit job
    API->>Worker: Start processing
    Worker-->>API: Processing result
    API-->>Client: Return status
```

문서 본문에서 message를 번호로 참조한다면 source 변경 후 번호가 바뀌지 않았는지 다시 검토한다.

## Splitting A Large Sequence Diagram Package

큰 sequence diagram은 participant와 message를 임의로 반으로 자르지 않고, 같은 수준의 책임을 가진 네 participant 영역을 package로 분리한다.

### Before: Four Equal Areas In One Diagram

네 영역의 주요 participant와 전체 handoff를 한 diagram에서 먼저 보여준다.

```mermaid
sequenceDiagram
    participant Source
    participant Transform
    participant Quality
    participant Delivery

    Source->>Transform: Send input
    Transform->>Quality: Send transformed data
    Quality->>Quality: Run checks
    alt Checks pass
        Quality->>Delivery: Release approved data
        Delivery-->>Source: Confirm delivery
    else Checks fail
        Quality-->>Transform: Request correction
        Transform-->>Source: Request revised input
    end
```

### After: Overview

네 영역 사이의 주요 message만 overview로 남긴다.

```mermaid
sequenceDiagram
    participant Source
    participant Transform
    participant Quality
    participant Delivery

    Source->>Transform: Input
    Transform->>Quality: Transformed data
    Quality->>Delivery: Approved data
```

### After: Four Detail Diagrams

overview의 네 영역을 각각 하나의 detail diagram으로 확장한다. participant 영역을 합치거나 하나의 message 흐름을 임의로 끊지 않는다.

#### Source Detail

```mermaid
sequenceDiagram
    participant Source
    participant InputStore

    Source->>InputStore: Write input
    InputStore-->>Source: Input accepted
```

#### Transform Detail

```mermaid
sequenceDiagram
    participant Transform
    participant InputStore
    participant ModelStore

    Transform->>InputStore: Read input
    InputStore-->>Transform: Return records
    Transform->>ModelStore: Write transformed data
    ModelStore-->>Transform: Model accepted
```

#### Quality Detail

```mermaid
sequenceDiagram
    participant Quality
    participant ModelStore
    participant IssueLog

    Quality->>ModelStore: Read transformed data
    ModelStore-->>Quality: Return records
    Quality->>Quality: Run checks
    Quality->>IssueLog: Record failures
```

#### Delivery Detail

```mermaid
sequenceDiagram
    participant Delivery
    participant Quality
    participant OutputStore

    Delivery->>Quality: Request approved data
    Quality-->>Delivery: Return approved data
    Delivery->>OutputStore: Publish data
    OutputStore-->>Delivery: Delivery confirmed
```
