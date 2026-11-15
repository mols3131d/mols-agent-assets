---
description: 개별 Skill과 Skill family의 설계 의도, 경계, 변경 기준과 회귀 검증을 다루는 유지보수 문서 진입점을 찾을 때 사용합니다.
---

# Skill Maintenance Docs

이 디렉터리는 **개별 Skill 또는 Skill family의 설계 의도, 경계, 변경·검증 기준을 유지보수하는 문서**를 둡니다.

- Skill 작성 원본은 `src/rulesync/.rulesync/skills/`(재사용 Rulesync), `src/<vendor>/`(재사용 vendor-native), `.rulesync/skills/`(저장소 전용)가 정본이며, 이 디렉터리의 문서는 실행 지침을 재정의하지 않습니다.
- 모든 Skill에 공통 적용하는 관리 절차와 작성 규약은 [`docs/development/agent-assets/`](../development/agent-assets/README.md)와 [`docs/development/agent-assets/skills/`](../development/agent-assets/skills/README.md)가 소유합니다.
- 이 디렉터리에는 하위 `INDEX.tsv`를 두지 않으며, 상위 [`docs/INDEX.tsv`](../INDEX.tsv)의 `skills/` 항목에서 진입한 뒤 필요한 `<skill>/` 디렉터리의 `README.md`나 유지보수 문서를 직접 탐색합니다. 전체 Skill 목록을 이 문서에 복제하지 않습니다.
