---
description: 개인 소규모 개발을 위한 작업 관리·Spec/Test-driven 통합 Skill의 간결한 설계 결정입니다.
---

# Personal Project Workflow — Design

## Goal

`mols-project-workflow`는 개인 토이 프로젝트에서 **할 일을 선택하고, 개발하고, 다음 세션에 이어가는** 단일 Skill이다. 기존 `mols-spec-stdd`는 설계 참고 자료이며 **레거시 호환 대상이 아니다**. 새로운 구조에 불필요한 registry·workflow engine·CLI·형식·이름은 이어받지 않는다.

사용 의도에 따라 **Task / Spec / Combined** 중 필요한 기능만 수행한다. 단일 수정·일상 코딩에는 기록과 단계 생성을 요구하지 않는다. Task만 할 때 Spec 자원을 읽지 않고, Spec만 할 때 백로그를 만들지 않는다. 프레임워크는 저장소의 상위 지침이나 프로젝트 테스트·코드 개발 절차를 대체하지 않는다.

## Storage and Human Readability

사용자가 작업 디렉터리와 스펙 디렉터리를 결정한다. Git이 있으면 각 저장소의 **branch/ref도 사용자 선택**이다. Task와 Spec은 코드와 같은 브랜치에 있어도, 각각 별도의 브랜치에 있어도 된다. 특정 `.work/`, `spec/` 또는 별도 설정 파일은 기본 생성하지 않는다.

- 파일 작업 전 실제 repository/workspace, **경로와 ref**를 확인한다. 사용자가 이전에 선택한 위치나 프로젝트 지침이 명확하면 재사용하고, 위치가 불분명하면 쓰기 전에 확인한다.
- 읽기·수정은 **선택된 ref의 정본**에서 수행한다. 접근할 수 없는 ref를 `main`이나 현재 checkout으로 대체하지 않는다. Git CLI가 없어도 허용된 파일/원격 Git 도구로 가능한 범위만 수행한다.
- 작업의 식별자는 **Task root에서의 상대 파일 경로**다. 파일명·H1은 사람이 의미를 이해할 수 있게 작성하고, 경로가 같은 파일을 중복 등록하지 않는다. 이름·이동이 바뀌면 `depends_on` 참조를 함께 갱신한다.
- Git은 기록·diff·branch를 제공하지만 작업 lock이나 교차 ref 트랜잭션은 제공하지 않는다. 같은 파일의 경쟁 변경, stale spec, 조건부 쓰기 실패는 확인하고 임의 덮어쓰지 않는다.

### Task File

```markdown
---
status: todo
depends_on: [backend/db-schema]
---
# 로그인 API 구현

로그인 요청을 처리하고 정상·실패 응답을 검증한다.

## 다음 행동
- DB 스키마 완료를 확인하고 API를 구현한다.
```

필수는 **명확한 제목과 `status`**뿐이다. 완료 조건·다음 행동은 실질적 가치가 있을 때 적는다. `depends_on`은 선택한 task root 기준 상대 경로(확장자 제외), `priority`는 선택적이다. 사람이 읽는 제목·목적·진행 근거를 불투명 ID·장황한 metadata로 대체하지 않는다.

`todo | doing | done | cancelled`만 저장한다. `todo`에서 확인된 선행 작업이 모두 `done`이면 **ready**, 미완료·취소된 선행 작업 등은 **blocked**, 참조 누락·순환·조회 실패는 **unknown**으로 계산한다. `doing`은 새 대기 작업이 아니라 **재개 후보**다. 고우선순위라는 이유로 blocked를 우회하지 않는다.

작업을 진행할 때 필요한 경우에만 **확인한 사실 / 남은 일 / 다음 행동**을 해당 파일에 짧게 남긴다. 재개 시 기록만 신뢰하지 말고 선택된 ref의 현재 파일과 실제 코드·검증 결과를 다시 확인한다. 완료된 작업은 검증 근거를 확인한 뒤 `done`으로 바꾼다.

## Spec-driven Development

**가져올 것은 검증된 개발 의미이지 기존 파일·코드 구조가 아니다.**

사용자가 선택한 `spec-root` 안에서 다음 두 책임을 분리한다.

```text
<spec-root>/
  changes/<change-name>/specs/<domain-path>/spec.md
  specs/<domain-path>/spec.md
```

- **Change**는 현재 제안·구현 중인 요구사항의 **delta**이고, **Domain Spec**은 반영 완료된 기대 동작의 정본이다. `domain-path`는 필요한 만큼 중첩한다.
- 명세가 필요한 변경에서는 관찰 가능한 요구사항 → 적합한 테스트/구현 → 증거 기반 Review를 수행한다. Proposal, Research, Plan, Test Design은 **필요할 때만** 문서로 만들고, 8단계 파이프라인을 필수로 요구하지 않는다.
- Review에서 결함을 발견하면 영향을 받은 요구사항·테스트·코드만 수정·재확인한다. 정상적인 test-first red와 실제 결함을 구분한다.
- 요구사항 delta를 장기 정본에 반영하려면 완료 조건·실제 검증 증거와 정본의 **현재 버전**을 확인한다. 오래된 baseline, 권한 불명, 충돌 또는 미검증이면 덮어쓰거나 완료를 주장하지 않는다. 다른 요구사항은 보존한다.
- 완료한 change 기록의 보관·정리는 **프로젝트가 정한다**. `changes/archive/`를 기본 강제하지 않는다. Git 이력은 활용하되 Git이 없는 환경에서 없는 기록을 있다고 주장하지 않는다.
- Task 파일과 Change/Domain Spec은 같은 객체가 아니다. 필요하면 사람이 읽을 수 있는 링크로 연결하되, 1:1 매핑·교차 브랜치 자동 상태 변경·별도 추적 테이블은 만들지 않는다.

## Baseline Workflow — Tuned from Mols Loops

모든 실제 개발 실행에 적용할 **기준 흐름은 하나**다. 범용 `mols-loops`의 Prepare → RPI(Research / Plan / Work / Review) → Finalize를 개인 프로젝트의 Task·Spec·Code 관점으로 줄인다. **별도 Skill 의존성이나 중첩 루프 조율은 만들지 않는다.**

- **Prepare:** 목표·수락 조건·Task/Spec/Code의 경로/ref를 확인하고 Task-only / Spec-only / Combined / Small edit을 선택한다. blocked/unknown 작업은 착수하지 않는다.
- **RPI:** 필요한 자료만 조사하고 최소 작업 범위를 정한 뒤 실제 Task/Spec/Code를 수정·Review한다. 결함은 해당 지점으로만 돌아가며 매번 모든 단계를 반복하지 않는다.
- **Finalize:** 실제 검증 근거로 Spec 정본 반영과 Task 완료를 **각각 판단**하고, 미완료·차단이면 다음 행동을 기록한다. 실행하지 않은 테스트·쓰기는 완료로 보고하지 않는다.

Small edit과 작업 목록 조회는 전체 루프나 별도 문서 작성을 요구하지 않는다. 긴 작업에서도 루프 수를 채우기 위해 반복하지 않으며 진전이 없으면 인계한다. 범용 `mols-loops`가 함께 선택되면 외부 Run 조율은 그 Skill이 담당하고 이 기본 흐름은 도메인 Work 절차를 제공한다.

실제 작성 원본은 [Default Workflow](../../../src/rulesync/.rulesync/skills/mols-project-workflow/references/default-workflow.md)이며, 통합 [SKILL.md](../../../src/rulesync/.rulesync/skills/mols-project-workflow/SKILL.md)에서 다단계 변경 시에만 읽는다.

## Minimal Package

재사용 Rulesync source: `src/rulesync/.rulesync/skills/mols-project-workflow/`.

- **하나의 발견 가능한 `SKILL.md`**와 다단계 개발에만 로드하는 `references/default-workflow.md`를 둔다. 후속 Spec 상세 자료는 실제 context 절감 가치가 있을 때만 추가한다.
- **드랍:** 구 Skill 호환 layer·alias·migration, `artifacts.json`, 범용 8단계 workflow JSON/검사기(`flow.py`), 필수 proposal/research/plan/test-design 템플릿, Beads/Dolt/DB/MCP, scheduler·claim·lock, 별도 dashboard/index.
- 기존 `store.py`는 **자동 이관하지 않는다**. 명세 흡수에서 실제 반복 오류나 여러 파일 동시 수정 위험이 확인될 때만 작고 테스트 가능한 보조 도구를 채택한다. 어떤 환경에서도 실제 읽기·검증·쓰기 성공 여부를 구분한다.
- 새 Skill이 목표 동작을 검증받으면 **같은 PR에서** 구 `mols-spec-stdd` source·유지보수 문서·tests·eval·route 참조를 정리한다. 구 Skill을 병행 제공하거나 호환용 stub·deprecated alias·변환 도구를 남기지 않는다.

## Validation Focus

| 사용 사례 | 성공 조건 |
| --- | --- |
| Task-only | 사용자가 선택한 경로/ref에서 5개 작업을 구분·선택·재개; Spec 파일 생성 없음 |
| Spec-only | Task 파일 없이 계층형 delta 작성, 부분 변경 Review, 최신 정본에 안전하게 반영 |
| Combined | Task에서 필요한 Change를 연결하되 상태 정본을 중복 저장하지 않음 |
| Small edit | 불필요한 task/spec 파일, 전체 workflow, 추가 설정 생성 없음 |
| Branch & resume | Task·Spec·Code ref가 달라도 정확한 ref의 파일을 사용하고 오래된 상태를 재확인 |
| Invalid state | 누락·순환 의존, 취소 선행 작업, stale spec, 잘못된 완료 근거를 성공으로 판정하지 않음 |
| Human readability | 파일명·제목·짧은 본문·diff만으로 작업의 목적과 현재 상황을 파악 가능 |

실제 런타임에서 관찰하지 않은 동작은 **미검증**으로 기록한다. 현재 `SKILL.md`와 기본 워크플로 원본은 PR에 초안으로 작성되었으나, 실제 기능 검증·기존 Spec 패키지 정리·route 반영은 미완료다. 이 문서는 실행 정본이 아닌 설계 근거다.
