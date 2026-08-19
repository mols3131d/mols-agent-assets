# route

`route/`는 Rulesync native runtime 밖에서 이 저장소의 canonical Agent Asset을 선택적으로 찾고 로드하기 위한 **cross-runtime discovery projection**을 둔다.

이 디렉터리는 canonical source가 아니다. 정본은 계속 각 원본 asset이 소유하며, Rulesync로 관리되는 Rule, Skill, Subagent의 정본은 `src/rulesync/.rulesync/`에 있다.

## 역할

- native discovery가 부족한 chatbot/runtime에 최소 routing metadata를 제공한다.
- routing metadata는 필요한 canonical asset의 `source`를 가리킨다.
- Skill body, Rule body, project policy를 복제하지 않는다.
- Rulesync가 native projection/discovery를 제공하는 runtime에서는 이 route layer를 우선하거나 중복 적용하지 않는다.

## 두 Route Surface

이 저장소가 정의하는 route surface는 이름이 비슷하지만 책임이 다르다.

| 경로 | 책임 |
| --- | --- |
| `route/` | 이 저장소가 배포하는 cross-runtime discovery projection |
| `.agents/routes/` | `mols-chatbot-bootstrap`이 대상 workspace에 둘 수 있는 repository-local compatibility route |

둘은 서로의 출력 위치로 사용하지 않는다.

- `scripts/generate_distribution_routes.py`는 repository-root `route/`만 갱신한다.
- `src/rulesync/.rulesync/skills/mols-chatbot-bootstrap/scripts/generate_routes.py`는 별도의 target-workspace 도구이며 기본적으로 `.agents/routes/`를 다룬다.

## 경계

```text
src/rulesync/.rulesync/   canonical Rulesync assets
        ↓
route/                    derived distribution discovery metadata
        ↓
non-native chatbot/runtime
        ↓
selected canonical asset load
```

`route/`는 `src/rulesync/` 내부에 두지 않는다. `src/rulesync/`는 Rulesync native workspace와 canonical source만 소유하고, 이 저장소의 별도 compatibility convention은 repository-root `route/`가 소유한다.

## 파일

필요한 routing surface만 추가한다.

- `skills.jsonl` — task-relevant Skill을 `name`과 `description`으로 선택하고 해당 `source`를 로드하는 generated metadata.
- `rules.jsonl` — runtime이 native Rule applicability discovery를 제공하지 않을 때만 사용하는 Rule routing metadata.
- `ROUTE.md` — 여러 route 파일을 하나의 entrypoint로 묶을 필요가 있을 때만 추가한다.

현재 `skills.jsonl`은 `src/rulesync/.rulesync/skills/*/SKILL.md`의 canonical `name`과 `description`에서 결정론적으로 생성한다. 각 `source`는 외부 chatbot/runtime이 repository checkout 없이도 읽을 수 있는 canonical raw URL을 가리킨다. 이 파일은 직접 편집하지 않는다.

아직 필요하지 않은 route file을 미리 만들지 않는다.

## Authority

Route entry는 discovery를 위한 파생 metadata다. Route와 canonical asset이 충돌하면 canonical asset이 우선한다.
