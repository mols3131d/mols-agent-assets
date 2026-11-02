# Repository Work Route

`.agents/route/`는 이 repository를 관리·개발할 때 **사용하는 Agent Asset**의 repository-local routing surface입니다.

로컬 에이전트의 네이티브 Skill 발견 기능으로 필요한 자산을 직접 찾을 수 있다면 이 route를 중복 로드하지 않습니다. 추가 탐색이 필요할 때 [`routes.jsonl`](routes.jsonl)을 읽고 관련 `kind`와 가장 좁은 family를 선택합니다. 작업이 여러 family에 걸치면 **필요한 family route만 각각** 읽습니다. `uncategorized`에는 분류되지 않은 Skill이 있고, `all`은 적절한 route를 알 수 없을 때만 사용하는 최후의 fallback입니다. `all`과 개별 family를 함께 선로드하지 않습니다.

선택한 Skill route의 `name`과 `description`으로 task-relevant Skill만 고르고 실제 필요한 `source`만 로드합니다. 여러 family가 같은 Skill을 제시해도 한 번만 로드합니다. `rulesync.lock`과 `skills-lock.json`의 dependency도 이 탐색 대상입니다. Lock은 선택할 source/revision의 기준이고, 로컬 설치 상태가 그 기준과 같은지는 별도로 검증합니다. 작업 범위가 실질적으로 바뀔 때만 route 선택을 다시 평가합니다.

`uncategorized`는 어떤 family에도 아직 배정되지 않은 lock-backed Skill을 노출해 discovery 누락을 막습니다. Skill family membership은 [`families.json`](families.json)이 소유합니다.

`routes.jsonl`과 현재 Skill family `*.jsonl`은 root `rulesync.lock`, `rulesync.jsonc`, `skills-lock.json`, `families.json`에서 생성되는 discovery data이므로 직접 편집하지 않습니다. 다른 Agent Asset kind가 이 repository에서 실제로 사용되고 선택적 routing이 필요해질 때만 별도 route owner를 추가합니다.

이 surface는 routing만 소유합니다. Repository policy는 root [`AGENTS.md`](../../AGENTS.md)와 연결된 canonical 문서가, 각 Agent Asset의 behavior와 authority는 해당 canonical source가 소유합니다.
