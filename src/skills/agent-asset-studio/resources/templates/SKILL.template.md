---
name: {{slug}}
description: >
  <!-- 작성 지침: USE WHEN과 EXCLUDES를 포함하여 스킬 트리거 조건을 1-2문장으로 명확히 작성합니다. -->
  USE WHEN: {{slug}} 스킬이 활성화되어야 하는 조건 및 사용자 의도를 기술합니다.
  EXCLUDES: 이 스킬이 적용되지 않는 제외 대상 및 범위를 기술합니다.
---

# {{slug}}

<!-- Header: Overview (Optional) -->
<!-- 작성 지침: 이 스킬이 에이전트에게 제공하는 배경 맥락과 요약을 간단히 기술합니다. -->
## Overview

Overview of {{slug}}.

<!-- Header: Goal (Required) -->
<!-- 작성 지침: 이 스킬의 핵심 목적과 책임 범위를 명확히 작성합니다. -->
## Goal

Goal of {{slug}}.

<!-- Header: Non-Goal (Optional) -->
<!-- 작성 지침: Scope creep 방지를 위해 이 스킬에서 제외할 영역을 명시합니다. -->
## Non-Goal

Non-Goals of {{slug}}.

<!-- Header: When to Use (Required) -->
<!-- 작성 지침: 이 스킬을 사용해야 하는 구체적 시나리오 및 활성화 조건 목록을 작성합니다. -->
## When to Use

Use this skill when:

- Scenario 1
- Scenario 2

<!-- Header: When NOT to Use (Optional) -->
<!-- 작성 지침: 이 스킬을 사용하지 않거나 다른 자산으로 위임해야 하는 조건 목록을 작성합니다. -->
## When NOT to Use

Do not use this skill when:

- Excluded scenario 1
- Excluded scenario 2

<!-- Header: When to STOP (Optional) -->
<!-- 작성 지침: 실행 중단 조건, 명시적 조기 종료 조건 또는 완료 점검 항목을 작성합니다. -->
## When to STOP

Stop execution when:

- Early termination condition 1
- Completion criteria met

<!-- Header: Instructions (Required) -->
<!-- 작성 지침: 에이전트가 준수해야 하는 긍정적 가이드라인 및 규칙을 작성합니다. -->
## Instructions

Instructions for {{slug}}.

<!-- Header: Constraints (Optional) -->
<!-- 작성 지침: 에이전트가 절대 위반해서는 안 되는 엄격한 제약 사항을 작성합니다. -->
## Constraints

Constraints for {{slug}}.

<!-- Header: References (Optional) -->
<!-- 작성 지침: 참조하는 외부 문서나 references/ 디렉터리 내 리소스를 명시합니다. 본문 내 명시된 경우 중복 작성 자제(DRY). -->
## References

References for {{slug}}.

<!-- Header: Workflow: <Workflow Name> (Optional) -->
<!-- 작성 지침: 순차적 절차가 필요한 경우 작성합니다. 규칙 위주 스킬인 경우 생략 가능합니다. -->
## Workflow: {{slug}} Execution

<!-- Sub-Header: Context (Optional) -->
<!-- 작성 지침: 워크플로우 수행 시 인지해야 하는 맥락(환경, 상태, 입력 정보 등)을 정리하는 상위 헤더입니다. -->
### Context

<!-- Sub-Header: Arguments (Optional) -->
<!-- 작성 지침: 명령 호출 시 입력되는 CLI 스타일(-a, --flag 등) 간략 옵션을 작성합니다. -->
#### Arguments

Arguments for {{slug}}.

<!-- Sub-Header: Parameters & Variables (Required inside Context) -->
<!-- 작성 지침: 컨텍스트 및 작업 현황에 따른 환경 변수와 인지 맥락 파라미터를 작성합니다. (Context 내 필수) -->
#### Parameters & Variables

Parameters & Variables for {{slug}}.

<!-- Sub-Header: Procedure (Required within Workflow) -->
<!-- 작성 지침: 목표 달성을 위한 순차적 실행 절차 및 조건부 분기를 작성합니다. -->
### Procedure

1. Step 1
2. Step 2

<!-- Sub-Header: Validation (Optional) -->
<!-- 작성 지침: 수행 결과의 정확성을 검증하는 점검 항목을 작성합니다. -->
### Validation

Validation criteria for {{slug}}.
