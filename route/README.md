# route

`route/`는 이 repository가 **제공하는 Agent Asset**을 native discovery가 없는 runtime에서도 찾을 수 있게 하는 derived discovery surface입니다. Canonical asset body나 policy를 소유하지 않습니다.

- `ROUTE.md`는 bootstrap transition만 소유합니다.
- `routes.jsonl`은 제공하는 asset kind의 next route를 선택하게 합니다.
- `skills.jsonl`과 `subagents.jsonl`은 각 canonical source의 `name`·`description`에서 생성되는 asset-kind route입니다.
- `scripts/generate_distribution_routes.py`가 generated `*.jsonl`을 소유하며 직접 편집하지 않습니다.
- `.agents/route/`는 이 repository가 **사용하는 Agent Asset**을 위한 별도 repository-local routing surface입니다. `route/`의 output이 아닙니다.

새 asset kind가 실제 canonical source에 추가되고 cross-runtime discovery가 필요해질 때만 해당 route를 추가합니다. 존재하지 않는 kind를 위한 빈 route나 schema를 미리 만들지 않습니다.

Runtime이 해당 Agent Asset의 native discovery를 제공하면 이 layer를 중복 적용하지 않습니다. Route metadata와 canonical source가 충돌하면 canonical source가 우선합니다.
