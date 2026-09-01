# Tree Structures

파일, module, section과 ownership처럼 각 항목이 하나의 parent를 가진 hierarchy에 사용한다.

```text
pipeline/
├── extract/
│   ├── api.py
│   └── database.py
├── transform/
│   └── clean.py
└── load/
    └── warehouse.py
```

- root와 ordering 기준을 명확히 한다.
- `├──`, `└──`, `│`를 일관되게 사용한다.
- 기본 depth는 4단계 이하로 유지한다.
- 큰 구조는 핵심 branch만 보여주고 생략 범위를 표시한다.
- 실제 hierarchy와 이름을 보기 좋게 만들려고 재배치하지 않는다.
- 긴 설명은 tree 밖의 list나 table로 분리한다.

여러 parent를 가진 DAG, dependency와 runtime flow는 이 표현의 범위를 벗어난다. 대안 선택은 [Visual Routing](markdown.md#visual-routing)을 따른다.
항목별 속성 비교는 table을 사용한다.
