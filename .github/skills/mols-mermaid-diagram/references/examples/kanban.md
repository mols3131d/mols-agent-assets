# Kanban

workflow stage별 현재 작업 상태가 핵심이면 `kanban`을 사용한다. 시간 흐름이나 dependency 계획은 Gantt가 더 적합하다.

## Basic: Workflow Columns

```mermaid
kanban
    backlog[Backlog]
        contract[Define data contract]
        baseline[Create baseline]
    active[In progress]
        checks[Implement checks]
    done[Done]
        inventory[Inventory sources]
```

## Advanced: Governed Snapshot With Ownership And Review Queue

Advanced board는 ticket link, owner, priority와 review stage를 결합한다. 여러 item을 넣어 WIP concentration과 review queue를 읽을 수 있게 하되 dependency planning으로 사용하지 않는다.

```mermaid
---
config:
  kanban:
    ticketBaseUrl: 'https://tracker.example/items/#TICKET#'
---
kanban
    ready[Ready]
        contract[Define data contract]@{ ticket: DE-101, assigned: 'Data Steward', priority: 'High' }
        recovery[Document recovery flow]@{ ticket: DE-102, assigned: 'Platform', priority: 'Very High' }
    active[In progress]
        checks[Implement contract checks]@{ ticket: DE-103, assigned: 'Data Engineering', priority: 'Very High' }
        evidence[Collect failure evidence]@{ ticket: DE-104, assigned: 'Operations', priority: 'High' }
    review[Review]
        coverage[Validate check coverage]@{ ticket: DE-105, assigned: 'QA', priority: 'High' }
        security[Approve recovery boundary]@{ ticket: DE-106, assigned: 'Security', priority: 'Very High' }
    done[Done]
        inventory[Inventory sources]@{ ticket: DE-099, assigned: 'Data Engineering', priority: 'Low' }
        ownership[Confirm source owners]@{ ticket: DE-100, assigned: 'Data Steward', priority: 'Low' }
```

이 예시는 four-stage snapshot, cross-functional ownership, ticket traceability, priority와 review queue를 결합한다. snapshot timestamp는 diagram 밖에 명시한다.

## Rules

- column ID와 task ID는 unique하게 유지한다.
- priority 허용값은 renderer 문서와 일치시킨다.
- board가 실제 상태와 동기화되지 않으면 snapshot 시점을 명시한다.
