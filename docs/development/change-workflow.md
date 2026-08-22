# Change Workflow

이 문서는 repository-local change workflow에서 **branch naming과 작업 순서**만 정의합니다.

## Branch Naming

기본 branch 이름:

```text
<owner>/<type>/<topic>
```

Branch 사용 규칙은 [`AGENTS.md`](../../AGENTS.md)가 소유합니다. Repository-local rule이나 explicit user instruction이 있으면 그것이 우선합니다.

## Flow

1. [Source Authority](source-authority.md)에 따라 변경할 canonical source를 식별합니다.
1. 해당 source를 수정합니다.
1. 검증 범위와 evidence 수준은 [Testing](testing.md)을 따릅니다.
1. 작업 중 non-canonical artifact가 필요하면 [Knowledge Lifecycle](../document/knowledge-lifecycle.md)을 따릅니다.
