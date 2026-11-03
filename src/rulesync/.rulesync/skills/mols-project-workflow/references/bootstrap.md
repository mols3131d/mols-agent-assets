# Project Bootstrap

새 프로젝트에서 `mols-project-workflow`를 시작하거나 기존 프로젝트에 Task/Spec 저장소를 처음 마련할 때만 사용한다. **설치·초기화 명령은 필요하지 않다.** 사용자가 선택한 디렉터리와 Git ref에 읽기 쉬운 Markdown 정본을 만드는 것이 부트스트랩이다. 이미 설정된 프로젝트를 매번 재초기화하지 않는다.

## 1. Decide What to Use

먼저 프로젝트의 지침, 현재 저장소·ref, 기존 작업 목록과 스펙 정본을 확인한다. **새 저장소를 만들기 전에 기존 owner를 재사용할지 판단한다.** 요청에 필요한 영역만 준비한다.

| 사용 목적 | 사용자에게 받아야 할 위치 | 생성할 수 있는 정본 |
| --- | --- | --- |
| Task 관리 | Task root (디렉터리)와 사용하려는 Git ref | `<task-root>/<work-item>.md` |
| Spec-driven | Spec root (디렉터리)와 사용하려는 Git ref | `<spec-root>/changes/...`, `<spec-root>/specs/...` |
| 둘 다 | 각 root와 ref. 같아도 되고 달라도 됨 | 필요한 쪽의 Markdown만 |
| 단순 변경 | 새 저장소 선택 불필요 | 초기화하지 않음 |

Git을 사용하지 않는 프로젝트는 **workspace + 디렉터리**만 결정하면 된다. Git 프로젝트에서는 **repository + ref + 디렉터리**로 실제 파일 위치를 식별한다. 코드가 있는 ref도 구현 시 확인하되, 별도의 Task/Spec 브랜치를 필수로 만들지 않는다.

- 경로를 사용자가 이미 지정했다면 그대로 사용한다. 사용자가 폴더를 결정하지 않았다면 기존 프로젝트 설정이나 명확히 합의된 경로가 있는지 먼저 찾는다. **없다면 쓰기 전에 경로를 선택받는다.**
- 제안은 가능하지만 `.work/`, `spec/`, `tasks/`, `planning/` 등 어떤 이름도 프레임워크의 기본값이 아니다. 권장 예시는 **선택지**이지 자동 생성 지시가 아니다.
- Git ref가 명시되었다면 그것을 사용한다. ref 지정 없이 현재 checkout의 작업을 요청했다면 **현재 활성 ref를 확인한 뒤** 사용할 수 있다. 확인할 수 없는 기본 브랜치나 과거 기록으로 임의 대체하지 않는다.
- 새 branch가 필요한 경우 **사용자가 선택한 이름과 출발 ref**를 확인한 뒤 권한과 프로젝트 Git 정책에 따라 생성한다. 별도 Task 브랜치를 코드 브랜치로 자동 병합하지 않는다.

## 2. Choose a Human-readable Layout

아래는 **설명용 예시**이며 이름, 깊이, 배치 모두 사용자 선택이다.

**A. 같은 브랜치에서 관리**

```text
repository: toy-api
task ref: feature/login
spec ref: feature/login
code ref: feature/login

planning/
  tasks/
    backend/
      db-schema.md
      login-api.md
  product-spec/
    changes/
      login/
        specs/
          auth/
            login/
              spec.md
    specs/
      auth/
        login/
          spec.md
```

- Task root = `planning/tasks/`; `backend/db-schema`처럼 그 root 기준 상대 경로(확장자 제외)가 작업 ID다.
- Spec root = `planning/product-spec/`. `changes/`는 변경 요구사항, `specs/`는 완료된 도메인 정본이다.
- 표시된 파일은 가능한 **최종 구조의 예시**일 뿐이다. 첫 작업에 없는 도메인이나 아직 승인되지 않은 정본을 미리 생성하지 않는다.

**B. 작업만 전용 브랜치에서 관리**

```text
repository: toy-api
task ref: personal-tasks
task root: backlog/
spec ref: feature/login
spec root: docs/specification/
code ref: feature/login

personal-tasks:backlog/backend/login-api.md
feature/login:docs/specification/changes/login/specs/auth/login/spec.md
feature/login:src/auth/login.py
```

- 동일한 repo여도 ref마다 파일 내용과 존재 여부가 다르다. branch를 선택해 읽고, **그 branch에만** 기록한다.
- 로컬 Git은 ref를 읽는 방법과 수정할 worktree/checkout을 구별한다. 도구가 해당 ref에 안전하게 쓸 수 없다면 쓰기 대신 필요한 작업을 인계한다.

## 3. Inspect, Propose, Create

1. **Inspect:** 위 위치의 실제 파일과 권한을 읽고, 기존 `status`가 있는 Task 파일·기존 `changes/`, `specs/`를 식별한다. Task root가 프로젝트 루트처럼 넓으면 unrelated Markdown을 작업으로 취급하지 않는다.
2. **Propose:** 선택된 `repo/ref/root`, 새로 만들 파일과 목적을 짧게 제시한다. 사용자가 이미 경로와 작업 내용을 명확히 요청했다면 중복 확인을 요구하지 않는다.
3. **Create only what is needed:** 초기 작업이 정해졌다면 첫 Task 파일 하나를 만들고, 요구사항 변경이 정해졌다면 해당 Change delta를 만든다. 전체 디렉터리 트리, 빈 `specs/`, 샘플 작업·가짜 완료 기록, 상태 인덱스, 설정 manifest는 자동 생성하지 않는다. Git은 빈 디렉터리를 추적하지 않는다.
4. **Empty bootstrap:** 아직 실제 작업·변경이 없다면 경로/ref 선택과 사용법 안내까지만 수행한다. 사용자가 **비어 있는 초기 저장소를 영속적으로 남기길 명시한 경우에만** 선택한 root에 짧은 `README.md`를 생성할 수 있다. 기존 README를 무단 덮어쓰지 않는다. README는 작업 인덱스나 상태 정본이 아니다.
5. **Verify:** 생성/갱신된 파일을 지정 ref에서 다시 읽어 제목·경로·상태·의존 참조를 확인한다. 작성 성공, 코드 브랜치의 변경, 테스트 실행은 각각 실제 결과로만 보고한다.

### First Task File

사용자가 `planning/tasks/backend/login-api.md`를 첫 작업으로 선택한 경우:

```markdown
---
status: todo
---
# 로그인 API 구현

로그인 요청의 정상·오류 동작을 확인한다.

## 완료 조건
- 지정된 성공·실패 사례가 검증된다.

## 다음 행동
- 로그인 API의 기존 구현과 테스트를 확인한다.
```

선행 작업이 **실제 존재하는 경우에만** frontmatter에 `depends_on: [backend/db-schema]`를 추가한다. 이때 `backend/db-schema.md`는 **같은 Task root/ref에 존재**해야 한다. 부트스트랩을 위해 가짜 선행 작업을 만들지 않는다.

### First Spec Change

사용자가 `planning/product-spec/`를 선택하고 로그인 요구사항 변경을 요청한 경우:

```text
planning/product-spec/
  changes/
    login/
      specs/
        auth/
          login/
            spec.md
```

해당 파일에는 변경될 **동작과 검증 기준**만 기록한다. 기존 `specs/auth/login/spec.md`가 있다면 먼저 읽고 차이와 현재 기준 버전을 확인한다. 없으면 새 도메인으로 취급한다. **완료되지 않은 변경을 바로 `specs/` 정본으로 복사하지 않는다.** Review·실제 검증·기준 최신성 확인 후 해당 domain spec을 반영한다.

## 4. Make It Resumable

성공한 부트스트랩을 보고할 때는 사용한 **workspace/repository, Task root/ref, Spec root/ref(해당되는 경우), 최초 생성한 파일과 현재 단계**를 표시한다. 이 정보가 새 세션에서 발견되어야 한다면 **사용자가 선택한 기존 프로젝트 안내 문서/지침**에 짧게 기록할 수 있다. 별도 프레임워크 설정 파일은 필수도 기본도 아니다.

새 세션에서는 저장된 선택을 실제 파일·ref와 대조한다. 기록이 없거나 모호하면 사용자가 선택한 경로를 재확인하고 임의의 새 root를 만들지 않는다. 권한·동시 수정·다른 계정 문제는 임의 우회하지 않는다.

## Acceptance Examples

- **Task-only:** 사용자가 `backlog/`와 `personal-tasks` ref를 선택하면 Spec 저장소 없이 작업 파일 한 건만 만든다.
- **Spec-only:** 사용자가 `docs/specs/`와 현재 코드 ref를 선택하면 Task 파일 없이 필요한 Change delta만 만든다.
- **Existing repo:** 이미 `work/`에 관리 중인 Task가 있으면 새 `planning/tasks/`를 만들지 않는다.
- **Not decided:** 사용자가 위치를 정하지 않았고 프로젝트에도 명확한 설정이 없으면 예시 후보를 보여주되 파일은 쓰지 않는다.
- **Unreachable ref:** 지정한 브랜치를 읽거나 수정할 수 없다면 다른 ref에 대신 생성하지 않는다.
- **Empty setup:** 작업·변경이 하나도 없을 때 샘플/빈 디렉터리로 완료를 꾸미지 않는다.
