---
name: mols-stdd
description: >-
  Manage personal-project Changes as ticket-like work items: issue and select
  ready work, assign or delegate agent execution, resume and verify results,
  and connect dependencies, specifications, tests, review, and completion.
  Use for project bootstrap, work backlogs, agent task assignment, and
  spec/test-driven multi-step changes with nested domain specs. Not for
  trivial one-off edits, standalone test critiques, enterprise scheduling,
  automatic task-queue engines, or build-command configuration.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Mols STDD

개인 프로젝트의 **Change 하나**에서 티켓 발행·작업 선택·할당·진행·명세·테스트·구현·Review·완료를 연결한다. 작업과 명세를 별도 모드나 이중 상태로 관리하지 않는다. 작업 규모에 따라 필요한 근거와 파일만 작성한다. 기존 프로젝트 지침, 실제 코드·테스트, 명세 정본과 Git 권한을 우선한다.

## One Change, One State

Change는 함께 검증·완료해야 하는 결과를 단위로 잡는다. 파일·컴포넌트 수로 나누지 않고 수락 조건을 독립적으로 검증·종료할 수 있는 변경은 분리한다. 서로 선행 관계라면 `depends_on`으로 연결하고, 여러 도메인이 하나의 완료 조건에 결합되면 같은 Change로 관리한다.

사용자 지정 root에서 상대 경로 `<change-id>` 하나가 변경을 식별한다. 계층형 ID를 허용한다.

```text
<work-root>/changes/<change-id>/work.md                 # 변경 상태·완료 조건·다음 행동
<spec-root>/changes/<change-id>/specs/<domain>/spec.md   # 필요한 경우의 명세 delta
<spec-root>/specs/<domain>/spec.md                       # 검증 후 유지하는 도메인 정본
```

Work와 Spec root는 같아도, 별도 디렉터리·Git ref여도 된다. **같은 Change ID**를 사용하고 별도 Task ID·연결 테이블·중복 상태를 만들지 않는다. Change ID·도메인 경로·의존 참조는 선택한 root 내부의 정규화된 상대 경로여야 한다. 절대 경로, `.`·`..` 구간, root 밖으로 나가는 심볼릭 링크는 허용하지 않는다. 기존 프로젝트가 명세 정본을 관리한다면 두 번째 정본을 만들지 않고 기존 구조를 따른다. 기존 작업 상태 정본도 중복 생성하지 않는다. 기존 Work 구조가 이 계약과 호환되지 않으면 상태 정본을 선택·이관하기 전에는 별도 `work.md`를 추가하지 않는다. 코드·테스트는 프로젝트가 정한 원래 위치에 둔다.

`work.md`는 **유일한 진행 상태 정본**이다. 사람이 읽을 수 있는 제목·목표·완료 조건·다음 행동을 필요한 만큼 적는다.

```markdown
---
status: doing
depends_on: [backend/db-schema]
---
# 로그인 API 구현

정상·실패 응답을 구현하고 검증한다.

## 완료 조건
- 성공·실패 응답이 검증된다.

## 다음 행동
- 인증 실패 테스트 결과를 확인한다.
```

`status: todo | doing | done | cancelled`만 저장한다. 선택적 `depends_on`은 같은 work root/ref의 Change ID(확장자 제외)를 참조한다. 선행 변경이 모두 `done`이고 외부 차단이 없는 `todo`는 ready, 미완료·취소된 선행 변경은 blocked, 누락·순환·조회 실패는 unknown으로 **계산**한다. 이 파생 상태는 저장하지 않는다. `doing`을 재개할 때는 기록뿐 아니라 실제 코드·검증 결과와 이전 실행의 종료 여부를 재확인한다. 이름을 바꾸면 의존 참조도 갱신한다.

## Ticket and Agent Dispatch

티켓은 기존 Change이며, 발행은 `todo` 기록이지 GitHub Issue 생성이나 작업 실행이 아니다. 실행 요청이 없다면 명세·코드 작업이나 Agent 호출을 시작하지 않는다. 실행할 Change는 실제 `doing`의 미종료 실행과 선행 의존·차단 여부를 확인해 선택한다. 파생 `ready`는 **실행 후보**이지 선점·권한·실행 시작의 증거가 아니다.

할당 대상은 실제로 사용 가능한 실행 주체여야 한다. 세션 간 지정 보존이 필요하고 다른 할당 정본이 없다면 선택적 `assignee`를 기록할 수 있지만 상태·실행 승인·독점 Claim을 대신하지 않는다. 작업 선택·할당·실행 위임·인계에는 [Dispatch](references/dispatch.md)를 조건부로 읽고 런타임의 네이티브 위임·격리·Claim 능력과 실제 권한을 확인한다. 단일 에이전트는 직접 수행할 수 있다.

## Requirement and Evidence

행동 계약이 바뀌면 같은 Change ID 아래 해당 도메인의 delta를 기록한다. 새 요구사항·수정·삭제, 수락 조건과 기존 정본의 기준 버전·내용을 구분한다. 한 Change가 여러 하위 도메인을 바꿀 수 있다. **명세 delta는 독립 작업이 아니라 Change의 검증 근거**다. 명세가 불필요한 변경에는 빈 Spec을 만들지 않는다. 신규 도메인에는 기존 정본이 없음을 확인해 신규 요구사항으로 기록하며, 존재하지 않는 baseline을 만들어내지 않는다.

요구사항, 적절한 테스트, 구현, Review를 대조한다. Test-first의 정상적인 red와 실제 결함을 구분하고, 결함 발견 시 영향받은 명세·테스트·코드만 재검토한다. Proposal, Research, Plan, Test Design 문서는 유용할 때만 남긴다.

Delta 작성 시 수정 대상 요구사항의 변경 전 내용이나 정본 revision 등 **비교 가능한 기준**을 남긴다. 반영 전 최신 정본·기준·검증 근거를 대조하고, 검증된 요구사항만 병합하며 무관한 부분은 보존한다. stale baseline·충돌·권한 부족·미검증이면 덮어쓰지 않는다. 최신 정본 변경이 해당 요구사항과 충돌하지 않음을 확인한 경우에만 비교 기준과 필요한 검증을 갱신해 반영할 수 있다. 재개 시 이미 반영된 내용이 실제 정본과 일치하면 재적용하지 않고, 적용 여부가 불명확하면 완료를 보류한다. 완료한 Change 기록의 보관·삭제는 프로젝트가 정한다.

**`done`은 필요한 테스트·구현·Review 및 명세 반영이 모두 확인된 후에만 기록한다.** 완료 기록을 쓰기 직전에도 `work.md`의 최신 내용을 재확인하고 충돌을 덮어쓰지 않는다. 명세가 없는 Change는 없는 delta의 검증을 요구하지 않는다. 여러 ref의 쓰기는 원자적이지 않으므로 일부만 성공했다면 완료를 보류하고 검증된 결과·불확실한 부분·다음 행동을 같은 `work.md`에 남긴다. 재개에 필요한 별도 repository/ref/root도 발견할 수 있어야 하되 별도 설정 파일을 강제하지 않는다.

## Bootstrap and Execution

처음 도입하거나 저장 위치를 정할 때만 [Bootstrap](references/bootstrap.md)을 읽는다. 진행·재개·다단계 변경은 [Development Workflow](references/default-workflow.md)를 적용한다. 작업 선택·할당·위임·인계를 요청받은 경우에만 [Dispatch](references/dispatch.md)를 추가로 읽는다. 단순 조회와 기록 가치가 없는 작은 수정은 별도 Change 파일·전체 루프를 강제하지 않는다. 이는 독립된 모드가 아니라 **필요한 작업량만 실행하는 동일 절차**다.

쓰기 전 실제 workspace/repository, 경로·ref, 연결 계정·권한, 최신 파일을 확인한다. 사용자 선택이나 기존 정본 없이 기본 루트·브랜치를 정하지 않는다. 지정 ref 접근 실패 시 다른 계정이나 기본 브랜치로 우회하지 않는다. `mols-loops`가 별도로 선택되면 외부 Run 제어는 그 Skill이 맡고 여기서는 Change의 도메인 절차만 제공한다.

실제 수행·검증과 미실행·실패·차단을 구분해 보고한다. 별도 DB, manifest, workflow engine, 외부 Skill 설치, 자동 cross-ref 트랜잭션을 요구하지 않는다.
