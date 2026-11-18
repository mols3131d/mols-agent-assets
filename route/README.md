# route

`route/`는 이 repository가 **제공하는 Agent Asset**을 native discovery가 없는 runtime에서도 찾을 수 있게 하는 derived discovery surface입니다. Canonical asset body나 policy를 소유하지 않습니다.

- [`ROUTE.md`](ROUTE.md)는 정본을 이미 아는 자산의 직접 로드와, 아직 찾아야 할 자산의 탐색을 구분합니다.
- [`routes.jsonl`](routes.jsonl)은 자산 유형별 다음 목록을 안내합니다. Skill은 [경량 목록](skills-brief.jsonl)이 기본이며, 읽거나 파싱할 수 없으면 `routes.jsonl`의 Skill 항목에 있는 `fallback`으로 복구합니다.
- 경량 목록은 정본 설명의 첫 문장과 `Also use`, `Also apply`, `Always load`로 시작하는 적용 조건을 보존합니다. 목록은 읽었지만 후보가 없거나 적용 여부가 불분명하면 `_meta.fallback`이 [전체 Skill 목록](skills.jsonl)을 안내합니다. 전체 Skill 목록과 [Subagent 목록](subagents.jsonl)은 정본의 전체 설명을 제공합니다.
- `scripts/agent_assets/routes_distribution_generate.py`가 generated `*.jsonl`을 소유하며 직접 편집하지 않습니다.
- `.agents/route/`는 이 repository가 **사용하는 Agent Asset**을 위한 별도 repository-local routing surface입니다. `route/`의 output이 아닙니다.

새 asset kind가 실제 canonical source에 추가되고 cross-runtime discovery가 필요해질 때만 해당 route를 추가합니다. 존재하지 않는 kind를 위한 빈 route나 schema를 미리 만들지 않습니다.

Runtime이 해당 Agent Asset의 native discovery를 제공하면 이 layer를 중복 적용하지 않습니다. Route metadata와 canonical source가 충돌하면 canonical source가 우선합니다.
