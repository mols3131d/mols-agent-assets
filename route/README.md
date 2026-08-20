# route

`route/`는 native Skill discovery가 없는 runtime을 위한 **derived discovery surface**입니다. Canonical asset body나 policy를 소유하지 않습니다.

- `ROUTE.md`는 bootstrap transition만 소유합니다.
- `skills.jsonl`은 canonical Skill metadata에서 생성되며 직접 편집하지 않습니다. `scripts/generate_distribution_routes.py`가 소유합니다.
- `.agents/routes/`는 `mols-chatbot-bootstrap`이 target workspace에 만드는 별도 compatibility surface이며 `route/`의 output이 아닙니다.

Runtime이 native discovery를 제공하면 이 layer를 중복 적용하지 않습니다. Route metadata와 canonical source가 충돌하면 canonical source가 우선합니다.
