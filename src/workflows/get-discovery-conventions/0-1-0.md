---
description: Generate a project-specific discovery-conventions.md to help agents map conventions and guidelines.
---

# Get Discovery Conventions Workflow (Meta-Workflow)

이 워크플로우는 프로젝트의 문서를 스캔하여, 에이전트가 해당 프로젝트의 규칙과 관행을 가장 빠르고 정확하게 파악할 수 있도록 돕는 `discovery-conventions.md` 워크플로우를 생성합니다.

## `discovery-conventions.md`란?

`discovery-conventions.md`는 에이전트가 새로운 프로젝트에 진입했을 때 수행해야 하는 '온보딩(Onboarding)' 절차를 정의한 워크플로우입니다. 프로젝트마다 문항의 위치, 기술 스택, 에이전트 전용 규칙(`AGENTS.md`)의 구조가 다르기 때문에, 이를 체계적으로 탐색하는 가이드를 제공하는 것이 목적입니다.

## Steps

### 1. **ENVIRONMENT MAPPING**

- 루트 디렉토리 및 `.agents/` 디렉토리를 포함한 프로젝트 전체 구성을 스캔하여 다음을 파악합니다:
    1. **핵심 문서 식별**: `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `.cursorrules` 등 규칙이 담긴 파일들.
    2. **기술 스택 탐색**: `package.json`, `requirements.txt` 등을 통해 주요 기술 및 아키텍처 파악.
    3. **에이전트 자산 확인**: `.agents/rules/`, `.agents/workflows/` 등 에이전트 전용 자산의 존재 여부 및 위치.
- **만약 프로젝트의 기본 구조조차 파악하지 못했다면, 해당 사실을 사용자에게 보고하고 워크플로우를 종료합니다.**

### 2. **Create Discovery Conventions Workflow**

- **맞춤형 생성**: 파악된 환경 정보를 바탕으로, 다음 단계를 포함하는 `discovery-conventions.md`를 생성합니다.
    1. **계층적 문서 읽기**: `README`부터 `AGENTS.md`까지 우선순위에 따른 가이드라인 분석 단계.
    2. **규칙 정렬(Alignment)**: 인간 개발자용 규칙과 에이전트용 규칙 사이의 충돌 해결 방식 정의.
    3. **체크리스트**: 프로젝트의 고유 관행(코드 스타일, 커밋 규칙 등)을 추출하기 위한 질문 리스트.
- **저장 및 업데이트**:
    - 별도 지침이 없다면 **루트(Root)**를 기본 저장 위치로 선정하고 사용자에게 알립니다.
    - 기존 파일이 존재할 경우, 파일명 뒤에 `_`를 붙여 생성하고(예: `discovery-conventions_.md`) 사용자에게 이를 경고합니다.

### 3. **REPORT**

- 작업 완료 후 사용자에게 다음 사항을 보고합니다:
    - **탐색된 문서 지도**: 에이전트가 참고한 주요 파일 목록.
    - **생성된 워크플로우의 중점**: 해당 프로젝트 온보딩 시 에이전트가 특히 주의 깊게 봐야 할 영역.
