---
description: directory·bundle entrypoint인 README.md의 작성 원칙과 authored INDEXING.md, generated INDEX.tsv의 역할, 생성 조건과 ownership 경계를 결정할 때 사용하는 repository documentation policy입니다.
---

# Entrypoints and Indexes

이 repository의 문서 surface는 **entrypoint**와 **index**의 책임을 filename으로 구분합니다.

| Surface | Role |
| --- | --- |
| directory의 `README.md` | directory entrypoint |
| bundle형 문서 또는 파일의 `README.md` | bundle entrypoint |
| directory의 `INDEXING.md` | 사람이 작성하는 indexing 전담 문서 |
| directory의 `INDEX.tsv` | 생성되는 indexing projection |

`README.md`는 무엇을 읽고 어떻게 시작할지 설명합니다. `INDEXING.md`는 사람이 읽는 curated navigation을, `INDEX.tsv`는 도구와 빠른 discovery를 위한 재생성 가능한 inventory를 담당합니다.

## `README.md`

`README.md`는 directory와 bundle형 문서 또는 파일의 **entrypoint**입니다. Directory나 bundle이 존재한다는 이유만으로 만들지 않고, 시작점에서 설명해야 할 책임이 있을 때만 둡니다.

다음은 `README.md`를 둘 근거가 됩니다.

- 이름만으로 복구하기 어려운 목적이나 responsibility boundary
- 올바른 child·문서·파일을 선택하려면 먼저 알아야 하는 navigation decision
- 해당 scope에만 적용되는 maintenance 또는 recovery rule
- bundle을 하나의 단위로 읽거나 사용할 때 필요한 시작 설명

`README.md`의 목표는 완결된 manual이 아니라 **현재 scope를 이해하고 올바른 다음 행동을 선택하게 하는 것**입니다. 해당 scope가 직접 소유하는 의미와 진입 정보만 두고, 단순 파일 목록이나 쉽게 재생성되는 inventory는 복제하지 않습니다.

### Authoring Questions

README는 고정 template를 채우는 대신, 해당 scope에서 실제로 필요한 질문에 답합니다.

- 이 scope는 무엇을 소유하고 무엇을 위한 것인가?
- 독자는 왜 또는 언제 이 scope를 사용해야 하는가?
- 가장 먼저 취할 권장 행동이나 읽을 경로는 무엇인가?
- 더 자세한 절차, reference, explanation 또는 도움은 어디에 있는가?
- ownership이나 contribution 경계가 명확하지 않다면 누가 또는 무엇이 이를 소유하는가?

Repository root README는 project의 목적과 유용성, 시작 방법, 도움을 얻는 위치와 maintainer·contribution 진입점을 필요에 따라 포함합니다. Directory와 bundle README는 같은 질문을 자기 scope에 필요한 만큼만 축소해서 답하며 root README의 section 구성을 복제하지 않습니다.

### Recommended Flow

README는 독자의 읽기 순서에 맞춰 **orientation → first action → deeper navigation**으로 확장합니다.

1. 첫 문단에서 scope의 정체성, 목적 또는 사용 시점을 가장 짧게 밝힙니다.
1. 행동 전에 알아야 하는 prerequisite, 중요한 boundary나 선택 조건이 있으면 먼저 둡니다.
1. 실제 사용을 바로 시작해야 하는 scope라면 가장 짧은 권장 경로를 제공합니다.
1. 세부 절차와 reference는 canonical document로 연결하고 README에는 진입에 필요한 수준만 남깁니다.
1. curated navigation 자체가 독립적인 책임이 될 만큼 커지면 `INDEXING.md`로 분리합니다.

이 순서는 section template가 아닙니다. 해당 scope에 필요 없는 단계나 section은 만들지 않습니다.

### Writing Rules

- 핵심 정보와 중요한 조건을 문단과 section 앞에 둡니다.
- 한 문단에는 하나의 핵심을 두고, descriptive heading과 얕은 heading hierarchy로 빠르게 훑을 수 있게 합니다.
- 절차에는 가장 권장되는 한 경로를 먼저 제시합니다. 대안은 독자의 선택을 실제로 바꿀 때만 추가합니다.
- Quick start나 command가 있으면 필요한 prerequisite를 먼저 밝히고, 가능한 한 그대로 실행할 수 있는 최소 예시를 제공합니다. Output은 성공 여부 확인이나 다음 행동에 필요할 때만 보여줍니다.
- Repository 안의 다른 문서로 이동할 때는 clone과 branch에서도 동작하는 relative link를 우선합니다.
- GitHub가 Markdown heading에서 outline을 자동 생성하므로 manual table of contents는 기본값으로 두지 않습니다. 다른 주요 consumer가 실제로 필요로 할 때만 추가합니다.
- Full tutorial, exhaustive reference, 긴 architecture explanation, changelog, 반복되는 policy와 단순 file inventory를 README에 누적하지 않습니다. 해당 책임의 canonical owner로 연결합니다.
- Badge나 status summary는 현재 상태를 신뢰할 수 있게 반영하고 독자의 판단에 실제로 도움이 될 때만 둡니다. 장식용 badge wall은 만들지 않습니다.
- `Welcome`, `Overview` 같은 형식적 서론이나 README 자체를 설명하는 문장보다 scope의 결론을 바로 제시합니다.

### Quality Gate

README를 추가하거나 크게 수정할 때 다음을 확인합니다.

- 첫 부분만 읽어도 scope의 목적과 사용 시점, 다음 행동을 판단할 수 있습니다.
- 각 section은 독자의 이해, 선택 또는 행동을 실제로 바꾸며 그렇지 않은 section은 제거하거나 더 적절한 owner로 이동합니다.
- Quick start가 있으면 prerequisite와 command가 실제 권장 경로를 나타내고 copy-paste를 방해하는 불필요한 선택지가 없습니다.
- Repository 내부 link는 가능한 한 relative하며, 이동·clone·branch context에서도 의미가 유지됩니다.
- Child file이 추가되거나 정렬 순서가 바뀌어도 README가 단순 inventory drift 때문에 낡지 않습니다.
- `INDEXING.md`, `INDEX.tsv` 또는 다른 canonical documentation이 소유하는 내용을 README가 중복하지 않습니다.

Directory entrypoint인 `README.md`의 frontmatter `description`은 파일 자체보다 **그 directory를 언제 탐색해야 하는지**를 설명하며 generated docs index의 directory metadata로 사용할 수 있습니다.

이 repository에서 directory metadata source로 인정하는 entrypoint는 `README.md`뿐입니다. `README.md`에 frontmatter가 없거나 필요한 field가 비어 있어도 다른 filename으로 fallback하거나 metadata를 합치지 않습니다.

Frontmatter의 세부 contract는 [Frontmatter](frontmatter.md)가 소유합니다.

## `INDEXING.md`

`INDEXING.md`는 directory에서 사람이 읽는 **indexing 전담 문서**가 실제로 필요할 때만 둡니다. Directory entrypoint가 아니며 directory contract나 metadata source 역할을 대신하지 않습니다.

다음처럼 filesystem이나 generated inventory만으로 복구하기 어려운 curated navigation이 있을 때 가치가 있습니다.

- 문서를 category나 목적별로 묶어 보여줘야 하는 경우
- 권장 reading order나 선택 기준이 필요한 경우
- 같은 directory 안의 항목 사이 관계나 차이를 짧게 설명해야 하는 경우

단순 sibling 목록을 손으로 유지하기 위한 `INDEXING.md`는 만들지 않습니다. 의미 있는 grouping, selection cue나 관계가 없다면 filesystem, search 또는 `INDEX.tsv`를 사용합니다.

`INDEXING.md`는 일반 authored Markdown이므로 해당 documentation frontmatter contract를 따르지만, generated `INDEX.tsv`의 directory metadata source로 사용하지 않습니다.

## `INDEX.tsv`

`INDEX.tsv`는 source document가 아니라 **generated indexing projection**입니다. Row를 직접 추가하거나 수정하지 않고 source Markdown, frontmatter 또는 generator policy를 고친 뒤 다시 생성합니다.

Repository의 docs index는 현재 다음 contract를 사용합니다.

- [`scripts/generate_docs_indexes.py`](../../scripts/generate_docs_indexes.py)가 docs index의 selection과 materialization logic을 소유합니다.
- repository-level write entrypoint는 `mise run generated-sync`입니다.
- 기본 materialization depth는 `0`이므로 `docs/INDEX.tsv`만 생성합니다.
- 그 index는 기본적으로 전체 `docs/` subtree를 재귀적으로 포함합니다.
- field는 `path`와 `description`입니다.
- document row의 `description`은 해당 Markdown frontmatter에서 가져옵니다.
- directory row의 metadata는 해당 directory의 `README.md`에서만 가져옵니다.
- `README.md`와 authored `INDEXING.md`는 generated inventory row로 중복하지 않습니다.
- generated index, `AGENTS.md`, systemic·hidden Markdown과 문서가 없는 subtree는 generator의 selection rule에 따라 제외합니다.

따라서 새 nested directory가 생겼다는 이유만으로 그 안에 `INDEX.tsv`를 수동으로 추가하지 않습니다. 더 깊은 위치에 index materialization이 필요하다면 개별 파일을 추가하는 대신 generator policy와 그 필요성을 함께 변경합니다.

다른 route, catalog 또는 generated index는 이 문서의 `INDEX.tsv` contract를 자동으로 상속하지 않습니다. 해당 surface의 canonical owner와 generator를 따릅니다.

## Maintenance

문서 변경 시 source와 projection의 순서를 지킵니다.

1. `README.md`, `INDEXING.md`, 일반 Markdown 또는 frontmatter의 authored source를 수정합니다.
1. `mise run generated-sync`로 generated projection을 갱신합니다.
1. `INDEX.tsv` diff가 source 변경의 예상 결과인지 검토합니다.
1. 필요한 repository check를 실행하고, 실행하지 않은 검증을 통과했다고 기록하지 않습니다.

Committed docs index drift를 별도로 확인해야 할 때는 [Testing](../development/testing.md)의 Optional Validation `docs_indexes`를 사용합니다.

## Boundaries

- Directory documentation의 생성 조건과 scope placement → [Documentation Ownership](ownership.md)
- 중복 판단과 canonical owner 선택 → [Duplication Boundaries](duplication-boundaries.md)
- frontmatter와 discovery metadata → [Frontmatter](frontmatter.md)
- generated projection의 repository command와 validation → [Testing](../development/testing.md)
