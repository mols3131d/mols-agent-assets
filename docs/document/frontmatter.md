---
description: Markdown 문서의 frontmatter 필드와 description 작성 기준을 결정하거나 검토할 때 사용합니다.
---

# Frontmatter

이 문서는 `docs/`의 일반 문서에 사용하는 frontmatter 작성 규칙을 소유합니다.

## Fields

- `description`은 필수입니다.
- `title`은 선택입니다.
- `tags`는 taxonomy가 정해질 때까지 사용하지 않습니다.

다른 artifact contract를 따르는 embedded document는 해당 contract가 우선합니다.

## Description

`description`은 요약문보다 **탐색과 라우팅을 위한 trigger metadata**로 작성합니다.

- 문서를 선택해야 하는 상황이나 질문을 식별합니다.
- 문서가 소유하는 책임을 구분할 만큼만 구체적으로 씁니다.
- 제목이나 본문을 반복하지 않습니다.
- 적은 context로 높은 routing signal을 주는 표현을 우선합니다.

Front Matter CMS의 설정과 사용 방법은 [Front Matter CMS](../references/tooling/front-matter-cms.md)를 참고합니다.
