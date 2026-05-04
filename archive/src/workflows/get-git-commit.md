---
description: Discover project-specific git rules from agent documentation and generate an optimized git-commit workflow.
---

# Get Git Commit Workflow (Meta-Workflow)

이 워크플로우는 프로젝트의 **에이전트 가이드라인(`AGENTS.md`)** 및 **전용 규칙(`.agents/rules/`)**을 계층적으로 분석하여, 해당 프로젝트에 가장 최적화된 `git-commit` 워크플로우를 생성합니다.

## Steps

### 1. **RULE DISCOVERY**

- `README.md`, `CONTRIBUTING.md`, `.gitmessage`와 같은 개발자 가이드라인과 `AGENTS.md`, `.agents/`와 같은 에이전트 가이드라인을 파악하여 다음을 수행합니다:
    1. **깃(Git) 규칙 파악**: 프로젝트 고유의 커밋 컨벤션 및 제약 사항 확인.
    2. **에이전트 관행 파악**: 워크플로우, 스킬, 작업 등이 저장된 디렉토리 및 관리 방식 확인.
- **만약 위 규칙이나 관행을 파악하지 못했다면, 해당 사실을 사용자에게 보고하고 워크플로우를 종료합니다.**

### 2. **Create Git Commit Workflow**

- **기본 관행 (Baseline)**: 별도 규칙이 없을 경우 다음을 기본으로 합니다.
    1. `git status` + `git diff`로 변경사항 확인.
    2. `git add`로 변경사항 추가.
    3. `git status`로 변경사항 확인.
    4. `git commit`으로 커밋(`.gitmessage` 또는 Conventional Commit 준수).
    5. 사용자에게 변경사항 및 커밋 메시지 보고.
- **맞춤형 생성**: 파악된 프로젝트 규칙을 결합하여 최적화된 `git-commit.md` 워크플로우를 생성합니다.
- **저장 및 업데이트**:
    - 별도 지침이 없다면 `.agents/workflows/git-commit.md`를 우선적인 저장 위치로 선정합니다.
    - 기존 파일이 존재할 경우, 단순 덮어쓰기보다 기존의 유효한 규칙을 보존하며 개선(Refine)하는 방식을 취합니다.

### 3. **REPORT**

- 작업 완료 후 사용자에게 다음 사항을 보고합니다:
    - **발견된 프로젝트 깃 규칙**: 타입, 스코프, 제약 사항 등.
    - **에이전트 워크플로우 관행**: 저장 위치 및 파일 관리 방식.
    - **생성/업데이트 결과**: 새로 구성된 `git-commit` 워크플로우의 주요 특징.
