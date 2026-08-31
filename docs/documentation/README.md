---
description: 저장소 전반의 문서 원칙과 README 작성, 문서 인덱싱, frontmatter, Agent Asset 유지보수 문서 정책을 찾을 때 사용합니다.
---

# Documentation

이 디렉터리는 **저장소 전반의 문서 정책을 찾는 시작점**입니다. 공통 판단 기준은 [Documentation Principles](principles.md)가 맡고, 특정 디렉터리나 문서 유형에만 적용되는 규칙은 가장 가까운 문서 책임 주체가 맡습니다.

## Working Knowledge

- 조사·검토·초안·인계 자료처럼 작업 중인 결과물은 계속 참고할 지식으로 확정되기 전까지 inbox에 둘 수 있습니다. 이후에도 판단에 영향을 주는 내용으로 확정되면 적절한 정본 문서에 반영합니다.
- 일반적인 변경 과정과 이전 상태는 Git history와 PR을 기본 기록으로 사용합니다. 보관본은 Git 이력만으로 부족하고 원문 자체를 다시 볼 가치가 있을 때만 둡니다.

## Policies

- [Documentation Principles](principles.md) — 문서의 목적, 책임 범위, 정본, 신뢰성, 탐색성, 유지보수성에 적용하는 공통 원칙
- [README Authoring](readme-authoring.md) — 디렉터리나 문서·파일 묶음의 README를 언제 만들고 무엇을 담을지 정하는 정책
- [Document Indexing](indexing.md) — README의 `Index`와 자동 생성 `INDEX.tsv` 중 어떤 방식을 사용할지 정하는 원칙
- [Frontmatter](frontmatter.md) — 문서 frontmatter와 `description`의 탐색·라우팅 역할
- [Asset Maintainer Documentation](asset-maintainer-documentation.md) — Agent Asset 또는 family의 유지보수 문서 배치와 책임 경계

상위 문서 구조는 [`docs/README.md`](../README.md)에서 확인합니다.
