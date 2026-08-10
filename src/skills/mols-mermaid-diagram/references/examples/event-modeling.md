# Event Modeling

> Mermaid v11.15.0+의 `eventmodeling` DSL이다.

command, event, read model과 UI가 시간 순서로 어떻게 연결되는지 보여줄 때 사용한다.

## Basic: State Change

```mermaid
eventmodeling
    tf 01 ui IncidentUI
    tf 02 cmd CreateIncident
    tf 03 evt IncidentCreated
```

## Advanced: Reset Frames, Namespaces And Read Models

```mermaid
eventmodeling
    tf 01 ui Operations.IncidentUI
    tf 02 cmd Operations.CreateIncident { source: string }
    tf 03 evt Operations.IncidentCreated

    rf 04 evt External.RecoveryCompleted
    tf 05 pcr Operations.RecoveryProcessor
    tf 06 cmd Operations.RecordRecovery
    tf 07 evt Operations.RecoveryRecorded

    rf 08 evt Operations.IncidentCreated
    rf 09 evt Operations.RecoveryRecorded
    tf 10 rmo Operations.IncidentSummary ->> 08 ->> 09
    tf 11 ui Operations.IncidentUI
```

## Rules

- timeframe 번호는 전체 timeline에서 unique하게 유지한다.
- inference를 끊어야 할 때만 `rf`/`resetframe`을 사용한다.
- UI, processor, command, read model, event의 의미를 섞지 않는다.
