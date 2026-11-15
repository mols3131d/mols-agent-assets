---
description: 재사용 Subagent와 Subagent family별 설계 의도, 역할 경계, 유지보수 기준을 다루는 개별 문서 진입점을 찾을 때 사용합니다.
---

# Subagent Maintenance Docs

이 디렉터리는 **개별 Subagent 또는 Subagent family의 설계 의도, 위임·권한 경계, 변경·검증 기준을 유지보수하는 문서**를 둡니다.

- Subagent 실행 정의의 정본은 `src/rulesync/.rulesync/subagents/`(재사용)와 `.rulesync/subagents/`(저장소 전용)이며, 이 디렉터리의 문서는 실행 계약을 복제하거나 대체하지 않습니다.
- 공통 Agent Asset 관리 절차와 설계 원칙은 [`docs/development/agent-assets/`](../development/agent-assets/README.md)가 소유합니다.
- 이 디렉터리에는 하위 `INDEX.tsv`를 두지 않으며, 상위 [`docs/INDEX.tsv`](../INDEX.tsv)의 `subagents/` 항목에서 진입한 뒤 필요한 `<subagent>/` 디렉터리의 `README.md`나 유지보수 문서를 직접 탐색합니다. 전체 Subagent 목록을 이 문서에 복제하지 않습니다.
