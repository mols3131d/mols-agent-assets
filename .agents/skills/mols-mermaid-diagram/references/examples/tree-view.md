# TreeView

> Mermaid v11.14.0+의 `treeView-beta` 문법이다.

directory-like hierarchy, file structure와 간단한 annotation을 보여줄 때 사용한다.

## Basic: Indentation-Based Tree

```mermaid
treeView-beta
    data-platform/
        src/
            ingestion/
            quality/
        tests/
        pyproject.toml
        README.md
```

## Advanced: Ownership Boundaries, Generated Assets And Annotations

box-drawing input으로 깊은 hierarchy를 명시하고 annotation으로 responsibility와 generated boundary를 드러낸다. 중요한 path만 강조하고 모든 node에 설명을 붙이지 않는다.

```mermaid
treeView-beta
├── src/ ## production code
│   ├── ingestion/ ## source adapters
│   │   ├── api.py
│   │   └── files.py
│   ├── quality/ :::highlight ## validation boundary
│   │   ├── contracts.py
│   │   └── reconciliation.py
│   └── publishing/ ## output adapters
├── tests/
│   ├── unit/
│   └── integration/ ## cross-boundary checks
├── generated/ ## do not edit manually
│   └── schema.json
└── pyproject.toml ## dependency and tool config
```

이 예시는 hierarchy, responsibility annotations, generated-file boundary와 selective highlight를 결합한다. arbitrary dependency는 flowchart를 사용한다.

## Intermediate: Built-In File And Folder Icons

```mermaid
---
config:
  treeView:
    showIcons: true
---
treeView-beta
    data-platform/
        src/
            pipeline.py
        tests/
            test_pipeline.py
        pyproject.toml
```

## Rules

- directory는 trailing `/`를 사용한다.
- indentation과 box-drawing input을 한 diagram에서 혼용하지 않는다.
- external icon pack은 embedding host가 등록한 경우에만 사용한다.
