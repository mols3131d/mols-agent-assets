---
description: README의 inline Index와 generated INDEX.tsv 중 적절한 문서 인덱싱 surface를 선택하고 생성·중복·유지보수 경계를 결정할 때 사용하는 repository documentation policy입니다.
---

# Document Indexing

문서 인덱싱은 entrypoint를 대신하지 않습니다. 사람에게 필요한 navigation은 `README.md` 안에서, 재생성 가능한 inventory는 `INDEX.tsv`로 나눕니다.

## Surfaces

| Surface | Responsibility |
| --- | --- |
| Filesystem과 search | 별도 설명이 필요 없는 단순 inventory와 파일 존재 여부 |
| `README.md`의 `Index` section | 작은 scope의 사람용 curated navigation |
| directory의 `INDEX.tsv` | source에서 다시 만들 수 있는 generated indexing projection |

별도 authored index 전용 파일은 두지 않습니다. 기본값은 **index surface를 추가하지 않는 것**이며, 독자의 선택이나 도구의 discovery를 실제로 개선할 때만 README inline `Index` 또는 `INDEX.tsv`를 사용합니다.

## README Inline `Index`

작고 안정적인 curated navigation이면 README 안의 `Index` section으로 충분합니다.

다음 조건에 잘 맞습니다.

- 항목 수가 작고 README의 entrypoint 역할을 흐리지 않는 경우
- path만 보는 것보다 목적, 사용 시점이나 선택 기준을 함께 보면 이득이 있는 경우
- grouping, reading order 또는 관계 설명이 짧은 table 안에서 충분히 표현되는 경우
- 별도 generated index를 materialize하거나 유지할 실익이 없는 경우

Table은 **선택에 필요한 최소 column만** 둡니다. 보통 `Path | Purpose` 또는 `Path | When to use` 정도면 충분합니다. 파일명만 나열하거나 filesystem에서 즉시 복구되는 정보만 반복하는 table은 만들지 않습니다.

Inline index가 길어져 README의 entrypoint 역할을 흐리면 먼저 grouping과 설명을 줄일 수 있는지 검토합니다. 그래도 deterministic inventory가 필요하다면 `INDEX.tsv`를 사용하고, 사람에게 꼭 필요한 선택 기준만 README에 남깁니다.

README 작성 자체의 원칙은 [README Authoring](readme-authoring.md)이 소유합니다.

## `INDEX.tsv`

`INDEX.tsv`는 source document가 아니라 **generated indexing projection**입니다. Row를 직접 추가하거나 수정하지 않고 source Markdown, frontmatter 또는 generator policy를 고친 뒤 다시 생성합니다.

사람에게 설명해야 하는 선택 기준이나 reading cue를 `INDEX.tsv`에 숨기지 않습니다. 반대로 deterministic하게 다시 만들 수 있는 inventory를 README에 손으로 복제하지 않습니다.

같은 scope에 README inline `Index`와 `INDEX.tsv`가 함께 있다면 두 surface는 다른 문제를 해결해야 합니다. README table은 generated inventory에 없는 사람용 selection cue만 소유합니다.

## Repository Docs Projection

이 repository의 docs `INDEX.tsv`는 현재 다음 contract를 사용합니다.

- [`scripts/generate_docs_indexes.py`](../../scripts/generate_docs_indexes.py)가 docs index의 selection과 materialization logic을 소유합니다.
- repository-level write entrypoint는 `mise run generated-sync`입니다.
- 기본 materialization depth는 `0`이므로 `docs/INDEX.tsv`만 생성합니다.
- 그 index는 기본적으로 전체 `docs/` subtree를 재귀적으로 포함합니다.
- field는 `path`와 `description`입니다.
- document row의 `description`은 해당 Markdown frontmatter에서 가져옵니다.
- directory row의 metadata는 해당 directory의 `README.md`에서만 가져옵니다.
- directory entrypoint인 `README.md`는 generated inventory row로 중복하지 않습니다.
- generated `INDEX.*`, `AGENTS.md`, systemic·hidden Markdown과 문서가 없는 subtree는 generator의 selection rule에 따라 제외합니다.

`indexing.md` 같은 일반 lowercase documentation은 이름에 `index`가 들어간다는 이유만으로 generated docs index에서 제외하지 않습니다. 예약된 generated index filename과 일반 문서 filename을 구분합니다.

새 nested directory가 생겼다는 이유만으로 그 안에 `INDEX.tsv`를 수동으로 추가하지 않습니다. 작은 local scope에서 README inline `Index`면 충분하다면 별도 generated index를 요구하지 않습니다. 더 깊은 위치에 `INDEX.tsv` materialization이 실제로 필요하다면 개별 파일을 수동 추가하는 대신 generator policy와 그 필요성을 함께 변경합니다.

다른 route, catalog 또는 generated index는 이 문서의 docs `INDEX.tsv` contract를 자동으로 상속하지 않습니다. 해당 surface의 canonical owner와 generator를 따릅니다.

## Maintenance

Authored source와 generated projection의 순서를 지킵니다.

1. README inline `Index`, 일반 Markdown 또는 frontmatter의 authored source를 수정합니다.
1. generated docs projection에 영향을 주는 변경이면 `mise run generated-sync`를 실행합니다.
1. `INDEX.tsv` diff가 source 변경의 예상 결과인지 검토합니다.
1. README inline index가 generated inventory를 불필요하게 복제하지 않는지 확인합니다.
1. 필요한 repository check를 실행하고, 실행하지 않은 검증을 통과했다고 기록하지 않습니다.

Committed docs index drift를 별도로 확인해야 할 때는 [Testing](../development/testing.md)의 Optional Validation `docs_indexes`를 사용합니다.

## Boundaries

- README entrypoint의 생성·작성·scope metadata → [README Authoring](readme-authoring.md)
- frontmatter와 discovery metadata → [Frontmatter](frontmatter.md)
- 중복 판단과 canonical owner 선택 → [Duplication Boundaries](duplication-boundaries.md)
- generated projection의 repository command와 validation → [Testing](../development/testing.md)
