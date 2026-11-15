---
description: Skill 작성에 공통 적용하는 패키지·형식·메타데이터 규약과 공식 명세 registry를 찾을 때 사용합니다.
---

# Skill Authoring Guidance

이 디렉터리는 **모든 Skill 작성에 공통 적용하는 Skill 전용 설계 규약과 공식 명세 registry**를 소유합니다.

- 공통 Agent Asset 관리 절차, 설계 원칙, 지침 작성 기준은 [`docs/development/agent-assets/`](../README.md)와 [Agent Asset Management](../agent-asset-management.md)이 맡습니다.
- 개별 Skill의 유지보수 문서와 회귀 기준은 [`docs/skills/`](../../../skills/README.md)에 둡니다.
- 재사용 가능한 Skill의 작성 원본은 `src/rulesync/.rulesync/skills/`, 이 저장소 전용 Skill 원본은 `.rulesync/skills/`에 둡니다.

## Documents

- [Skill Authoring Conventions](skill-authoring-conventions.md) — 패키지, `description`, context, naming, metadata 관행
- [Skill Specification](specification.md) — Agent Skills 공통 표준, 대상별 확장, creator guidance 공식 원본 registry
