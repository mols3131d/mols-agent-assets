# Change Bootstrap

프로젝트 최초 도입뿐 아니라 **기존 프로젝트에 새 Change를 발행할 때도** 사용하는 절차다. 이미 정해진 work/spec root와 정본은 다시 선택하지 않으며, 설치 명령이나 고정 저장 위치가 필요하지 않다.

## Locate and Decide

1. 프로젝트 지침과 실제 파일·Git ref를 확인한다. 기존 Work·Spec 정본의 소유자와 호환성을 확인한다. 호환되는 정본은 유지하고, 새 `work.md`가 기존 작업 상태와 이중 정본이 된다면 명시적인 정본 선택·이관 결정 전에는 만들지 않는다.
2. 이미 선택된 work root, 필요한 spec root와 각 repository/ref가 있으면 재사용한다. 처음 선택할 때는 사용자 결정에 따르며 같은 디렉터리·ref 또는 별도 위치를 허용한다. 코드 ref는 구현할 때 확인한다. Git이 없으면 workspace와 경로를 사용한다.
3. 이미 선택된 위치는 다시 묻지 않는다. 결정되지 않았고 기존 소유자도 없으면 후보를 제시하고 **쓰기 전에 선택받는다**. `.work/`, `tasks/`, `spec/` 또는 특정 branch를 기본값으로 강제하지 않는다. 결정되지 않은 위치를 추정해 생성하거나 기존 상태를 자동 이관하지 않는다.
4. 지정 ref를 읽고 현재 상태·권한을 확인한다. tag·commit처럼 직접 쓸 수 없는 ref에 기록하지 않는다. 새 branch가 필요하면 이름과 출발 ref를 확인하고 승인된 범위에서 만든다. 다른 계정·branch를 대체 수단으로 쓰지 않는다.

## Single Change Layout

```text
repository: toy-api
work root: planning/    ref: feature/login
spec root: planning/    ref: feature/login

planning/
  changes/
    backend/
      login/
        work.md
        specs/
          auth/
            login/
              spec.md
  specs/
    auth/
      login/
        spec.md
```

`backend/login`은 하나의 Change ID다. `work.md`는 진행 정본, 변경 하위 `specs/`는 필요한 명세 delta, 최상위 `specs/`는 검증된 도메인 정본이다. **예시의 전체 트리를 미리 만들지 않는다.** 행동 계약 변경이 없으면 `work.md`만 있고, 검증 전에는 도메인 정본을 미리 만들지 않는다.

서로 다른 repository/ref를 선택하더라도 동일 ID와 하나의 상태 정본을 유지한다. 아래 경로는 같은 repository의 서로 다른 ref 예시다.

```text
personal-work:backlog/changes/backend/login/work.md
feature/login:docs/behavior/changes/backend/login/specs/auth/login/spec.md
feature/login:docs/behavior/specs/auth/login/spec.md   # 검증 후
```

각 ref의 파일 존재·읽기·쓰기 결과를 따로 확인한다. 명세 delta에 작업 상태를 복제하거나 서로 다른 ref의 자동 완료를 가정하지 않는다.

## First Record

1. 선택한 root/ref에서 기존 `changes/**/work.md`와 목표가 겹치는 Change를 확인한다. 동일 ID나 동일 목적의 티켓을 중복 발행하지 않고 기존 기록의 재사용·수정·재개를 검토한다. 아무 Markdown이나 Change로 간주하지 않는다. Change ID·도메인 경로가 절대 경로·`..`·심볼릭 링크를 통해 선택한 root 밖을 가리키지 않는지 확인한다.
2. 실제 목표가 있을 때 `changes/<id>/work.md`를 발행한다. 최소한 H1과 `status: todo`를 사용하고 목표·완료 조건·다음 행동을 구체화한다. `depends_on`은 실제로 존재하는 선행 Change에만 쓴다. 발행만 요청받았다면 `doing`으로 전환하거나 구현·Agent 실행을 시작하지 않는다.
3. 행동 요구사항을 실제로 변경할 때만 동일 ID에 명세 delta를 추가한다. 발행만 요청받았으면 추측한 delta를 미리 만들지 않는다. 기존 정본이 있으면 먼저 읽어 기준을 확인하고, 신규 도메인이라면 정본 부재를 신규 요구사항의 근거로 구분한다. 검증 전에는 정본으로 흡수하지 않는다.
4. 작성 결과를 **선택한 각 ref에서 재조회**하고 생성 파일·현재 상태·다음 행동을 보고한다.

첫 변경이 없으면 경로/ref를 결정한 뒤 파일은 만들지 않는다. 가짜 Change·빈 폴더·샘플 명세를 자동 생성하지 않는다. 사용자가 영속적인 빈 설정을 명시적으로 요청한 경우에만 선택한 위치에 짧은 README를 둘 수 있다.

```markdown
---
status: todo
---
# 로그인 API 구현

성공과 인증 실패 응답을 구현한다.

## 완료 조건
- 성공·실패 사례가 실제 테스트로 검증된다.

## 다음 행동
- 현재 API 계약과 테스트를 확인한다.
```

새 세션은 선택된 repository/ref/root와 `doing` Change를 실제 파일과 대조한다. 별도 위치를 다시 발견하기 어렵다면 기존 프로젝트 안내 문서나 해당 `work.md`에 repository/ref/root를 선택적으로 기록한다. 별도 설정 파일이나 상태 registry는 만들지 않는다.
