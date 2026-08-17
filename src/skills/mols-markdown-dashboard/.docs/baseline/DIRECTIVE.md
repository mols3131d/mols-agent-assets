---
title: "MOLS Markdown Dashboard Directive"
description: "스킬이 후속 수정에서 훼손되지 않도록 핵심 요구사항과 결정사항을 보존한다."
---

# Directive

이 문서는 스킬 수정 시 가장 먼저 확인해야 하는 정본이다. 요구사항이나 결정사항을 바꾸려면 해당 행을 명시적으로 수정하고 이유를 남긴다.

## Requirements

| ID | Requirement | Rationale |
| --- | --- | --- |
| R-001 | Project dashboard는 Domain을 한 행으로 사용한다. | 프로젝트 수준의 책임 경계를 빠르게 비교한다. |
| R-002 | Domain dashboard는 Capability를 한 행으로 사용한다. | 스펙과 검증을 구현 파일보다 안정적인 의미 단위로 집계한다. |
| R-003 | 최상단 표의 열은 대상, Implementation Status, Implementation Progress, Verification Status, Verification Progress 순서다. | 구현과 검증을 각각 상태→범위 순으로 읽는다. |
| R-004 | Progress는 10칸 진행 바와 정확한 `n/n`을 함께 표시한다. | 빠른 비교와 정확한 수치를 동시에 제공한다. |
| R-005 | Implementation Progress는 완료 Requirement / 전체 필수 Requirement다. | 스펙 문서 작성량이나 task 수를 진행률로 오인하지 않는다. |
| R-006 | Verification Progress는 현재 결과가 확보된 Verification Target / 전체 필수 Verification Target이다. 실패 결과도 분자에 포함하며 상태는 별도로 `Failing`으로 표시한다. | 검증 범위와 검증 결과의 건강도를 분리한다. |
| R-007 | Implementation Gaps는 미구현 Requirement만 한 행씩 표시한다. | 완료 내용의 반복을 제거하고 남은 작업만 보여준다. |
| R-008 | Verification Gaps는 실패·미검증·blocked·manual-only Target만 한 행씩 표시한다. 실패 Target은 progress 분자에 포함될 수 있고 나머지는 포함되지 않는다. | 실제 신뢰 공백과 검증 범위를 동시에 보존한다. |
| R-009 | Gap 번호는 각 Domain 또는 Capability 안에서 1부터 시작한다. | 항목별 추적과 대화를 쉽게 한다. |
| R-010 | 상태 셀은 이모지와 영문 상태명을 함께 표시한다. | 색상만 의존하지 않으면서 빠르게 스캔한다. |
| R-011 | 핵심 세 표는 YAML에서 Jinja2로 렌더링할 수 있어야 한다. | 에이전트 토큰과 반복 편집 비용을 줄인다. |
| R-012 | YAML은 `yaml.safe_load`로 읽고 생성 Markdown은 pyromark로 파싱한다. | 안전한 입력 처리와 기계적 결과 검증을 제공한다. |
| R-013 | 모델은 표준 라이브러리 `dataclasses`와 `StrEnum`을 사용한다. | Pydantic 없이 가볍고 명시적인 런타임 모델을 유지한다. |
| R-014 | 스크립트는 계산·형식·검증만 담당하고 의미 판단은 에이전트가 담당한다. | 자동화가 근거 없는 status나 denominator를 만들지 않게 한다. |
| R-015 | 기본 템플릿은 차트를 강제하지 않는다. | 진행 바와 중복되는 시각화를 피한다. |
| R-016 | Risks / Blockers와 References는 값이 있을 때만 렌더링한다. | 빈 section과 장식적 구조를 제거한다. |
| R-017 | 정의되지 않은 YAML 필드는 경로가 포함된 오류로 즉시 거부한다. | 에이전트 오타가 조용히 유실되거나 잘못 렌더링되는 일을 막는다. |
| R-018 | 출력 파일은 임시 파일을 거쳐 atomic replace로 갱신한다. | 실패한 렌더가 기존 dashboard를 부분적으로 손상하지 않게 한다. |
| R-019 | 예제 Markdown은 예제 YAML에서 생성되며 품질 검사에서 drift를 확인한다. | 문서 예제와 실제 renderer의 차이를 방지한다. |
| R-020 | release 품질 게이트는 `uv`, `ruff`, `ty`, `rumdl`, `pytest`와 예제 drift 검사를 사용한다. | 실행·형식·타입·Markdown 품질을 하나의 재현 가능한 절차로 고정한다. |

## Decisions

| ID | Decision | Alternatives rejected | Reason |
| --- | --- | --- | --- |
| D-001 | YAML을 dashboard 반복 생성의 local render source로 사용한다. | Markdown 직접 편집만 사용 | 구조화된 입력이 토큰과 formatting drift를 줄인다. |
| D-002 | Jinja2를 Markdown template engine으로 사용한다. | f-string 전용 renderer, custom template syntax | 유지보수 가능한 template loader와 `StrictUndefined`를 제공한다. |
| D-003 | PyYAML을 YAML parser로 사용한다. | custom parser | 간단하고 널리 사용되며 `safe_load`를 제공한다. |
| D-004 | pyromark는 생성기가 아니라 결과 parser로 사용한다. | pyromark로 template 생성 | pyromark의 책임은 Markdown parsing이다. |
| D-005 | Progress bar는 10칸이며 완료 전에는 내림한다. | 반올림 | 시각적으로 실제 진척을 과장하지 않는다. 정확한 `n/n`이 보완한다. |
| D-006 | 프로젝트 합계는 분자·분모 합산으로 계산한다. | 행별 percentage 평균 | Capability 또는 Domain 규모 차이를 보존한다. |
| D-007 | 완료된 항목은 Gap 표에서 제거한다. | 전체 Requirement·Target 목록 표시 | 최상단 진행표와 중복을 피하고 남은 공백에 집중한다. |
| D-008 | Verification Target은 test layer에 제한하지 않는다. | Unit test만 집계, test function 수 집계 | component, integration, runtime도 capability 신뢰에 필요할 수 있다. |
| D-009 | 핵심 Markdown 표에는 상태 범례와 풋노트를 기본 생성하지 않는다. | 상태 풋노트 또는 별도 legend | 이모지와 상태명이 이미 의미를 전달한다. |
| D-010 | 차트와 복잡한 Mermaid는 조건부이며 전문 스킬에 위임한다. | 모든 dashboard에 chart 삽입 | visual duplication과 유지보수 비용을 줄인다. |
| D-011 | loader boundary 이후에는 raw dictionary 대신 immutable slot dataclass를 사용한다. | 전 구간 `dict[str, Any]` 사용 | 타입 경계를 명확히 하고 renderer와 validation의 계약을 단순화한다. |
| D-012 | 단일 `scripts/check_quality.py`가 모든 release 검사를 조정한다. | 도구별 명령을 사람 기억에 의존 | 에이전트와 사람이 동일한 품질 절차를 반복할 수 있게 한다. |

## Protected Invariants

- `Development Progress`, `Implementation Gaps`, `Verification Gaps`의 의미를 서로 섞지 않는다.
- `Implementation Status`와 `Verification Status`를 하나의 generic status로 합치지 않는다.
- progress denominator를 test function, file, commit 또는 임의 task 수로 자동 대체하지 않는다.
- project와 domain dashboard의 표 문법은 첫 번째 열을 제외하고 동일해야 한다.
- YAML status에는 이모지를 저장하지 않는다. renderer가 표시 문자열을 결정한다.
- Markdown을 재렌더링해도 Gap 번호와 합계가 결정적으로 같아야 한다.
- schema, examples, template, tests와 directive를 서로 독립적으로 변경하지 않는다.
- 품질 도구를 사용할 수 없으면 통과했다고 기록하지 않고 제한을 review 문서에 남긴다.

## Non-Goals

- live monitoring UI
- BI dashboard 또는 interactive web application
- source code에서 Requirement와 Verification Target을 완전 자동 추론
- test runner 또는 observability backend 대체
- 일정·owner·action 관리 도구 대체
