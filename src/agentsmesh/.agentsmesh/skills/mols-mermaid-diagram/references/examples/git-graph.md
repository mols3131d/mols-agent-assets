# Git Graph

branch, merge, release strategy의 **의도된 흐름**을 설명할 때 `gitGraph`를 사용한다. 실제 repository history를 정확히 재현하는 용도로 사용하지 않는다.

```mermaid
gitGraph
    commit id: "baseline"
    branch feature
    checkout feature
    commit id: "implement"
    commit id: "test"
    checkout main
    merge feature id: "merge feature"
    commit id: "release"
```

## Advanced: Tags, Branch Ordering And Highlighted Commits

```mermaid
gitGraph LR:
    commit id: "baseline" tag: "v1.0"
    branch develop order: 2
    checkout develop
    commit id: "schema"
    branch feature order: 3
    checkout feature
    commit id: "implementation" type: HIGHLIGHT
    checkout develop
    merge feature id: "feature merged"
    checkout main
    merge develop id: "release" tag: "v1.1"
```

## Improvement: Keep Strategy Visible

commit을 모두 복사하지 않고 branch 생성, integration, release처럼 독자가 이해해야 하는 event만 남긴다.

```mermaid
gitGraph LR:
    commit id: "main"
    branch release
    branch feature
    checkout feature
    commit id: "change"
    checkout release
    merge feature id: "candidate"
    checkout main
    merge release tag: "v1.0"
```

renderer가 `gitGraph`를 지원하지 않으면 branch policy table이나 flowchart로 대체한다.
