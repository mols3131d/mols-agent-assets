# 자산 개발 가이드

## Directory Roles

- `src/rulesync/rulesync.jsonc`: isolated native Rulesync workspace의 projection configuration.
- `src/rulesync/.rulesync/rules/`: Rulesync-compatible Rule canonical source.
- `src/rulesync/.rulesync/skills/`: Rulesync-compatible Skill canonical source.
- `src/rulesync/.rulesync/subagents/`: Rulesync를 통해 target Agent로 projection되는 Agent canonical source.
- `src/`의 다른 경로: Rulesync contract로 표현할 수 없는 실제 custom/non-standard Agent Asset만 유지.
- `tests/`: 자산 및 도구의 deterministic verification.
- `evals/`: behavioral/model eval과 cross-asset regression contract.
- `docs/<asset-type>/<asset-name>/`: 특정 자산에 필요할 때만 두는 maintainer-only 문서.
- `docs/references/`: 여러 자산이 공유하는 공통·유형별 reference.

Repository root의 `.rulesync/`, `rulesync.jsonc`, `.github/skills/`, `.github/agents/`, `.github/copilot-instructions.md`, `.agents/rules/`, `.agents/skills/`, `.agents/agents/`는 canonical 또는 generated distribution surface로 commit하지 않습니다. `src/rulesync/.rulesync/`만 distribution source로 사용합니다.

현재 target이 canonical asset의 semantics를 완전히 지원하지 않더라도 canonical authority와 target capability를 구분합니다. 지원되지 않는 semantics를 portability 명목으로 삭제하거나 수동 projection으로 위조하지 않습니다.

## Skill Package Convention

Skill은 chatbot/agent 또는 flat/runtime으로 분류하지 않습니다.

모든 canonical Skill은 다음 경로에서 시작합니다.

```text
src/rulesync/.rulesync/skills/<skill-name>/SKILL.md
```

`SKILL.md` 하나로 capability가 완결되면 **single-file Skill**로 유지합니다. 파일 길이나 runtime 존재만으로 분리하지 않습니다.

실행에 실제로 필요할 때만 같은 package에 `references/`, `scripts/`, `assets/`, `templates/` 같은 supporting resource를 추가합니다.

Single-file Skill에서는 top-level `#` heading을 여러 Markdown 문서의 responsibility boundary처럼 사용할 수 있습니다. 모든 heading은 하나의 명확한 책임을 가져야 하며, 불필요한 미세 분할은 하지 않습니다.

## Asset Documentation

자산별 maintainer 문서는 기본 산출물이 아닙니다. canonical source만으로 안전하게 유지보수하기 어렵거나 복잡성·훼손 위험·durable decision·recovery 지식이 별도로 보존될 가치가 있을 때만 `docs/<asset-type>/<asset-name>/`을 만듭니다.

- runtime이 읽어야 하는 정보는 deployable asset package에 둡니다.
- 임시 작업 로그와 쉽게 재생성되는 상태는 durable maintainer docs로 승격하지 않습니다.
- 완료된 migration 계획·보고서는 current guidance로 유지하지 않고 Git history에 맡깁니다.
- 유형 전체가 공유하는 지식은 `docs/references/<asset-type>/`이 소유합니다.

### README 관행

디렉터리 진입 문서가 필요하면 `README.md` 하나만 두고 한국어를 기본으로 작성합니다. `README.en.md`, `README.ko.md`처럼 언어별 복제본은 만들지 않습니다. 제품명, 표준명, 코드·경로·API 식별자와 영어가 더 정확한 기술 용어는 원문을 유지할 수 있습니다.

## Workflow

1. `<owner>/<type>/<topic>` 브랜치를 생성합니다.
1. Rulesync가 표현할 수 있는 Rule, Skill, Agent는 `src/rulesync/.rulesync/`에서 작성하거나 수정합니다. Agent는 Rulesync canonical `subagents/`로 표현합니다.
1. 필요한 경우에만 자산별 maintainer docs를 함께 갱신합니다.
1. Markdown 변경은 repository rumdl policy에 맞춰 format합니다.
1. Read-only Rulesync validation은 `src/rulesync/`에서 `doctor --strict` 또는 `generate --dry-run`으로 수행합니다.
1. Generation처럼 파일을 쓰는 native validation은 `src/rulesync/` workspace 전체를 temporary directory로 복사한 뒤 `generate`와 `generate --check`를 수행합니다. Persistent lock이나 generated target을 이 저장소의 drift baseline으로 두지 않습니다.
1. 필요한 repository test/eval을 실행합니다.
1. canonical source를 검토합니다. generated projection과 Rulesync lock state는 commit하지 않습니다.
