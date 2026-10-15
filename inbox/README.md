# Inbox

`inbox/`는 조사·계획·검토·인계 등 **정본으로 확정되지 않은 작업 아티팩트**를 보관하는 플랫폼 독립적인 공간입니다.

## 경로

작업을 식별하기 쉬운 기준으로 아티팩트를 묶습니다. 별도 식별자가 없으면 날짜를 기본으로 사용합니다.

| 기준 | 경로 |
| --- | --- |
| 날짜 (기본값) | `inbox/YYYY-MM-DD/<artifact>` |
| 브랜치 | `inbox/branch-<slug>/<artifact>` |
| GitHub Issue·PR | `inbox/github-<number>/<artifact>` |

날짜는 작업 디렉터리를 처음 만든 날을 사용하며, GitHub Issue와 PR은 번호만으로 식별합니다.

아카이브 경로는 `inbox/archive/YYYY-MM-DD/<artifact-or-directory>`입니다. 날짜는 아카이브한 날을 뜻합니다.

## 번들

아티팩트는 **단일 문서** 또는 **디렉터리 번들**로 둘 수 있습니다. 디렉터리 번들에는 문서 하나만 있어도 되며, 그 안의 문서도 단일 문서 번들로 사용할 수 있습니다. **번들 내부의 추가 하위 디렉터리는 허용하지 않습니다.**

```text
inbox/github-244/
├── research.md
└── review/
    ├── findings.md
    └── evidence.md
```

정본 승격과 보존은 [Working Knowledge](../docs/documentation/README.md#working-knowledge)를 따릅니다.
