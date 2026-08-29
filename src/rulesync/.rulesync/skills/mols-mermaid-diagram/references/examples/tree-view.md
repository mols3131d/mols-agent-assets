# TreeView

> `treeView-beta` syntax와 version-specific feature 지원은 target renderer와 Mermaid 공식 문서를 확인한다.

repository path, file/directory structure처럼 **source-backed literal hierarchy를 compact tree로 읽는 것**이 핵심이면 TreeView를 사용한다. Tree connector는 parent-child containment를 나타내며 dependency, execution order, ownership 또는 process transition을 자동으로 의미하지 않는다.

Conceptual taxonomy나 하나의 중심 개념을 분해하는 질문이면 Mindmap, import/call/generation 같은 cross-tree relationship이 핵심이면 Flowchart나 관계 table을 우선 검토한다.

## Basic: Literal Hierarchy

```mermaid
treeView-beta
    src/
        ingestion/
            api.py
            files.py
        quality/
            contracts.py
    tests/
        integration/
    pyproject.toml
```

TreeView renderer는 입력 node 위에 virtual `/` root를 둘 수 있다. 이 `/`는 renderer의 tree scaffold이며 source가 실제 filesystem root, repository root 또는 domain owner라고 자동으로 주장하지 않는다.

## Scope And Completeness

TreeView는 complete filesystem dump일 수도 있고 질문에 필요한 path만 고른 excerpt일 수도 있다. 둘을 구분하지 않으면 보이지 않는 sibling이나 상위 path가 존재하지 않는 것처럼 읽힐 수 있다.

- Complete tree인지 selected-path excerpt인지 해석에 필요하면 주변 prose에서 명시한다.
- Excerpt를 complete inventory처럼 사용해 “다른 파일이 없다”, “이 directory에는 이 child만 있다” 같은 결론을 만들지 않는다.
- 누락을 표시하려고 source에 없는 `...`, `others/` 같은 가짜 file/directory node를 추가하지 않는다. 필요하면 diagram 밖에서 생략 범위를 설명한다.
- 여러 top-level entry가 있어도 TreeView는 virtual root 아래의 forest로 표현할 수 있다. 이 공통 visual root를 source에 없는 실제 공통 parent로 승격하지 않는다.
- Visible `/`가 fragment scope를 실제 root처럼 오해하게 할 정도로 중요한 경우에는 target의 current root behavior를 확인하고, ambiguity를 제거할 수 없으면 plain tree/outline/table fallback을 우선한다.

## File And Directory Identity

Trailing `/`는 directory를 나타내는 **semantic type signal**이다. 단지 bold label이나 folder-like appearance를 얻기 위해 사용하지 않는다.

- 실제 directory에만 trailing `/`를 붙이고 file에는 붙이지 않는다.
- Parser가 허용하더라도 filesystem-like tree에서 file 아래에 child를 중첩하지 않는다. Parent가 children을 포함한다면 source도 directory/container 관계를 뒷받침해야 한다.
- 같은 filename이 서로 다른 directory에 반복되면 각 path의 별도 occurrence다. 같은 label이라는 이유로 하나의 shared entity로 합치지 않는다.
- Generic concept hierarchy를 folder/file처럼 위장하기 위해 임의의 trailing `/`를 사용하지 않는다. 그런 경우 Mindmap이나 outline이 더 직접적일 수 있다.

## Structural Input Is Semantic

TreeView hierarchy는 indentation 또는 box-drawing branch 위치에서 결정된다. Structural spacing을 단순 formatting으로 취급하지 않는다.

Indentation input은 depth별 indentation을 일관되게 유지한다.

```mermaid
treeView-beta
    docs/
        architecture/
            overview.md
        operations/
            runbook.md
```

Box-drawing input은 source tree를 그대로 읽기 좋은 경우에 사용한다.

```mermaid
treeView-beta
├── docs/
│   ├── architecture/
│   │   └── overview.md
│   └── operations/
│       └── runbook.md
└── README.md
```

- 한 diagram의 hierarchy에는 indentation 또는 box-drawing 중 하나의 structural style을 선택한다.
- Box-drawing branch의 column position이 depth 계산에 사용될 수 있으므로 branch 문자를 보기 좋게 임의 이동하지 않는다.
- 기존 source의 indentation이나 branch column을 바꿀 때 parent-child가 바뀌는 semantic edit인지 먼저 확인한다.
- 두 입력 형식이 같은 tree를 표현해야 한다면 label, node type과 parent-child가 동일한지 비교한다. 시각적 유사성만 확인하지 않는다.

## Source-Backed Annotations

`##` description, highlight와 icon은 hierarchy를 보조하는 presentation/annotation layer다. Source에 실제로 있는 responsibility, generated status나 purpose를 짧게 설명할 수 있지만 새로운 관계를 만들지는 않는다.

```mermaid
treeView-beta
├── src/ ## production code
│   ├── ingestion/ ## source adapters
│   │   ├── api.py
│   │   └── files.py
│   ├── quality/ :::highlight ## validation code
│   │   ├── contracts.py
│   │   └── reconciliation.py
│   └── publishing/ ## output adapters
├── tests/
│   └── integration/ ## cross-boundary tests
├── generated/ ## generated output; do not edit manually
│   └── schema.json
└── pyproject.toml ## project/tool configuration
```

- `:::highlight`는 **해당 row를 강조**할 뿐 subtree boundary, ownership scope, security zone 또는 critical path를 만들지 않는다.
- `##` description은 source-backed fact만 적는다. Filename이나 directory 이름만 보고 purpose, owner, generated status를 추론하지 않는다.
- Description text에 `uses X`, `generated from Y` 같은 관계를 써도 connector가 생기는 것은 아니다. 그 relationship이 load-bearing information이면 Flowchart나 companion table로 직접 표현한다.
- External icon pack이나 icon mapping은 embedding host가 실제로 지원·등록한 경우에만 사용한다. Icon이 없어도 file/directory identity와 hierarchy가 읽혀야 한다.
- Shape/color/icon/highlight 하나에 ownership, risk, state 같은 domain semantics를 맡기지 않는다.

## Order Is Not Dependency

Renderer는 declaration의 tree traversal 순서대로 row를 배치할 수 있지만 vertical order 자체는 dependency나 execution sequence가 아니다.

- Source가 directory listing order를 제공하면 필요에 따라 보존할 수 있지만 위/아래 위치를 priority, chronology, import order 또는 runtime call order로 해석하지 않는다.
- Sibling reorder가 source의 실제 hierarchy를 바꾸지 않는 presentation edit라면 가능하지만, source가 명시적 ordering을 소유하는 경우에는 그 순서를 보존한다.
- Arbitrary dependency, backlink, symlink target 또는 cross-branch relationship이 핵심이면 TreeView connector로 흉내 내지 않는다.

## Viewport And Density

TreeView는 깊이가 늘수록 indentation으로 폭이 커지고, `##` description은 긴/deep label 뒤의 공통 description column 때문에 전체 폭을 더 키울 수 있다.

- 상위 [Mermaid Diagram Reference](../mermaid-diagrams.md)의 hierarchy readability budget에 도달하면 subtree split을 다시 검토한다.
- 긴 description을 여러 row에 반복하기보다 label에는 path identity를 남기고 상세 purpose·policy는 companion prose/table로 이동한다.
- Width를 줄이기 위해 실제 intermediate directory를 삭제하거나 child를 다른 parent로 옮기지 않는다.
- Complete tree가 너무 크면 source-backed subtree나 질문별 selected paths로 나누고, excerpt임을 숨기지 않는다.
- Icon과 highlight를 늘려 density 문제를 해결하려 하지 않는다. 먼저 scope, label과 annotation 양을 줄인다.

## Renderer-Sensitive Review

TreeView는 syntax validity와 **literal hierarchy fidelity**를 따로 검증한다.

1. TreeView가 conceptual taxonomy가 아니라 path-like/literal hierarchy라는 질문에 맞는가.
1. Virtual `/`를 실제 source root나 common owner로 잘못 해석하고 있지 않은가.
1. Complete tree와 excerpt의 범위를 혼동하지 않았는가.
1. 모든 parent-child가 source-backed containment이며 file/directory type이 trailing `/`와 일치하는가.
1. File 아래 child처럼 parser가 받아들일 수 있어도 source model과 모순되는 구조가 없는가.
1. Indentation 또는 box-drawing column만 읽어도 intended depth가 명확한가.
1. Structural input style을 섞어 parent 계산을 renderer의 보정이나 우연한 parsing에 맡기지 않았는가.
1. Row order를 dependency, chronology, priority 또는 runtime order로 승격하지 않았는가.
1. Highlight, description과 icon이 hierarchy보다 강한 boundary·ownership·state를 암시하지 않는가.
1. Long/deep labels와 description column 때문에 horizontal downscaling이 필요한 경우 scope/split을 먼저 재검토했는가.
1. Beta syntax, annotations, icon integration과 root behavior가 실제 target에서 의도대로 읽히는가.

문제가 있으면 예쁜 file tree를 만들기 위해 path, type 또는 containment를 발명하지 않는다. 먼저 source scope와 representation choice를 고친다.

## Portable Fallback

Target renderer가 TreeView를 안정적으로 지원하지 않으면 **path, file/directory identity, parent-child와 필요한 annotation**을 보존하는 plain-text box tree, indented outline 또는 table로 전환한다. Dependency나 cross-link가 load-bearing information이면 Flowchart 등 해당 관계를 직접 표현하는 representation을 사용한다.
