# Repository Work Route

`.agents/route/`는 이 repository를 관리·개발할 때 **사용하는 Agent Asset**의 repository-local routing surface입니다.

이 entrypoint를 읽었다면 먼저 [`routes.jsonl`](routes.jsonl)을 읽습니다. 서로 다른 `kind`의 Agent Asset이 독립적으로 적용되면 필요한 kind의 route만 선택합니다. 현재 generated `kind`인 `skills`에서는 **현재 작업 범위를 가장 좁게 설명하는 family route 하나**를 선택하고, 적절한 좁은 family가 없거나 작업이 여러 family를 가로지르면 `all`을 사용합니다. 여러 Skill family route나 `all`을 함께 선로드하지 않습니다.

선택한 Skill route의 JSONL에서 `name`과 `description`으로 task-relevant Skill만 고르고 각 `source`를 읽은 뒤 작업을 계속합니다. `rulesync.lock`과 `skills-lock.json`에서 가져오는 외부 Skill도 같은 routing 대상입니다. 작업 범위가 실질적으로 바뀔 때만 route 선택을 다시 평가합니다.

`uncategorized`는 어떤 family에도 아직 배정되지 않은 lock-backed Skill을 노출해 discovery 누락을 막습니다. Skill family membership은 [`families.json`](families.json)이 소유합니다.

`routes.jsonl`과 현재 Skill family `*.jsonl`은 root `rulesync.lock`, `rulesync.jsonc`, `skills-lock.json`, `families.json`에서 생성되는 discovery data이므로 직접 편집하지 않습니다. 다른 Agent Asset kind가 이 repository에서 실제로 사용되고 선택적 routing이 필요해질 때만 별도 route owner를 추가합니다.

이 surface는 routing만 소유합니다. Repository policy는 root [`AGENTS.md`](../../AGENTS.md)와 연결된 canonical 문서가, 각 Agent Asset의 behavior와 authority는 해당 canonical source가 소유합니다.
