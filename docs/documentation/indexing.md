---
description: README의 inline Index와 generated INDEX.tsv 중 적절한 문서 인덱싱 방식을 선택할 때 사용하는 repository documentation policy입니다.
---

# Document Indexing

문서 인덱스는 **사람의 탐색을 돕거나 재생성 가능한 inventory가 필요할 때만** 둡니다. 별도 authored index 전용 파일은 만들지 않습니다.

## Choose a Surface

| 필요 | 사용 |
| --- | --- |
| 파일명과 search만으로 충분함 | 별도 index 없음 |
| 작은 scope에서 목적·선택 기준을 함께 보여줘야 함 | `README.md`의 `Index` section |
| 파일 목록과 metadata를 도구가 읽거나 재생성해야 함 | `INDEX.tsv` |

README와 `INDEX.tsv`를 함께 쓸 수 있지만 같은 정보를 복제하지 않습니다.

## README `Index`

README의 `Index` section은 작은 사람용 navigation에 사용합니다.

- 항목 수가 작고 안정적일 때 사용합니다.
- path만으로 구분하기 어려운 목적, 사용 시점이나 선택 기준을 함께 보여줍니다.
- table은 선택에 필요한 최소 column만 둡니다. 보통 `Path | Purpose` 또는 `Path | When to use`면 충분합니다.
- 단순 파일 목록이나 generated `INDEX.tsv`를 그대로 복제하지 않습니다.

Index가 README의 entrypoint 역할을 흐릴 정도로 커지면 사람이 꼭 알아야 하는 선택 기준만 README에 남기고, 재생성 가능한 inventory는 `INDEX.tsv`로 옮깁니다.

## `INDEX.tsv`

`INDEX.tsv`는 authored document가 아니라 **generated projection**입니다. 직접 수정하지 않고 source에서 다시 생성합니다.

- field는 `path`와 `description`입니다.
- document description은 해당 Markdown frontmatter에서 가져옵니다.
- directory metadata는 해당 directory의 `README.md`에서만 가져옵니다.

README와 `INDEX.tsv`가 함께 있으면 README는 사람용 selection cue를, `INDEX.tsv`는 generated inventory를 소유합니다.
