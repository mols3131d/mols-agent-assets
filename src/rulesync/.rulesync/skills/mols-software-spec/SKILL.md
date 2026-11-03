---
name: mols-software-spec
description: >-
  Drive a software change through behavior specifications, test decisions,
  implementation evidence, and review-directed rework using configurable
  artifact-aware workflows. Use for substantial spec/test-driven feature or
  behavior changes, specification-to-code alignment, and review feedback that
  must return to an affected development stage. Do not use for general task
  tracking, backlog prioritization, routine code edits without a spec need,
  or standalone test-design advice.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
---

# Software Spec- and Test-driven Development

소프트웨어 변경의 **기대 동작 → 테스트·구현 → 관찰된 근거**를 일치시키고 Review의 finding에 따라 영향을 받는 개발 단계로 돌아간다. 작업 백로그·우선순위·여러 작업 간 일정은 관리하지 않는다. 기존 프로젝트의 지침, 스펙 저장소, 테스트·CI 및 실제 실행 도구가 우선한다.

## Source of Responsibility

- **Artifact Registry:** [assets/artifacts.json](assets/artifacts.json)이 산출물 ID·종류와 문서 기본 파일명을 정의한다. 산출물의 의미·작성 기준은 [Artifacts](references/artifacts.md)가 설명한다. **생성 순서는 Artifact가 소유하지 않는다.**
- **Workflow:** [Default](assets/workflows/default.json)는 제안 → 조사 → 계획 → 스펙 → 테스트 설계 → 테스트 구현 → 코드 구현 → 리뷰의 권장 전체 흐름이다. [Focused](assets/workflows/focused.json)는 기존 프로젝트와 작은 변경에 맞춘 짧은 예시다. 단계와 의존성·복귀 대상은 [Workflow](references/workflow.md)와 선택된 workflow 파일이 소유한다.
- **Runtime:** 실제 가용 도구로 산출물을 읽고 수정하고 검증한다. [scripts/flow.py](scripts/flow.py)는 workflow 구조 검사와 Review 기반 재확인 경로를 계산하는 선택적 **읽기 전용 도구**이며 작업이나 테스트를 실행하지 않는다.

## Execution

1. **범위를 확인한다.** 사용자 요청·수락 조건·실제 저장소의 규칙과 변경 범위를 확인한다. 이미 OpenSpec 등 기존 정본이 있으면 별도 정본 트리를 임의로 만들지 않고 그 계약을 우선한다. 단일 수정 작업에 이 Skill이 필요 없는 경우 활성화를 늘리지 않는다.
2. **Workflow를 선택한다.** 명시된 절차가 있으면 그것을, 아니면 명세 중심의 충분한 개발 흐름에는 `default`, 이미 조사·계획이 충분하거나 작고 한정된 변경에는 `focused`를 고려한다. 단계 선택은 필요한 근거와 위험에 비례한다. Workflow의 순서를 바꾸려면 Artifact Registry가 아니라 선택된 Workflow를 조정한다. 사용자 지정 workflow의 구조는 가능하면 `flow.py validate`로 확인한다.
3. **산출물을 재사용하거나 작성한다.** 해당 단계의 정본·기존 파일을 먼저 확인한다. 부족한 산출물만 프로젝트가 허용하는 위치에 생성한다. 독립 저장소를 처음 만든다면 승인된 위치를 선택한다. 별도 규칙이 없을 때의 제안 경로는 `spec/changes/<change-id>/`이지만, 경로 제안은 쓰기 권한이나 디렉터리 자동 생성을 뜻하지 않는다. 테스트 코드와 제품 코드는 프로젝트의 원래 코드 경로에 둔다.
4. **테스트·구현을 연결한다.** 스펙의 관찰 가능한 동작과 수락 조건을 먼저 구체화한다. 선택된 단계가 요구하는 검증 범위에서 테스트 설계·실제 테스트 구현·코드 변경을 수행한다. 전체 workflow의 테스트 선행은 기본값이지 모든 프로젝트에 강제하는 법칙이 아니다. 테스트를 먼저 썼을 때 기대된 red 상태와 제품 결함·테스트 오류를 구분한다.
5. **Review를 수행한다.** 스펙, 테스트 oracle·실행 결과, 코드·CI의 실제 근거와 차이를 검토한다. 발견한 문제는 원인·근거·대상 단계를 구체적으로 남긴다. 분류된 finding은 [Workflow](references/workflow.md)에 따라 `rework`로 복귀시키고, 필요한 단계만 재확인한다. 결정적 도움을 받을 수 있으면 `flow.py route`를 사용한다. script의 후보 반환은 실제 수정을 의미하지 않는다.
6. **종료를 검증한다.** Review가 근거를 갖춘 PASS여도 구조 검사나 LLM 판정 자체가 테스트 통과를 보장하지 않는다. 실제 실행·관찰 수준에서 수락 조건을 판정한다. 실행할 수 없거나 근거가 부족하면 `blocked` 또는 부분 완료·인계로 구분하며, 성공으로 꾸미지 않는다.

## Runtime and Safety

- CLI와 scripts를 직접 사용할 수 있으면 **해당 Skill 패키지에 포함된** 원본과 가용 의존성을 확인하고 실행한다. ChatGPT Chat 등 스크립트 접근·실행이 불확실한 환경에서는 파일·연결 앱으로 가능한 동일 논리의 단계를 수행하되, 실행하지 않은 validator의 PASS를 주장하지 않는다.
- 작업 상태와 백로그는 기존 issue tracker 또는 작업 관리 owner가 소유한다. 별도의 `tasks.json`, stage progress DB, 자동 scheduler를 만들지 않는다. Spec 변경은 관련 Work Item을 **참조만** 할 수 있다.
- 단일 Review에서 무조건 처음부터 다시 실행하거나 영향을 받지 않은 파일을 일괄 다시 작성하지 않는다. `recheck`는 **필요한 영향 확인**이며 자동 수정·무효화를 뜻하지 않는다.
- 원격 작업 전에 연결 계정·현재 ref·권한과 대상 파일을 확인하고, 사용자 승인·프로젝트 정책이 정한 경계를 지킨다. 실패한 쓰기를 다른 계정이나 무단 도구 전환으로 우회하지 않는다.

## Boundaries

이 Skill은 소프트웨어 변경 한 건의 명세·테스트·구현 **연결과 Review 복귀**를 맡는다. 일반 task management, 요구사항과 관계없는 일상 코딩, 전문적인 테스트 oracle 판단 자체, CI admission·Git PR 승인, 기존 스펙 도구의 공식 명령 의미, 프로젝트 내부 반복 오케스트레이션을 재정의하지 않는다. 독립적인 다른 Skill의 설치를 실행 전제로 삼지 않는다.
