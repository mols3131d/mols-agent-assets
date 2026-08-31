---
description: repository-wide 문서 원칙과 README authoring, indexing, frontmatter, asset maintainer documentation policy를 찾을 때 사용합니다.
---

# Documentation

이 디렉터리는 **이 repository 전체에 적용되는 문서 원칙과 관행**을 소유합니다.

특정 directory나 documentation surface에만 적용되는 contract, navigation, maintenance rule은 여기서 소유하지 않습니다. 그런 규칙은 가장 가까운 local owner, 보통 해당 directory의 `README.md` 또는 그 directory 안의 문서가 소유합니다.

## Shared Rules

- 같은 scope에서 같은 의미는 하나의 authoritative owner만 소유합니다. Entrypoint의 짧은 routing label과 link는 중복으로 보지 않습니다.
- 서로 다른 scope의 overlap은 portability나 self-containment에 실제로 필요할 때만 허용합니다.
- 현재와 미래의 판단을 계속 바꾸는 durable knowledge는 canonical owner에 반영합니다. research·review·draft·handoff 같은 working artifact는 canonical이 되기 전까지 inbox에 둘 수 있습니다.
- 일반적인 변경 과정과 이전 상태는 Git history와 PR을 기본 기록으로 사용합니다. Archive는 non-canonical artifact 원문 자체를 다시 참고할 가치가 있을 때만 둡니다.

## Policies

- [Documentation Principles](principles.md) — 문서 생성·배치·ownership·authority에 적용하는 공통 원칙
- [README Authoring](readme-authoring.md) — directory·bundle `README.md`의 생성 조건, 작성 흐름과 scope metadata
- [Document Indexing](indexing.md) — README inline `Index`와 generated `INDEX.tsv`의 선택 기준
- [Frontmatter](frontmatter.md) — repository 문서의 frontmatter authority와 Front Matter CMS reference routing
- [Asset Maintainer Documentation](asset-maintainer-documentation.md) — asset 또는 family의 portable maintainer documentation contract

Top-level documentation layout은 [`docs/README.md`](../README.md)에서 시작합니다.
