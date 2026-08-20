# route

`route/`는 Rulesync native discovery가 없는 chatbot/runtime이 이 저장소의 canonical asset을 찾기 위한 **derived discovery metadata**를 둡니다. Canonical asset body나 policy를 복제하지 않습니다.

## 현재 surface

- `ROUTE.md` — linked route metadata를 실제로 로드하게 만드는 최소 bootstrap entrypoint.
- `skills.jsonl` — `src/rulesync/.rulesync/skills/*/SKILL.md`의 canonical `name`과 `description`에서 결정론적으로 생성되는 Skill routing metadata. 각 `source`는 해당 canonical `SKILL.md` raw URL을 가리킵니다.

`ROUTE.md`는 bootstrap transition만 소유하고, Skill 선택·로딩 규칙은 `skills.jsonl`의 `_meta.instructions`가 소유합니다. `skills.jsonl`은 직접 편집하지 않습니다. `scripts/generate_distribution_routes.py`만 갱신합니다.

Rulesync 또는 runtime이 native discovery를 제공하면 이 layer를 중복 적용하지 않습니다.

## 두 Route Surface

| 경로 | 책임 |
| --- | --- |
| `route/` | 이 저장소가 배포하는 cross-runtime discovery projection |
| `.agents/routes/` | `mols-chatbot-bootstrap`이 대상 workspace에 생성할 수 있는 repository-local compatibility route |

둘은 서로의 output directory가 아닙니다.

## Authority

```text
ROUTE.md
    ↓ load
route/skills.jsonl
    ↓ select
canonical Skill source
```

Route metadata와 canonical asset이 충돌하면 canonical asset이 우선합니다.
