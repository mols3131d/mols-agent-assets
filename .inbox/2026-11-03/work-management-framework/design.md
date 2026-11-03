---
description: 개인 개발용 작업 관리와 Spec/Test-driven 개발을 하나의 선택형 Skill로 통합하는 설계와 제약입니다.
---

# Personal Project Workflow — Integration Design

## Goal and Boundary

개인 토이 프로젝트와 국지적인 소프트웨어 개발을 위한 **단일 진입점 Skill `mols-project-workflow`**을 설계한다. 작업 관리와 스펙/테스트 기반 개발은 함께 제공하되 **요청에 필요한 경로만 실행**한다. 모든 단일 수정에 스펙·작업 파일을 강제하지 않는다.

**작업 정본은 사용자 지정 위치의 Markdown**, **도메인 동작 정본은 사용자 지정 spec root의 `specs/`**가 소유한다. Git은 선택적 변경 이력·ref 관리 수단이다. task directory·task Git ref·code Git ref는 같거나 달라도 된다. Beads에서는 작업 단위·의존 관계·ready 판단·재개만 참고하며 Beads, Dolt, GitHub Issues, DB, 서버, MCP, 전용 CLI를 실행 전제로 두지 않는다.

현재 `main`의 `mols-spec-stdd`가 **이미 소유한** change-scoped delta, 계층형 domain spec, workflow, Review 복귀, 완료 후 스펙 흡수는 유지한다. 처음부터 재구현하지 않고 기존 구현을 새 통합 패키지로 **이전·단순화**한다. 이 PR의 현재 작업 브랜치는 `main`과 분기되어 해당 Skill이 아직 없으므로 구현 전에 최신 `main`과 안전하게 통합한다.

사용자가 파일 기반 작업 관리를 채택하지 않았거나 기존 정본 tracker가 있다면 별도 task 정본을 무단 생성하지 않는다. 스펙 전용 요청은 task 파일 없이, 단순 작업 관리는 스펙 파일 없이 수행할 수 있다.

## Integrated Ownership and Selection

| 사용자 의도 | 실행할 기능 | 생성하지 않을 것 |
| --- | --- | --- |
| 작업 목록 정리, 의존·우선순위, 다음 작업, 재개 | Work Management | 스펙 변경·테스트 산출물 |
| 작은 버그 수정·코드 정리 | 프로젝트의 기본 개발 방법 | 새 task/spec 기록(필요 없을 때) |
| 의미 있는 API·도메인 요구사항 변경 | Spec/Test-driven + Review | 불필요한 task 항목 |
| 작업을 선택해 실제 기능 개발 | Work Management → 필요 시 Spec/Test-driven | 둘의 상태를 복제한 제3의 문서 |
| 스펙 변경 완료·정본 흡수 | Spec Store의 승인·검증 조건 | task `done` 자동 변경 |
| 작업 기록 완료 | task의 완료 근거 확인 | spec delta 자동 archive |

- **Work Item**은 여러 작업의 우선순위·의존성·인계를 소유한다. **Change**는 소프트웨어 요구사항 변경 제안·delta·검증 산출물을 소유한다. **Domain Spec**은 현재 기대 동작의 장기 정본이다. 이 셋은 동일 객체가 아니며 1:1 관계를 강제하지 않는다.
- 서로 연결할 때는 기존 Markdown 링크 또는 ref만 사용한다. 별도 연결 테이블, task 상태와 spec 상태를 병행 기록하는 파일, 필수 lifecycle 미들웨어를 만들지 않는다.
- 스펙 변경의 Review PASS와 delta 흡수는 여전히 기존 검증 근거가 필요하다. task가 `done`이어도 자동 흡수하거나, 스펙이 흡수됐다는 이유로 다른 task를 자동 완료시키지 않는다.
- 통합 Skill에는 **하나의 discoverable `SKILL.md`**만 둔다. 작업 관리의 짧은 절차는 entrypoint에, 상대적으로 무거운 Spec Store·Workflow·Script 설명은 필요할 때만 읽는 package resource에 둔다. 독립 `mols-spec-stdd`를 런타임 필수 의존성으로 두지 않는다.

## Storage: User-selected Directory and Ref

저장 위치는 프레임워크의 상수가 아니라 **작업 대상의 식별 정보**다.

| 요소 | 선택과 의미 |
| --- | --- |
| Repository / workspace | 실제 접근 가능한 프로젝트 또는 Git 저장소 |
| Task directory | 사용자가 선택한 경로. 루트·하위 디렉터리·기존 문서 경로 모두 가능 |
| Task Git ref | Git을 사용할 때 현재 코드 ref 또는 작업 관리 전용 branch를 선택 가능 |
| Code Git ref | 구현 코드의 기준 ref. 작업 관리 ref와 달라도 됨 |

- 특정 디렉터리 이름, `.work/`, `items/`를 기본 생성하거나 강제하지 않는다. 기존 작업 파일을 발견했다면 활용 여부를 확인하고, 경로를 아직 모르면 사용자에게 **저장 위치 선택**을 요청한다. 임의의 파일 쓰기로 먼저 결정하지 않는다.
- **작업 저장 위치는 `repository + task ref + directory`로 식별한다.** Git이 없는 경우에는 선택한 workspace와 directory만 사용한다. 별도 작업 branch만 지정하면 그 branch 루트도 유효한 directory다.
- 코드와 작업을 같은 branch/디렉터리에서 관리할 수도, 예를 들어 코드 `main`·작업 `tasks` branch에서 독립 관리할 수도 있다. 별도 branch를 강제 생성하거나 코드 branch로 merge하지 않는다.
- 작업 목록을 조회·수정·재개할 때 **선택된 task ref**를 기준으로 한다. 현재 checkout 또는 기본 branch를 작업 정본으로 임의 대체하지 않는다. 코드 변경이나 검증 결과는 해당 code ref를 기준으로 읽고 작업 파일에는 필요한 참조만 적는다.
- 저장 위치 선택은 사용자 요청·프로젝트의 기존 지침에서 재사용한다. 독립적인 설정 파일·registry를 자동 생성하지 않는다. 새 세션에서 경로/ref를 복원할 수 없으면 현재 사실을 조회하거나 사용자에게 확인한다.
- ref가 없거나 접근·쓰기 권한이 없으면 다른 branch에 대신 쓰지 않는다. GitHub Chat 등 원격 도구를 쓰더라도 같은 경계를 적용한다. 다른 계정·명의로 전환하지 않는다.

### Example: Separate Task Branch

```text
repository: toy-api
code ref: main
task ref: tasks
task directory: planning/
  backend/db-schema.md
  backend/login-api.md
  docs/getting-started.md
```

위 경로는 **사용자가 선택할 수 있는 예시**다. `planning/`이나 `tasks`는 프레임워크 기본값이 아니다. `tasks:planning/backend/login-api.md`와 `main:src/... `는 서로 다른 Git ref의 자산이다. 실제 작업을 진행할 때 해당 ref가 존재하고 파일 접근이 가능한지 확인한다.

## Human-readable Work Items

작업 파일은 에이전트가 파싱하는 데이터이면서 사람이 에디터·Git diff·파일 탐색기에서 읽는 문서다. **구분성·가독성은 단순한 부가 기능이 아닌 설계 품질 조건**이다.

- 파일 이름은 `login-api.md`, `db-schema.md`처럼 의미 있는 짧은 이름을 쓴다. 난수·타임스탬프·불투명한 ID를 기본으로 강제하지 않는다. 유사한 작업이 많으면 `backend/`, `docs/` 등의 사용자 선택 하위 디렉터리로 구분할 수 있다.
- 의존 참조는 **선택한 task directory 기준 상대 경로(확장자 제외)**를 사용한다. 예: `backend/db-schema`. 본문에 같은 ID를 중복 작성하지 않는다. 파일을 이동·개명할 때 참조를 함께 갱신한다.
- Markdown의 **제목은 사람이 읽는 작업 이름**이고, 첫 설명은 달성할 결과를 말한다. 작업 상태·의존성 같은 기계적으로 필요한 필드만 간결한 frontmatter에 둔다. 복잡한 메타데이터·서식을 강제하지 않는다.
- 완료 조건·진행 내용·다음 행동은 실제로 필요한 것만 **찾기 쉬운 짧은 본문**에 둔다. 다른 문서의 스펙·코드·테스트 결과를 복제하지 않고 링크한다.
- 작업 목록을 보여줄 때는 의미 있는 제목, `todo / doing / done / cancelled`, 차단 여부, 다음 행동을 명확히 구분한다. `ready / blocked / unknown`은 일시적 판단이므로 status에 저장하거나 별도 대시보드 파일을 강제하지 않는다.

예: 사용자 지정 디렉터리에 존재하는 `backend/login-api.md`:

```markdown
---
status: todo
depends_on: [backend/db-schema]
---
# 로그인 API 구현

로그인 요청의 정상·오류 응답을 제공한다.

## 완료 조건
- 지정된 입력과 실패 응답을 검증했다.

## 다음 행동
- DB 스키마 완료 여부를 확인하고 API를 구현한다.
```

필수는 **명확한 제목과 `status`**다. `depends_on`과 `priority: high | normal | low`는 필요할 때만 추가한다. 상태는 `todo | doing | done | cancelled` 네 개로 제한한다. 잠시 중단해도 새 상태를 만들지 않고 짧게 현재 상황과 다음 행동을 적는다. 완료 작업은 기본적으로 보존하며, 정리는 프로젝트가 정한다.

## Dependency, Ready, and Resume

1. `todo` 작업의 모든 `depends_on`이 `done`이고 알려진 외부 차단이 없을 때 **ready**로 판정한다.
2. 미완료·취소된 선행 작업 또는 외부 blocker가 있으면 **blocked**, 참조 누락·순환·권한/조회 불가로 확인이 안 되면 **unknown**이다. blocker나 unknown을 ready로 취급하지 않는다.
3. `doing`은 ready 대기열이 아니라 **진행 중 작업의 재개 후보**로 따로 보여준다. 사용자 목표와 진행 맥락을 우선하고, 필요할 때만 priority를 참고한다.
4. 큰 일만 필요한 만큼 분해해 별도 Markdown으로 만들고, 하위 작업·스펙·PR은 상대 경로/링크로 연결한다. 부모·트래커·상태 인덱스를 별도 생성하지 않는다.
5. 재개 시 이전 메시지나 인계의 상태를 그대로 신뢰하지 않는다. 선택한 **task ref + directory**, 파일의 최신 내용, 필요한 code ref·산출물을 다시 조회한다. 작업 기록에 확인된 사실·남은 일·다음 행동만 보존한다.

## Minimal Agent Procedure

`locate → inspect → choose → act → note`를 상황에 맞게 수행한다. 모든 작업에서 모든 단계를 문서화하거나 commit하지 않는다.

- **Locate:** 사용자가 선택한 저장 위치와 Git ref 및 작업 범위를 확인한다. 없는 디렉터리·branch를 추측하거나 만들지 않는다.
- **Inspect:** 관련 작업을 읽고 제목·상태·의존 참조를 확인하며, 잘못된 경로·중복 참조·순환 관계를 점검한다.
- **Choose:** 진행 중/ready/blocked/unknown을 구분하고 다음 작업과 이유를 짧게 제시한다.
- **Act:** 허용된 범위에서 task ref의 파일을 수정한다. 파일 경로·ref·권한·최신 상태를 확인하고 저장 결과를 다시 읽는다. 다른 ref로 쓰기, 자동 branch 생성, 무단 force push를 금지한다.
- **Note:** 세션이 끝나거나 다음 수행에 맥락이 필요할 때만 해당 파일에 다음 행동과 핵심 근거를 남긴다.

Git branch·commit·PR 생성은 **사용자의 저장소 운영 방식**을 따른다. 별도 task branch에서 기록을 보존하려면 실제 commit/push가 필요한 상황을 구분하되 작업당 commit을 규칙으로 만들지 않는다. Git은 lock·전역 claim·트랜잭션을 제공하지 않으므로 같은 파일의 병렬 수정은 최신 변경과 충돌을 확인한다. CLI가 없고 허용된 파일 도구만 있으면 그 범위에서 동작하며, 실행하지 않은 Git 동작을 완료로 보고하지 않는다.

## Design Checks

| Scenario | Expected result |
| --- | --- |
| 사용자가 다른 경로·기존 문서 디렉터리를 지정 | 강제 `.work/` 생성 없이 정확한 경로 사용 |
| 사용자가 작업 전용 branch를 지정 | 코드 branch와 독립적으로 작업 파일 조회·갱신, 임의 merge 없음 |
| task ref가 누락·조회 불가 | 기본 branch로 자동 대체하지 않고 차단·인계 |
| 비슷한 이름의 작업이 여러 폴더에 존재 | 상대 경로·제목으로 구분되고 의존 참조가 모호하지 않음 |
| 파일 이동·이름 변경 | 참조 영향 확인, 끊어진 의존 참조를 ready로 오판하지 않음 |
| 5개 작업의 의존·우선순위·중단 재개 | ready/blocked/unknown 판정과 재개 상태가 일관됨 |
| 같은 파일의 서로 다른 Git ref 수정 | 최신 ref 확인·충돌 인지, 자동 덮어쓰기 없음 |
| 단일 수정·스펙/테스트·build task | 불필요한 작업 파일이나 단계 생성 없이 비활성화 |

## Existing Spec Implementation: Preserve vs. Simplify

| 현재 `mols-spec-stdd` 구성 | 통합 시 원칙 |
| --- | --- |
| `changes/<change-id>/specs/<domain>/spec.md` → `specs/<domain>/spec.md` | **보존:** delta와 도메인 정본 분리, 계층형 domain, 완료 시 정본 흡수 |
| `changes/archive/`와 stale baseline·충돌 검사 | **보존:** 기존 문서·스크립트의 안전한 완료 계약 |
| Default / Focused Workflow, Review finding 복귀 | **보존:** 상황에 따라 선택, 전체 8단계 강제 금지 |
| Artifact Registry, templates, `flow.py`, `store.py` | **우선 재사용:** 실제 기여를 확인하고 불필요한 것만 단순화; 테스트 없이 제거하지 않음 |
| 기존 maintainer guide, tests, eval cases, route | **이관 대상:** 현재 경로와 활성화 계약에 맞추어 함께 갱신 |

작업 파일의 storage locator와 별개로 **spec root/ref도 프로젝트가 결정**한다. 기존 `spec/` 제안은 소비 프로젝트에 경로를 강제하는 규칙이 아니다. Task ref와 spec ref가 다르면 스펙 흡수나 task 완료를 **교차 브랜치 원자적 작업**으로 취급하지 않는다. 각각의 원본·권한·최신 상태·완료 근거를 확인하고 필요한 참조만 연결한다.

## Implementation Strategy

1. **Baseline:** PR #284 브랜치에 최신 `main`을 안전하게 통합하고 `mols-spec-stdd` 원본·테스트·eval·route·유지보수 문서 inventory를 확보한다. 이 상태에서는 기존 Skill을 삭제하지 않는다.
2. **Unify:** `src/rulesync/.rulesync/skills/mols-project-workflow/`를 단일 재사용 작성 원본으로 정하고 기존 Spec package의 의미·실행 자원을 보존하며 통합 Skill로 이전한다. 초기 migration 동안 중복 파일이 존재하더라도 *두 활성 정본*으로 배포하지 않는다.
3. **Add Tasks:** 사용자 지정 task directory/ref, 가독성 높은 Markdown, 의존성/ready/blocked/unknown 판정, 세션 재개를 entrypoint에 추가한다. 스펙 문서·스크립트는 task 처리 시 로드하지 않는다.
4. **Streamline:** 실제 소규모 사례로 Default/Focused·template·script의 사용성을 비교한다. 검증 보호장치나 핵심 스펙 기능은 성급히 삭제하지 않고, 필요 없는 진입 절차와 파일만 제거한다.
5. **Validate & Retire:** 기존 Spec deterministic tests·새 task 사례·integration 동작 평가를 수행하고, 관련 route/lock 영향·eval·maintainer 문서와 소비자 참조를 확인한다. 기능 대체가 확인된 뒤 기존 `mols-spec-stdd`를 안전하게 은퇴한다. 미검증이면 유지하거나 후속 작업으로 명시한다.

**이번 단계의 산출물은 설계·계획뿐이다.** 실제 Skill 작성·파일 이동·삭제·branch 동기화·CI·모델 행동 평가는 후속 작업이다. 구조·의미 검토와 실제 런타임 평가는 구분한다.

이 파일은 PR 인계용 설계 근거다. 실제 에이전트 동작의 정본은 구현될 통합 Skill이 소유한다.
