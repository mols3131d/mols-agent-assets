# Change Workflow

이 문서는 repository-local change workflow 중 다른 source가 소유하지 않는 최소 convention만 정의합니다.

## Branch

Normal change work는 `main`에서 직접 하지 않고 dedicated branch에서 수행합니다.

Branch 이름은 기본적으로 다음 형태를 사용합니다.

```text
<owner>/<type>/<topic>
```

Repository-local rule이나 explicit user instruction이 있으면 그것이 우선합니다.

## Flow

1. 변경할 behavior의 canonical source를 먼저 식별합니다.
1. 해당 source를 수정합니다.
1. 검증 범위와 evidence 수준은 [Testing](../testing.md)을 따릅니다.
1. 작업 중 report, review, handoff 등 non-canonical artifact가 필요하면 [`inbox/`](../../inbox/README.md)를 사용합니다.

Generated projection이나 일회성 artifact를 canonical source로 승격하지 않습니다. Source ownership이 불명확하면 [Authority Routing](authority-routing.md)에서 authority를 먼저 해소합니다.
