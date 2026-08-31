---
description: repository-wide 문서 원칙과 README authoring, indexing, frontmatter, asset maintainer documentation policy를 찾을 때 사용합니다.
---

# Documentation

이 디렉터리는 **repository-wide documentation policy의 entrypoint**입니다. 공통 판단 기준은 [Documentation Principles](principles.md)가 소유하고, 특정 directory나 surface에만 적용되는 contract와 세부 규칙은 가장 가까운 local owner가 소유합니다.

## Working Knowledge

- research·review·draft·handoff 같은 working artifact는 durable knowledge가 되기 전까지 inbox에 둘 수 있습니다. 현재와 미래의 판단을 계속 바꾸는 내용은 적절한 canonical owner에 반영합니다.
- 일반적인 변경 과정과 이전 상태는 Git history와 PR을 기본 기록으로 사용합니다. Archive는 non-canonical artifact 원문 자체를 다시 참고할 가치가 있을 때만 둡니다.

## Policies

- [Documentation Principles](principles.md) — 문서의 목적, scope, authority, 신뢰성, 탐색성과 유지보수성에 적용하는 공통 원칙
- [README Authoring](readme-authoring.md) — directory·bundle `README.md`의 생성 조건, 작성 흐름과 scope metadata
- [Document Indexing](indexing.md) — README inline `Index`와 generated `INDEX.tsv`의 선택 기준
- [Frontmatter](frontmatter.md) — repository 문서의 frontmatter authority와 Front Matter CMS reference routing
- [Asset Maintainer Documentation](asset-maintainer-documentation.md) — asset 또는 family의 portable maintainer documentation contract

Top-level documentation layout은 [`docs/README.md`](../README.md)에서 시작합니다.
