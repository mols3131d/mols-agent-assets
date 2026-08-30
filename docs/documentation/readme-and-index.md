---
description: directory의 README.md와 generated INDEX.tsv의 역할, 생성 조건, ownership과 갱신 경계를 결정할 때 사용하는 repository documentation policy입니다.
---

# README and Generated Index

`README.md`는 directory가 실제 contract나 navigation responsibility를 소유할 때 사람이 작성하는 local entrypoint입니다. `INDEX.tsv`는 Markdown과 frontmatter에서 다시 만들 수 있는 discovery projection입니다.

둘은 서로 대체하지 않습니다. `README.md`는 의미와 책임을 설명하고, `INDEX.tsv`는 이미 존재하는 문서를 빠르게 찾게 합니다.

## Responsibility

| Surface | Responsibility |
| --- | --- |
| `README.md` | 해당 directory의 목적, 책임 경계, 필요한 navigation·maintenance rule을 설명하는 authored entrypoint |
| `INDEX.tsv` | 문서 경로와 discovery metadata를 투영하는 generated index |
| Filesystem과 search | 별도 설명이 필요 없는 단순 inventory와 파일 존재 여부 |

정책, 판단 기준이나 유지보수 지식을 `INDEX.tsv`에만 두지 않습니다. 반대로 파일 목록을 보여주기 위해 `README.md`를 만들지 않습니다.

## `README.md`

Directory-level `README.md`는 **그 directory가 설명해야 할 책임이 있을 때만** 둡니다. Directory가 존재하거나 파일이 여러 개 있다는 사실만으로 생성하지 않습니다.

다음 중 하나 이상이 실제로 필요하면 local entrypoint의 근거가 됩니다.

- child 이름만으로 복구하기 어려운 directory contract나 responsibility boundary
- 올바른 문서를 선택하려면 알아야 하는 navigation decision
- 해당 directory에서만 적용되는 maintenance 또는 recovery rule
- parent가 소유하면 scope가 너무 넓어지는 local convention

`README.md`에는 해당 directory가 직접 소유하는 내용만 둡니다.

- directory의 목적과 책임 범위
- 필요한 경우 child surface 사이의 구분과 선택 기준
- local maintenance·recovery rule
- 공통 정책을 다시 쓰지 않는 canonical document link

Sibling 파일 목록이나 쉽게 재생성되는 inventory는 복제하지 않습니다. Repository-wide documentation principle은 [`docs/documentation/`](./)의 canonical policy를 따르고, descendant의 세부 책임은 가장 가까운 local owner에게 둡니다.

### Directory metadata

`README.md`가 directory entrypoint라면 frontmatter `description`은 파일 자체보다 **그 directory를 언제 탐색해야 하는지**를 설명합니다. 이 metadata는 generated docs index의 directory row에도 사용됩니다.

현재 docs index는 directory metadata를 찾을 때 `README.md`를 먼저 보고, YAML frontmatter 자체가 없을 때만 `index.md`를 fallback으로 사용합니다. 앞선 entrypoint에 frontmatter가 있으면 뒤 entrypoint와 field를 합치지 않습니다.

빈 index description을 채우기 위한 이유만으로 `README.md`를 만들지 않습니다. Local owner가 필요하지 않은 directory는 entrypoint 없이 존재할 수 있습니다.

Frontmatter의 세부 contract는 [Frontmatter](frontmatter.md)가 소유합니다.

## `INDEX.tsv`

`INDEX.tsv`는 source document가 아니라 **generated projection**입니다. Row를 직접 추가하거나 수정하지 않고 source Markdown, frontmatter 또는 generator policy를 고친 뒤 다시 생성합니다.

Repository의 docs index는 현재 다음 contract를 사용합니다.

- canonical wrapper는 [`scripts/generate_docs_indexes.py`](../../scripts/generate_docs_indexes.py)입니다.
- 기본 materialization depth는 `0`이므로 `docs/INDEX.tsv`만 생성합니다.
- 그 index는 기본적으로 전체 `docs/` subtree를 재귀적으로 포함합니다.
- field는 `path`와 `description`입니다.
- document row의 `description`은 해당 Markdown frontmatter에서 가져옵니다.
- directory row의 metadata는 ordered entrypoint인 `README.md`, `index.md`에서 가져옵니다.
- entrypoint 문서 자체는 별도 row로 중복하지 않습니다.
- generated index, `AGENTS.md`, systemic·hidden Markdown과 문서가 없는 subtree는 generator의 selection rule에 따라 제외합니다.

따라서 새 nested directory가 생겼다는 이유만으로 그 안에 `INDEX.tsv`를 수동으로 추가하지 않습니다. 더 깊은 위치에 index materialization이 필요하다면 개별 파일을 추가하는 대신 generator policy와 그 필요성을 함께 변경합니다.

다른 route, catalog 또는 generated index는 이 문서의 `INDEX.tsv` contract를 자동으로 상속하지 않습니다. 해당 surface의 canonical owner와 generator를 따릅니다.

## Maintenance

문서 변경 시 source와 projection의 순서를 지킵니다.

1. Markdown, `README.md` 또는 frontmatter의 authored source를 수정합니다.
1. `mise run generated-sync`로 generated projection을 갱신합니다.
1. `INDEX.tsv` diff가 source 변경의 예상 결과인지 검토합니다.
1. 필요한 repository check를 실행하고, 실행하지 않은 검증을 통과했다고 기록하지 않습니다.

Committed docs index drift를 별도로 확인해야 할 때는 [Testing](../development/testing.md)의 Optional Validation `docs_indexes`를 사용합니다.

## Boundaries

- Directory documentation의 생성 조건과 scope placement → [Documentation Ownership](ownership.md)
- 중복 판단과 canonical owner 선택 → [Duplication Boundaries](duplication-boundaries.md)
- frontmatter와 discovery metadata → [Frontmatter](frontmatter.md)
- generated projection의 repository command와 validation → [Testing](../development/testing.md)
