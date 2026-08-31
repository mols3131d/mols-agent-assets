---
description: directory·bundle entrypoint인 README.md의 생성 조건, scope metadata와 작성·품질 원칙을 결정할 때 사용하는 repository documentation policy입니다.
---

# README Authoring

`README.md`는 directory와 bundle형 문서 또는 파일의 **entrypoint**입니다. 완결된 manual이 아니라 현재 scope를 이해하고 올바른 다음 행동을 선택하게 하는 orientation layer입니다.

Directory나 bundle이 존재한다는 이유만으로 만들지 않습니다. 시작점에서 설명해야 할 책임이 있을 때만 둡니다.

## Responsibility

다음 중 하나 이상이 실제로 필요하면 `README.md`를 둘 근거가 됩니다.

- 이름만으로 복구하기 어려운 목적이나 responsibility boundary
- 올바른 child·문서·파일을 선택하려면 먼저 알아야 하는 navigation decision
- 해당 scope에만 적용되는 maintenance 또는 recovery rule
- bundle을 하나의 단위로 읽거나 사용할 때 필요한 시작 설명

`README.md`에는 해당 scope가 직접 소유하는 의미와 진입 정보만 둡니다. 상세 tutorial, exhaustive reference, 긴 explanation, 반복되는 policy와 단순 inventory는 더 적절한 canonical owner로 분리합니다.

## Authoring Questions

README는 고정 template를 채우는 대신, 해당 scope에서 실제로 필요한 질문에 답합니다.

- 이 scope는 무엇을 소유하고 무엇을 위한 것인가?
- 독자는 왜 또는 언제 이 scope를 사용해야 하는가?
- 가장 먼저 취할 권장 행동이나 읽을 경로는 무엇인가?
- 더 자세한 절차, reference, explanation 또는 도움은 어디에 있는가?
- ownership이나 contribution 경계가 명확하지 않다면 누가 또는 무엇이 이를 소유하는가?

Repository root README는 project의 목적과 유용성, 시작 방법, 도움을 얻는 위치와 maintainer·contribution 진입점을 필요에 따라 포함합니다. Directory와 bundle README는 같은 질문을 자기 scope에 필요한 만큼만 축소해서 답하며 root README의 section 구성을 복제하지 않습니다.

## Recommended Flow

README는 독자의 읽기 순서에 맞춰 **orientation → first action → deeper navigation**으로 확장합니다.

1. 첫 문단에서 scope의 정체성, 목적 또는 사용 시점을 가장 짧게 밝힙니다.
1. 행동 전에 알아야 하는 prerequisite, 중요한 boundary나 선택 조건이 있으면 먼저 둡니다.
1. 실제 사용을 바로 시작해야 하는 scope라면 가장 짧은 권장 경로를 제공합니다.
1. 세부 절차와 reference는 canonical document로 연결하고 README에는 진입에 필요한 수준만 남깁니다.
1. 작은 curated navigation이 필요하면 README 안에 `Index` section을 둘 수 있습니다.

이 순서는 section template가 아닙니다. 해당 scope에 필요 없는 단계나 section은 만들지 않습니다.

## Writing Rules

- 핵심 정보와 중요한 조건을 문단과 section 앞에 둡니다.
- 한 문단에는 하나의 핵심을 두고, descriptive heading과 얕은 heading hierarchy로 빠르게 훑을 수 있게 합니다.
- 절차에는 가장 권장되는 한 경로를 먼저 제시합니다. 대안은 독자의 선택을 실제로 바꿀 때만 추가합니다.
- Quick start나 command가 있으면 필요한 prerequisite를 먼저 밝히고, 가능한 한 그대로 실행할 수 있는 최소 예시를 제공합니다. Output은 성공 여부 확인이나 다음 행동에 필요할 때만 보여줍니다.
- Repository 안의 다른 문서로 이동할 때는 clone과 branch에서도 동작하는 relative link를 우선합니다.
- GitHub가 Markdown heading에서 outline을 자동 생성하므로 manual table of contents는 기본값으로 두지 않습니다. 다른 주요 consumer가 실제로 필요로 할 때만 추가합니다.
- Badge나 status summary는 현재 상태를 신뢰할 수 있게 반영하고 독자의 판단에 실제로 도움이 될 때만 둡니다. 장식용 badge wall은 만들지 않습니다.
- `Welcome`, `Overview` 같은 형식적 서론이나 README 자체를 설명하는 문장보다 scope의 결론을 바로 제시합니다.

## Inline Index

`INDEXING.md`나 local `INDEX.tsv`를 별도 surface로 둘 만큼 indexing 책임이 크지 않은 경우에는 README 안에 `Index` section과 작은 table을 둘 수 있습니다. 이 예외는 README의 entrypoint 역할을 흐리지 않는 범위에서 유지합니다.

Table column, 별도 `INDEXING.md`로의 승격 기준, generated `INDEX.tsv`와의 중복 경계 같은 세부 규칙은 [Document Indexing](indexing.md)이 소유합니다.

## Scope Metadata

Directory 또는 bundle의 entrypoint인 `README.md`는 frontmatter에 **README 파일 자체가 아니라 그 entrypoint가 대표하는 scope의 metadata**를 담습니다.

- `description`은 그 directory 또는 bundle을 **언제 탐색하거나 사용해야 하는지**를 설명합니다.
- `title`을 사용할 때는 README라는 파일명이 아니라 그 directory 또는 bundle의 사람이 읽는 이름을 나타냅니다.
- `이 README는 ...을 설명합니다`처럼 파일 자체를 서술하기보다 scope의 목적, trigger와 responsibility boundary를 표현합니다.

Generated docs index가 directory metadata를 projection할 때는 해당 directory의 `README.md`만 source로 사용합니다. `README.md`에 frontmatter가 없거나 필요한 field가 비어 있어도 다른 filename으로 fallback하거나 metadata를 합치지 않습니다.

Bundle README의 frontmatter도 같은 **scope metadata** 원칙을 따르지만, 특정 generator나 consumer가 bundle metadata를 어떻게 사용하는지는 해당 owner가 별도로 정의합니다. 일반 documentation frontmatter의 field와 schema는 [Frontmatter](frontmatter.md)가 소유합니다.

## Quality Gate

README를 추가하거나 크게 수정할 때 다음을 확인합니다.

- 첫 부분만 읽어도 scope의 목적과 사용 시점, 다음 행동을 판단할 수 있습니다.
- 각 section은 독자의 이해, 선택 또는 행동을 실제로 바꾸며 그렇지 않은 section은 제거하거나 더 적절한 owner로 이동합니다.
- Quick start가 있으면 prerequisite와 command가 실제 권장 경로를 나타내고 copy-paste를 방해하는 불필요한 선택지가 없습니다.
- Repository 내부 link는 가능한 한 relative하며, 이동·clone·branch context에서도 의미가 유지됩니다.
- Child file이 추가되거나 정렬 순서가 바뀌어도 README가 단순 inventory drift 때문에 낡지 않습니다.
- Inline `Index`가 있다면 README의 entrypoint 역할을 흐리지 않고 [Document Indexing](indexing.md)의 중복·승격 규칙을 따릅니다.
- Entrypoint frontmatter는 README 파일보다 directory 또는 bundle scope를 설명합니다.

## Boundaries

- README의 생성 조건과 scope placement → [Documentation Ownership](ownership.md)
- inline `Index`, `INDEXING.md`, `INDEX.tsv`의 선택과 유지보수 → [Document Indexing](indexing.md)
- frontmatter field와 discovery metadata → [Frontmatter](frontmatter.md)
- 중복 판단과 canonical owner 선택 → [Duplication Boundaries](duplication-boundaries.md)
