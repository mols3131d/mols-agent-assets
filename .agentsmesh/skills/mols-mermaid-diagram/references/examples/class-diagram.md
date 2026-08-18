# Class Diagram

class, interface, member와 inheritance·composition·dependency가 핵심이면 `classDiagram`을 사용한다.

```mermaid
classDiagram
    class Pipeline {
        +run() Result
        +validate() bool
    }

    class SourceReader {
        <<interface>>
        +read() Records
    }

    class CsvReader {
        +read() Records
    }

    class QualityCheck {
        +evaluate(Records) Report
    }

    SourceReader <|.. CsvReader : implements
    Pipeline *-- SourceReader : owns
    Pipeline --> QualityCheck : invokes
```

## Advanced: Generics, Multiplicity And Notes

```mermaid
classDiagram
    note "Ports isolate orchestration from storage implementations"

    class Repository~T~ {
        <<interface>>
        +save(T item)
        +findById(string id) T
    }

    class IncidentRepository {
        +save(Incident item)
        +findById(string id) Incident
    }

    class IncidentService {
        +open(Evidence evidence) Incident
        +resolve(string incidentId)
    }

    Repository~Incident~ <|.. IncidentRepository : implements
    IncidentService "1" --> "1" Repository~Incident~ : uses
    IncidentService "1" --> "0..*" Incident : manages
```

## Advanced: Labeled And Nested Namespaces

Mermaid 11.15.0 이상에서는 namespace label과 hierarchical namespace를 사용할 수 있다. package boundary가 설계 질문에 중요할 때만 사용한다.

```mermaid
classDiagram
    namespace Platform["Data Platform"] {
        namespace Quality {
            class ValidationService {
                +validate(DataSet) Report
            }
        }
        namespace Storage {
            class EvidenceRepository {
                +save(Report)
            }
        }
    }

    ValidationService --> EvidenceRepository : stores evidence
```

`hierarchicalNamespaces: false`는 기존 프로젝트가 fully-qualified namespace를 flat box로 표현하는 convention일 때만 사용한다.

## Relationship Choice

| Syntax | Meaning | Use |
| --- | --- | --- |
| `<|--` | inheritance | subtype가 base implementation을 상속한다 |
| `<|..` | realization | class가 interface를 구현한다 |
| `*--` | composition | parent가 child lifecycle을 소유한다 |
| `o--` | aggregation | 독립 lifecycle을 가진 객체를 묶는다 |
| `-->` | association | 지속적 reference나 협력 관계다 |
| `..>` | dependency | 일시적으로 사용하거나 의존한다 |

## Improvement: Model Responsibility, Not Every Field

class diagram은 source code listing이 아니다. 설계 질문과 관련된 member만 남기고, framework boilerplate와 trivial accessor는 생략한다.

```mermaid
classDiagram
    class IncidentService {
        +detect(Baseline, Current) Incident
        +propose(Incident) Remediation
    }

    class EvidenceStore {
        +loadBaseline() Baseline
        +saveIncident(Incident)
    }

    class RecoveryPort {
        <<interface>>
        +execute(Remediation) RecoveryResult
    }

    IncidentService --> EvidenceStore : reads/writes evidence
    IncidentService ..> RecoveryPort : requests approved recovery
```
