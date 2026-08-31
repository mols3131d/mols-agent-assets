---
description: repository-wide 문서 배치, ownership, duplication boundary, frontmatter, knowledge lifecycle과 asset maintainer documentation 원칙이 필요할 때 해당 documentation policy를 찾는 데 사용합니다.
---

# Documentation

이 디렉터리는 **이 repository 전체에 적용되는 문서 원칙과 관행**을 소유합니다.

특정 directory나 documentation surface에만 적용되는 contract, navigation, maintenance rule은 여기서 소유하지 않습니다. 그런 규칙은 가장 가까운 local owner, 보통 해당 directory의 `README.md` 또는 그 directory 안의 문서가 소유합니다.

## Policies

- [Ownership](ownership.md) — repository-wide 원칙과 directory-local documentation의 책임 경계
- [Entrypoints and Indexes](entrypoint-readme-index.md) — `README.md` 작성 원칙과 `INDEXING.md`, generated `INDEX.tsv`의 역할·생성 조건
- [Duplication Boundaries](duplication-boundaries.md) — 문서 owner와 scope를 기준으로 중복을 판단하는 공통 원칙
- [Frontmatter](frontmatter.md) — repository 문서의 frontmatter authority와 Front Matter CMS reference routing
- [Knowledge Lifecycle](lifecycle.md) — durable knowledge, inbox, archive와 Git history의 역할
- [Asset Maintainer Documentation](asset-maintainer-documentation.md) — asset 또는 family의 portable maintainer documentation contract

Top-level documentation layout은 [`docs/README.md`](../README.md)에서 시작합니다.
