# Repository Work Route

이 repository를 작업하는 agent가 이 entrypoint를 읽었다면 먼저 [`routes.jsonl`](routes.jsonl)을 읽고, **현재 작업 범위를 가장 좁게 설명하는 route 하나**를 선택합니다. 적절한 좁은 route가 없거나 작업이 여러 family를 가로지르면 `all` route를 사용합니다.

선택한 route의 JSONL에서 `name`과 `description`으로 task-relevant Skill만 고르고, 선택한 각 `source`를 읽은 뒤 작업을 계속합니다. 컨텍스트를 늘리기 위해 여러 family route나 `all` route를 함께 선로드하지 않습니다. 작업 범위가 실질적으로 바뀔 때만 route 선택을 다시 평가합니다.

`uncategorized`는 lock-backed Skill 중 어떤 family에도 아직 배정되지 않은 Skill을 노출해 discovery 누락을 막습니다. Family membership은 [`families.json`](families.json)이 소유합니다.

`routes.jsonl`과 각 `*.jsonl`은 root `rulesync.lock`, `rulesync.jsonc`, `skills-lock.json`, `families.json`에서 생성되는 discovery data입니다. 직접 편집하지 않습니다. 이 파일은 routing policy만 소유하며 repository policy는 root [`AGENTS.md`](../../AGENTS.md)와 연결된 canonical 문서가 소유합니다.
