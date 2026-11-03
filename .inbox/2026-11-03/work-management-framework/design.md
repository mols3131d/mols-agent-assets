---
description: Beads의 의존성·ready queue·작업 재개 원칙을 참고해 소규모 프로젝트용 파일·Git 기반 Work Management Skill을 설계합니다.
---

# Work Management — Lightweight Design

## Goal and Scope

개인 토이 프로젝트나 **소규모·국지적인 개발 작업**에서 여러 할 일을 잊지 않고, 막힌 일을 건너뛰고, 다음 세션에 이어서 진행하는 재사용 Skill `mols-work-management`를 만든다. **하나의 작업 파일이 상태 정본이고 Git은 선택적인 이력·협업 수단**이다. GitHub Issues, Beads, 서버, DB, MCP, 전용 CLI는 필요하지 않다.

작업 수가 적고 한 번에 끝나는 변경이면 이 Skill이나 기록을 강제하지 않는다. 이미 프로젝트에 task 관리 정본이 있다면 별도 저장소를 무단 도입하지 않는다. Skill이 관리할 대상은 **작업 간** 선택·차단·진행·재개이며, 개별 작업 안의 RPI, 스펙·테스트·구현 절차는 기존 프로젝트·선택된 Skill이 소유한다. `mols-spec-stdd`와 서로 필수 의존성은 없다.

## What to Reuse from Beads

[Beads Quick Start](https://github.com/gastownhall/beads/blob/main/docs/getting-started/quickstart.md)와 [Core Concepts](https://github.com/gastownhall/beads/blob/main/docs/core-concepts/index.md)를 설계 **참고 자료**로 사용한다. 실제 구현이나 실행 의존성은 없다.

| Beads에서 배울 점 | 경량 구현 |
| --- | --- |
| 작업 하나에 식별자·상태·설명 | Markdown 파일 하나 |
| `blocks` 관계와 `ready` 목록 | 선택적 `depends_on`; 완료된 선행 작업만 통과 |
| 시작·완료의 명시적 전환 | `todo → doing → done`, 취소는 `cancelled` |
| 컨텍스트 손실 후 재개 | 작업 파일의 짧은 현재 상황·다음 행동 |
| 충돌을 피하는 안정적 ID | 파일명에서 정한 고정 ID; 중복 확인 |

**버리는 것:** Dolt 저장소·동기화, 분산 claim/lock, 서버·MCP/CLI, 자동 스케줄러, 유형별 의존 그래프, epics/molecules/formulas/gates, 복잡한 우선순위·담당자·마일스톤 체계. Git은 Beads의 Dolt 트랜잭션이나 동시 작성 보장을 제공하지 않는다.

## Smallest Durable Format

기존 프로젝트 작업 경로를 우선한다. 새로 채택한다면 `.work/` 아래에 **작업당 Markdown 파일 하나**만 둔다. `items/`, 인덱스, 상태 DB, 일지·아카이브 디렉터리를 기본 생성하지 않는다.

```text
.work/
  setup-db.md
  auth-api.md
```

`auth-api.md` 예시:

```markdown
---
status: todo
depends_on: [setup-db]
---
# 인증 API 만들기

완료 조건: 인증 엔드포인트가 의도한 입력과 오류를 처리한다.

다음 행동: DB 스키마가 준비되면 API 구현을 시작한다.
```

- **ID는 파일명**(`auth-api`)으로 정한다. 본문에 별도 `id`를 복제하지 않는다. ID를 바꾸려면 모든 참조를 함께 갱신한다.
- 필수는 **제목과 상태**다. 완료 조건은 작업이 모호할 때 명시하고, 상태를 `done`으로 바꿀 때 실제 확인 근거를 살핀다.
- `depends_on`은 필요한 작업에만 두는 선택적 ID 배열이며 없으면 선행 관계가 없는 것으로 본다. 우선순위도 실제 필요할 때만 `priority: high | normal | low`로 둔다. 상태 필드와 이름에 과도한 스키마 검증을 요구하지 않는다.
- 상태는 `todo | doing | done | cancelled` 네 개만 사용한다. 중단·일시 보류는 상태를 추가하지 않고 간단한 **현재 상황/다음 행동**을 본문에 남긴다. `cancelled`는 의존성을 완료시키지 않는다.
- 큰 작업의 분해는 새 작업 파일로 수행하고, 관련된 부모·스펙·PR은 본문 링크로 연결한다. 계층 ID나 별도 registry를 강제하지 않는다.
- 완료한 작업 파일은 기본적으로 그대로 보존한다. Git 이력이 있다고 해서 기록 삭제·별도 아카이브를 자동 실행하지 않는다. 수명이 끝난 기록 정리는 프로젝트가 결정한다.

## Ready and Next-Work Decision

Beads의 `ready` 개념을 최소한으로 빌린다. 이는 **계산된 판단**이지 저장되는 상태가 아니다.

1. `todo` 중 모든 `depends_on`이 `done`이고 확인된 외부 blocker가 없는 항목만 **ready**다.
2. 완료되지 않은 의존 작업, `cancelled` 선행 작업, 명시된 외부 blocker가 있으면 **blocked**다. 누락된 참조·순환 관계·파일 접근 불가 등으로 판단할 수 없으면 **unknown**이다. 불명확한 항목을 ready로 추측하지 않는다.
3. ready 후보 사이에서는 사용자의 현재 목표를 우선하고, 필요할 때만 선택적 priority를 참고한다. 고우선순위여도 blocked면 선택하지 않는다.
4. `doing` 작업은 새 ready 후보로 취급하지 않고 **진행 중인 작업의 재개 후보**로 따로 제시한다. 동일 작업의 중복 수행을 피하되 전역 독점권이 있다고 주장하지 않는다.
5. 작업 목록이 적으면 파일을 읽고 판단한다. 별도의 그래프 엔진·캐시·`ready` 영속 파일을 기본 구현하지 않는다.

## Lightweight Agent Loop

`discover → choose → work → note → resume`를 기본 작업 경험으로 삼되, 각 단계가 새로운 문서나 Git commit을 요구하지는 않는다.

1. **Discover:** 기존 작업 루트, 현재 Git ref 및 관련 작업만 확인한다. 단일 단기 작업이면 파일을 만들지 않고 진행할 수 있다.
2. **Choose:** 진행 중인 작업과 ready 후보를 확인하고 하나를 선택한다. 필요하면 분해하거나 `depends_on`을 추가한다.
3. **Work:** 선택한 한 작업 내부 방법론은 소비자 프로젝트에 맡긴다. 시작 시 `doing`, 근거가 있는 완료 시 `done`으로 바꾼다.
4. **Note:** 중단하거나 다음 세션에 필요한 경우에만 **마지막으로 확인한 것 / 남은 것 / 다음 행동**을 해당 파일에 짧게 갱신한다. 같은 사실을 별도 인계 파일로 복제하지 않는다.
5. **Resume:** 다음 세션에는 기록만 믿지 말고 현재 파일, 실제 산출물, 접근 가능한 Git 변경을 다시 확인한다. 이미 바뀐 작업·의존성에 맞춰 재판단한다.

Git은 기존 프로젝트의 commit·branch·merge 정책에 따르며 **작업마다 commit/branch/PR을 만들지 않는다.** 동일 파일에 병렬 변경이 있으면 최신 상태와 충돌을 확인하고 무단 덮어쓰지 않는다. Git은 lock이나 atomic claim이 아니며 동시 작업자 간 중복 실행을 완전히 예방할 수 없다.

CLI가 없어도 허용된 파일 read/write를 제공하는 ChatGPT Chat 등의 환경에서 같은 계약을 적용할 수 있다. 파일 읽기/쓰기도 제공되지 않으면 제안·인계까지만 수행하고 저장/커밋을 주장하지 않는다. 외부 Git 연결·계정·작성 명의를 임의로 바꾸지 않는다.

## First Build and Checks

- 처음에는 **독립적인 `SKILL.md` 한 개**: `src/rulesync/.rulesync/skills/mols-work-management/SKILL.md`. 실행 전제는 대상 프로젝트의 허용된 파일 접근뿐이다. 배포·설치와 작성 원본을 구별한다.
- 스크립트·config·provider adapter·운영 가이드는 실제 반복되는 불편이나 오류가 확인되기 전에는 만들지 않는다.
- 소규모 작업 5개로 다음을 검토한다: (1) 선행 작업과 ready 선택, (2) 막힌 고우선순위 작업, (3) 누락/순환 참조, (4) `doing` 재개와 오래된 인계, (5) Git branch 간 같은 파일 수정, (6) 파일 접근만 가능한 ChatGPT, (7) 단일 수정·Spec/Test-driven·build task 비활성화.
- 대안 비교의 기준은 **기록 파일·필드·사용자 조작·에이전트 호출 수가 최소인지**, 잘못된 ready가 없는지, 다음 세션에서 복구 가능한지다. 과도한 방어 장치보다 소규모 작업의 실제 사용 편의를 우선한다.
- 문서 설계 검토와 실제 실행 평가를 분리해 기록한다. 이 문서는 `.inbox/`의 근거이며, 작성 원본이 아닌 실행 지침으로 사용하지 않는다.
