---
description: 저장소 개발 작업의 local policy, Agent Asset 설계 지식과 도구·명세 참고 자료를 찾을 때 사용합니다.
---

# Development

이 디렉터리는 **이 repository의 개발 규칙과 관행, Agent Asset 설계 지식과 도구·명세 참고 자료**를 소유합니다. 설계 지식과 공식 자료는 다른 repository에서도 필요한 부분을 참고·채택할 수 있지만, 이곳의 local policy가 consumer에 자동 적용되지는 않습니다.

## Local Policies

- [Development Principles](principles.md) — 여러 유효한 구현 사이에서 효과성, 운영 편의성, 단순성, 추상화와 변경 범위를 판단하는 공통 원칙
- [Development Environment](development-environment.md) — 개발환경 구축·복구·업데이트 운영 정책의 정본과 사용자 설치 허가 경계
- [VCS / Git](vcs-git.md) — branch policy와 naming, commit convention과 enforcement boundary
- [GitHub](github.md) — Issues, Pull Requests, PR Reviews, Merge, Rulesets와 Actions의 local policy. 본문 작성 구조는 [GitHub Authoring Templates](../../.github/templates/README.md)를 참고합니다.
- [Continuous Integration](ci.md) — local·CLI·API·MCP·Plugin·agent write path부터 branch validation, PR admission, deferred evidence와 projection gate까지의 integration lifecycle
- [작성 원본과 권한](source-authority.md) — 작성 원본, 표준, 대상과 저장소 고유 권한의 경계
- [Repository Layout](repository-layout.md) — 파일·디렉터리의 이름과 배치, 계층, source와 test의 대응
- [Formatting](formatting.md) — changed-only·전체 포맷 경로와 formatter automation boundary
- [Validation](validation.md) — 문서 frontmatter·index, Agent Asset routing, Rulesync-managed assets의 repository validation
- [Testing](testing.md) — deterministic test 설계와 repository-owned executable behavior의 evidence boundary
- [Evaluation](evaluation.md) — Agent Asset behavioral evaluation과 evidence 해석

## Design and Tooling References

- [Agent Asset Design](agent-assets/README.md) — 공통 설계 원칙, instruction 설계, naming과 Skill-specific specification·authoring convention
- [Tooling References](tooling/README.md) — 외부 도구·명세의 공식 source routing과 integration knowledge

## Related Owners

- Repository agent rules → [`AGENTS.md`](../../AGENTS.md)
- Documentation rules and conventions → [`docs/documentation/`](../documentation/)
- 프로젝트 도구의 기본 설정·버전 선택·예외 → [Tools](../tools/README.md)
- Reusable solution patterns → [Patterns](../../catalog/patterns/README.md)
- Rulesync source/workspace boundary → [Rulesync](tooling/rulesync.md)
- Skill authoring convention → [Skill Authoring Conventions](agent-assets/skills/skill-authoring-conventions.md)

이 README는 development entrypoint이며 linked policy의 본문을 복제하지 않습니다.
