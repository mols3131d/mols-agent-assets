---
name: mols-stdd
description: >-
  Manage personal project tasks and spec/test-driven software changes in a
  lightweight workflow. Use to bootstrap user-chosen task/spec directories
  and Git refs, select and resume dependent work, evolve domain specs, and
  guide implementation and review. Do not use for routine one-off code edits
  without work-management or specification needs, enterprise scheduling,
  standalone test review, or build-task execution.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Personal Spec/Test-driven Development

사용자가 선택한 파일·Git 환경에서 **작업 관리(Task) / 명세 기반 개발(Spec) / 통합 개발(Combined)**을 수행한다. 개인 프로젝트에 필요한 기능만 적용하고 단일·단기 수정에 문서·루프를 강제하지 않는다. 기존 프로젝트의 지침과 실제 테스트·Git 권한이 우선한다.

## Select the Work

- **Task-only:** 작업 발견·분해·우선순위·선행 관계·중단·재개·상태 갱신. 스펙 문서를 만들지 않는다.
- **Spec-only:** 요구사항 변경, 테스트·구현·Review, 도메인 정본 갱신. Task 파일을 만들지 않는다.
- **Combined:** 진행할 작업을 선택하고 그 작업에 실제 스펙 변경이 필요할 때만 Spec 절차를 수행한다. 서로 다른 상태를 복제하지 않고 링크로 연결한다.
- **Small edit:** 작업 관리나 명세가 필요 없는 간단한 수정에는 이 Skill의 기록·절차를 활성화하지 않는다.

**여러 단계의 개발 변경 또는 반복 검토가 필요한 작업**에는 [Default Workflow](references/default-workflow.md)를 적용한다. 단순 조회·상태 갱신·작은 변경은 해당 절차의 필요한 판단만 사용한다. 이 Skill은 범용 `mols-loops`의 설치나 별도 런타임을 요구하지 않는다.

## Bootstrap — First Use

프로젝트에 처음 도입하거나 Task/Spec 저장 위치를 설정해 달라는 요청에는 [Project Bootstrap](references/bootstrap.md)을 **먼저 읽고 적용**한다.

1. 기존 프로젝트의 실제 Task/Spec 정본과 Git 상태를 확인한다. 사용할 기능이 Task-only인지 Spec-only인지 Combined인지 결정한다.
2. 사용자에게 **필요한 디렉터리와 선택적 Git ref**를 고르게 한다. 이미 명확히 선택했으면 다시 묻지 않는다. 지정되지 않은 경로나 브랜치 이름을 기본값으로 확정하지 않는다.
3. 선택된 `repo/ref/root`별로 최소한의 최초 파일만 생성한다. Task는 **작업당 Markdown 하나**, Spec은 **실제로 필요한 `changes/<change>/specs/<domain>/spec.md`**부터 시작한다. 아직 검증되지 않은 Domain Spec은 미리 만들지 않는다.
4. 지정 ref에서 생성 결과를 다시 확인하고 위치·생성 파일·다음 행동을 보고한다. 별도 index/manifest·고정 루트·샘플 작업·빈 디렉터리는 강제하지 않는다.

저장 위치가 결정되지 않았으면 **후보 구조를 예시로 제시하고 기록은 보류**한다. 최초 작업·변경이 없는 빈 프로젝트는 필요할 경우 선택한 위치만 합의하고, 사용자가 영속적인 빈 부트스트랩을 명시적으로 원할 때만 README를 둘 수 있다.

## Locations and Ref Safety

Task와 Spec 저장 위치는 **사용자가 지정**한다. 작업 디렉터리, Spec root, 코드 ref는 같아도 달라도 된다. 저장소·워크스페이스와 각각의 대상 경로·Git ref를 확인하고 해당 경로만 수정한다. 불명확한 위치나 없는 branch를 추측해 만들거나, 접근할 수 없는 지정 ref 대신 기본 branch에 쓰지 않는다. 별도 설정 파일·고정 `.work/`·`spec/` 경로를 만들지 않는다.

허용된 로컬 파일 도구 또는 연결된 Git 도구만 사용한다. 수정 전 실제 계정·권한·최신 버전을 확인하며, commit·branch·PR은 사용자와 프로젝트의 운영 방식에 따른다. Git은 lock이나 서로 다른 ref에 대한 원자적 완료를 보장하지 않는다.

## Task Contract

Task root 아래의 `<relative-path>.md` 하나가 하나의 작업 정본이다. **파일명/경로가 ID**, H1은 사람이 이해하는 제목이다. 최소 메타데이터는 `status: todo | doing | done | cancelled`; 필요할 때만 `depends_on: [<relative-path-without-extension>]`과 우선순위를 사용한다.

- `todo`의 모든 선행 항목이 `done`이고 알려진 외부 차단이 없으면 **ready**. 선행 미완료·취소·외부 차단은 **blocked**, 누락·순환·조회 불가는 **unknown**. 이 판단은 파일에 저장하지 않는다.
- `doing`은 재개 대상이다. 원본 파일과 실제 산출물을 다시 확인하고, **현재 사실·남은 것·다음 행동**을 필요할 때만 짧게 갱신한다.
- 파일 이동·개명 시 의존 참조를 갱신한다. blocker와 unknown을 우선순위로 무시하지 않는다. 실제 완료 근거 없이 `done`을 기록하지 않는다.

작업 제목·목적·완료 조건은 독자가 에디터나 Git diff에서 이해할 수 있게 표현한다. 별도 DB·인덱스·대시보드는 만들지 않는다.

## Spec Contract

사용자 지정 `spec-root`에서 `changes/<change-name>/specs/<domain-path>/spec.md`는 진행 중 **요구사항 delta**, `specs/<domain-path>/spec.md`는 반영된 **장기 도메인 정본**이다. 도메인 경로는 필요한 만큼 중첩할 수 있다. 기존 프로젝트의 정본 구조가 따로 있으면 중복 저장소를 무단 생성하지 않는다.

- 의미 있는 동작 변경에는 기대 동작·수락 조건을 명시하고, 테스트·구현 결과와 대조해 Review한다. 추가 proposal/research/plan/test-design 파일은 필요한 경우만 만든다.
- Review finding은 영향을 받은 명세·테스트·코드로 되돌린다. 무관한 개발 단계를 반복하지 않는다.
- 요구사항 delta에는 추가·수정·삭제 대상과 수락 기준을 구분하고, 현재 정본의 기준 버전 또는 내용을 추적할 근거를 남긴다. 새 요구사항은 최초 정본이 없어도 명시적으로 검증한다.
- 정본 반영 전 실제 검증 근거·현재 정본·delta의 기준 내용을 확인한다. stale 변경, 충돌, 권한 부족, 불완전한 검증이 있으면 무단 반영하지 않는다. 영향받지 않은 요구사항은 보존하고 삭제·교체는 영향 범위를 확인한다.
- 완료한 change 파일의 보관·삭제는 프로젝트가 결정한다. Task `done`은 Spec 반영의 근거가 아니며 Spec 반영이 다른 Task를 자동 완료시키지도 않는다.

## Completion

결과는 수행한 파일 작업과 실제 검증, 누락·차단 사항, 다음 행동으로 구분하여 보고한다. 실행하지 않은 도구나 확인하지 않은 ref를 성공으로 주장하지 않는다. 이 Skill의 실행 흐름은 `mols-loops`에서 영감을 얻은 **도메인별 로컬 적용**이며, 외부 Skill에 숨은 필수 의존성을 두지 않는다.
