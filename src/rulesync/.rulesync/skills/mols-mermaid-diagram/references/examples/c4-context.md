# C4 Context

시스템 경계와 외부 actor·dependency가 핵심이면 C4 context diagram을 사용한다. renderer가 지원하지 않으면 flowchart나 text description으로 대체한다.

```mermaid
C4Context
    title System context
    Person(operator, "Operator", "Reviews incidents")
    System(pipeline, "Data Pipeline", "Loads and validates data")
    System_Ext(source, "Source System", "Provides input files")

    Rel(operator, pipeline, "Reviews results")
    Rel(source, pipeline, "Sends files")
```

## Advanced: Context To Containers

context diagram이 시스템 경계와 외부 관계를 설명한다면, 다음 단계에서는 system 내부의 주요 container와 책임을 분리한다. context의 actor와 external system을 container detail에 다시 복사하지 말고, 내부 책임에 집중한다.

```mermaid
C4Container
    title Data pipeline containers
    Container_Boundary(pipeline, "Data Pipeline") {
        Container(ingest, "Ingestion", "Python", "Reads source files")
        Container(transform, "Transformation", "dbt", "Builds analytical models")
        Container(quality, "Quality Checks", "Python", "Validates contracts")
        Container(store, "Warehouse", "DuckDB", "Stores curated data")
    }

    Rel(ingest, transform, "Writes staged data")
    Rel(transform, quality, "Publishes model metadata")
    Rel(quality, store, "Approves curated data")
```

## Improvement: Explicit Boundary And Relationship Meaning

개선된 C4는 system boundary, container 책임, relationship의 방향과 message 의미를 명시한다. 단순 component 목록보다 “누가 무엇을 제공하는가”를 읽을 수 있어야 한다.

```mermaid
C4Context
    title Reliability control plane
    Person(operator, "Operator", "Reviews evidence")
    System_Boundary(control_plane, "Reliability Control Plane") {
        System(lifecycle, "Lifecycle Analysis", "Detects incidents and drafts remediation")
    }
    System_Ext(data, "Source Data", "Provides source and analytical artifacts")
    System_Ext(recovery, "Recovery API", "Runs approved backfills")

    Rel(operator, lifecycle, "Reviews incident evidence")
    Rel(data, lifecycle, "Provides read-only inputs")
    Rel(operator, recovery, "Approves and requests recovery")
    Rel(recovery, lifecycle, "Returns recovery result")
```

## Advanced: Component And Dynamic Views

C4는 여러 zoom/view를 지원할 수 있지만 exact support는 target renderer와 현재 Mermaid 문서를 확인한다. 같은 질문을 여러 view에 반복하지 않고 zoom level을 명확히 한다.

```mermaid
C4Component
    title Validation components
    Container_Boundary(quality, "Quality Service") {
        Component(api, "Validation API", "Python", "Accepts validation requests")
        Component(engine, "Rule Engine", "Python", "Evaluates data contracts")
        Component(report, "Report Builder", "Python", "Creates evidence packages")
    }
    ContainerDb(metadata, "Metadata Store", "DuckDB", "Stores contracts and results")

    Rel(api, engine, "Evaluates request")
    Rel(engine, metadata, "Reads contracts")
    Rel(engine, report, "Sends findings")
```

```mermaid
C4Dynamic
    title Validation request sequence
    Person(operator, "Operator")
    Container(api, "Validation API", "Python")
    Container(engine, "Rule Engine", "Python")
    ContainerDb(metadata, "Metadata Store", "DuckDB")

    RelIndex(1, operator, api, "Requests validation")
    RelIndex(2, api, engine, "Evaluates dataset")
    RelIndex(3, engine, metadata, "Loads contract")
    RelIndex(4, api, operator, "Returns report")
```

## Advanced: Deployment View

C4 Deployment는 container가 실제 execution environment에 어떻게 배치되는지 보여준다. logical container diagram과 deployment topology를 한 view에 섞지 않는다.

```mermaid
C4Deployment
    title Data platform deployment

    Deployment_Node(client, "Operator workstation", "Web browser") {
        Container(ui, "Operations UI", "Browser", "Reviews incidents")
    }

    Deployment_Node(cloud, "Cloud environment", "Managed platform") {
        Deployment_Node(apps, "Application cluster", "Containers") {
            Container(api, "Reliability API", "Python", "Serves lifecycle operations")
            Container(worker, "Recovery Worker", "Python", "Runs approved backfills")
        }
        Deployment_Node(data, "Data services", "Managed storage") {
            ContainerDb(store, "Evidence Store", "Database", "Stores reports and decisions")
        }
    }

    Rel(ui, api, "Uses", "HTTPS")
    Rel(api, store, "Reads and writes", "SQL")
    Rel(api, worker, "Dispatches approved work")
    Rel(worker, store, "Records result", "SQL")
```

C4 support는 target-dependent하다. 실제 render를 확인하지 못했다면 support를 단정하지 않고, portable 문서에는 architecture, flowchart 또는 text fallback을 제공한다.
