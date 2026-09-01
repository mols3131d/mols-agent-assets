---
description: 저장소 개발 작업에서 공통 개발 원칙, VCS/Git, GitHub, 작성 원본과 권한, repository layout, formatting, validation, testing, evaluation 중 적용할 local policy를 찾을 때 사용합니다.
---

# Development

이 디렉터리는 **이 repository의 개발 규칙과 관행**을 소유합니다.

## Local Policies

- [Development Principles](principles.md) — 여러 유효한 구현 사이에서 효과성, 운영 편의성, 단순성, 추상화와 변경 범위를 판단하는 공통 원칙
- [VCS / Git](vcs-git.md) — branch policy와 naming, commit convention과 enforcement boundary
- [GitHub](github.md) — Issues, Pull Requests, PR Reviews, Merge, Rulesets와 Actions의 local policy. 본문 작성 구조는 [GitHub Authoring Templates](../../.github/templates/README.md)를 참고합니다.
- [작성 원본과 권한](source-authority.md) — 작성 원본, 표준, 대상과 저장소 고유 권한의 경계
- [Repository Layout](repository-layout.md) — 파일·디렉터리의 이름과 배치, 계층, source와 test의 대응
- [Formatting](formatting.md) — changed-only·전체 포맷 경로와 formatter automation boundary
- [Validation](validation.md) — 문서 frontmatter·index, Agent Asset routing, Rulesync-managed assets의 repository validation
- [Testing](testing.md) — deterministic test 설계와 PR Gate
- [Evaluation](evaluation.md) — Agent Asset behavioral evaluation과 evidence 해석

## Related Owners

- Repository agent rules → [`AGENTS.md`](../../AGENTS.md)
- Documentation rules and conventions → [`docs/documentation/`](../documentation/)
- Reusable knowledge → [References](../references/README.md)
- Agent Asset design knowledge → [Agent Assets](../references/agent-assets/README.md)
- Rulesync source/workspace boundary → [Rulesync](../references/tooling/rulesync.md)
- Skill authoring convention → [Skill Authoring Conventions](../references/agent-assets/skills/skill-authoring-conventions.md)

이 README는 development entrypoint이며 linked policy의 본문을 복제하지 않습니다.
