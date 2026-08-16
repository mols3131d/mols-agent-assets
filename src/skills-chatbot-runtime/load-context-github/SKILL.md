---
name: load-context-github
description: Mandatory GitHub repository-context loader. Use before any @GitHub or GitHub tool/connector/plugin/integration call and for concrete work on a specific repository, GitHub URL, file/path, PR/review, issue, branch/ref, commit/push/merge, Actions/check/workflow, release, or repository change. Before task-level action, discover repository-wide and target-path instructions such as AGENTS.md, README.md, .github/copilot-instructions.md, path-specific instructions, and referenced Git/VCS docs. Include read-only and follow-up tasks.
metadata:
  - target:
    - "OpenAI ChatGPT"
---

# Load GitHub Context

## Purpose

GitHub 관련 작업 전에 ChatGPT가 필요한 repository-specific Git/GitHub context를 로드한다.

이 skill은 **context loader**다. 구현, 리뷰, commit, PR 등 실제 작업 절차는 repository 지침과 해당 task skill에 맡긴다.

## Trigger

다음 중 하나라도 해당하면 적용한다.

- 특정 GitHub repository/resource/URL, file/path, commit/ref/branch를 읽거나 다룬다.
- Issue, pull request, review, check/CI, workflow, release 등 GitHub repository object를 읽거나 다룬다.
- 현재 conversation에서 이미 식별된 repository/PR/issue 등에 대한 follow-up 작업을 한다.
- GitHub tool/connector/plugin/integration을 호출한다. read-only 호출도 포함한다.

구체적인 GitHub target도 없고 GitHub tool도 사용하지 않는 일반 Git/GitHub 설명에는 적용하지 않는다.

GitHub integration을 context discovery에 먼저 사용할 수 있다. 단, **첫 task-level action 전에 필요한 context loading을 완료**한다.

## Directives

- 대상 repository와 필요한 ref/branch/PR/issue를 live context로 확인한다.
- Repository-specific 규칙은 기억이나 관례가 아니라 repository 파일과 관련 GitHub metadata에서 확인한다.
- 현재 task가 실제로 대상으로 하는 ref/branch의 instruction을 사용한다. PR/review에서는 head의 instruction 변경을 확인하고, 판단에 중요하면 base와 비교한다.
- Repository별 context를 격리하고, 여러 target path의 scoped instruction을 서로 누출하지 않는다.
- Branch, commit, PR, review, merge, release 규칙을 찾기 전에 관례를 추정하지 않는다.
- 요청 범위 밖의 변경이나 side effect를 만들지 않는다.
- 기존 작업, local change, commit history를 임의로 삭제하거나 덮어쓰지 않는다.
- Secret, credential, token 등 민감 정보를 output, commit, issue, PR, log에 남기지 않는다.
- Force push, history rewrite, destructive delete, permission/protection 변경은 명시적 요청 없이 수행하지 않는다.
- Merge, release, repository deletion, bulk mutation 등 큰 side effect는 사용자의 명시적 의도를 요구한다.

Repository 규칙을 찾지 못했다면 만들어내지 않는다. 안전 기본값을 사용할 수 있지만 repository 관례라고 표현하지 않는다. 상위 지침과 충돌하지 않는 범위에서 repository가 더 엄격한 규칙을 명시하면 그 규칙을 따른다.

## Load Repository Context

전체 repository를 무작정 읽지 않는다. **identify → path context → task context → search → references** 순으로 필요한 만큼만 탐색한다.

### 1. Identify

현재 작업에 필요한 대상을 식별한다.

- repository와 target ref/branch
- PR/issue 등 task object
- 변경 또는 검토 대상 path
- 작업 종류: read, review, edit, commit, PR, merge, release 등

Target path가 처음에는 없다면 root `AGENTS.md`/`README.md`와 high-signal repository instruction부터 확인한다. PR changed files처럼 path가 드러나는 즉시 해당 path context를 추가한다.

### 2. Load Path Context

Target path가 있으면 **repository root부터 target directory까지 ancestor chain 전체**를 확인한다. 파일이면 parent directory를 사용하고, directory면 그 directory 자체를 포함한다.

각 directory에서 다음을 확인한다.

- `AGENTS.md`
- 관련 `README.md`
- repository가 지정한 local/path-specific instruction
- `AGENTS.override.md`처럼 repository/tooling이 semantics를 명시한 override instruction

여러 target path는 각 chain을 따로 계산하되 shared ancestor context는 재사용한다.

#### AGENTS.md

`AGENTS.md` 계열은 agent instruction 후보로 취급한다.

- Root `AGENTS.md`: 별도 scope가 없으면 repository-wide.
- Nested `AGENTS.md`: 별도 scope가 없으면 해당 directory와 descendants.
- Target에 적용되는 ancestor `AGENTS.md`를 root → target 순으로 모두 로드한다.
- Repository/tooling이 precedence, scope, override semantics를 선언하면 그대로 따른다. semantics가 없으면 파일명만으로 override를 추정하지 않는다.
- 별도 규칙이 없다면 실제로 충돌하는 동일 주제에 한해 더 가까운 scoped instruction을 더 구체적인 규칙으로 취급한다.
- Agent/service 전용 instruction은 현재 ChatGPT 작업에도 실제로 적용되는 경우에만 사용한다.

#### README.md

`README.md`는 기본적으로 **context와 navigation source**다. 가까이 있다는 이유만으로 normative instruction이나 override가 되지 않는다.

Ancestor README에서는 현재 작업과 관련된 부분만 확인한다.

- directory/component의 목적과 경계
- local workflow 또는 사용법
- Git/GitHub 규칙
- 더 권위 있는 instruction/document로 향하는 참조

명시적 규칙은 현재 task에 직접 적용되는 범위가 분명할 때 규칙으로 적용한다. Scope가 불명확하면 proximity만으로 규범화하지 말고 context/reference로 유지한다. 참조된 필수 지침은 필요한 범위까지 따라간다.

#### Repository-Level Instructions

Task와 관련될 때 다음 high-signal 위치도 확인한다.

- Root: `CONTRIBUTING.md`, `DEVELOPMENT.md`, repository가 지정한 governance 문서
- GitHub: `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`, `.github/CONTRIBUTING.md`
- `.github/AGENTS.md`: target이 `.github/**`이거나 더 넓은 scope가 명시된 경우
- Repository가 지정한 agent/bot instruction 위치

Path selector 또는 `applyTo`가 있는 instruction은 target path가 실제로 match하는 경우에만 적용한다. 특정 agent/tool 전용 파일은 공통 repository convention인지 해당 tool 전용 동작인지 구분하며 ChatGPT 규칙으로 자동 승격하지 않는다.

### 3. Load Task Context

현재 작업에 필요한 surface만 추가로 확인한다.

- PR/review: `.github/PULL_REQUEST_TEMPLATE*`, `.github/CODEOWNERS`, review guidance
- Issue: `.github/ISSUE_TEMPLATE/`
- Commit: `.gitmessage`, commit/Git hook 관련 문서
- Branch/merge: branch, merge, VCS 문서와 필요한 protection/ruleset
- CI/release/security/permission: 관련 workflow, 문서, checks, permissions 등 live GitHub metadata
- Repository file change: target path instruction과 validation guidance

GitHub metadata는 작업에 실제로 영향을 주는 경우에만 조회한다.

### 4. Expand Only When Needed

명시적 위치에서 충분한 지침을 찾지 못하면 의미를 검색한다.

`git`, `github`, `vcs`, `branch`, `commit`, `push`, `pull request`, `merge`, `review`, `release`, `contributing`, `agent`, `bot`, `automation`

Repository가 다른 용어를 사용하면 그 용어를 따른다. 발견한 instruction이나 README가 다른 필수 지침을 참조하면 현재 작업에 필요한 범위까지만 따라간다. 참고 링크 때문에 repository 전체를 재귀적으로 읽지 않는다.

## Resolve Instructions

Repository가 scope 또는 precedence를 명시하면 그것을 따른다. 그렇지 않으면 다음을 확인한다.

1. 상위 user/system/tool 제약과 충돌하지 않는가
1. 현재 ChatGPT/task에 실제로 적용되는가
1. 현재 target path/task가 선언된 scope에 포함되는가
1. normative instruction인지 context/reference인지 구분되는가
1. 동일 주제의 충돌이라면 더 구체적으로 scoped된 instruction이 있는가

파일명이나 위치만으로 precedence를 만들지 않는다. `AGENTS.md` ancestor scope처럼 repository/tooling이 의미를 부여한 경우에만 그 semantics를 적용한다.

Mutation에 영향을 주는 instruction 충돌을 안전하게 해소할 수 없다면 mutation을 수행하지 않고 충돌을 드러낸다. Task-level action 전에 대상과 적용 지침이 확인됐는지 다시 확인하되, 불필요한 context는 미리 적재하지 않는다.

## Maintenance

이 skill을 수정하거나 재구성할 때는 `docs/DIRECTIVE.md`의 본질과 불변 조건을 보존한다. 문서 구조보다 해당 directive의 의미를 우선한다.

## Boundary

이 skill은 code implementation, test/verification, naming convention, PR/review 내용, GitHub tool 호출 순서, repository 고유 workflow를 정의하지 않는다.

이 항목들은 repository 지침, live GitHub context 또는 해당 task skill에서 결정한다.
