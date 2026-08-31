---
description: README의 inline Index와 generated INDEX.tsv 중 적절한 문서 인덱싱 방식을 선택하는 원칙을 확인할 때 사용합니다.
---

# Document Indexing

문서 인덱스는 **탐색을 실제로 개선할 때만** 둡니다. 별도 authored index 전용 파일은 만들지 않습니다.

## Principles

| 필요 | 선택 |
| --- | --- |
| 파일명과 search만으로 충분함 | 별도 index 없음 |
| 사람이 목적·차이·선택 기준을 함께 봐야 함 | `README.md`의 `Index` section |
| 재생성 가능한 inventory가 필요함 | `INDEX.tsv` |

- README의 `Index`는 사람의 판단을 돕는 curated navigation에 사용합니다.
- `INDEX.tsv`는 source에서 다시 만들 수 있는 generated inventory에 사용합니다.
- 두 surface를 함께 사용하더라도 같은 정보를 반복하지 않습니다.
- README의 entrypoint 역할을 흐릴 만큼 index가 커지면, 사람에게 필요한 선택 기준만 README에 남기고 재생성 가능한 정보는 generated index에 맡깁니다.
- Index는 원본이나 authority를 대신하지 않습니다. 의미와 metadata의 정본은 해당 source가 소유합니다.
