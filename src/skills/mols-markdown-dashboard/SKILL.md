---
name: mols-markdown-dashboard
description: >-
  Create, update, render, or review static Markdown engineering dashboards that
  reconcile specifications, implementation evidence, and verification evidence
  into requirement-level progress and gaps. Use for project/domain development
  dashboards, implementation or verification coverage and gaps, readiness against
  specs/tests, snapshot comparison, or conversion of specs, code, tests, and
  results into this dashboard format. Also use to maintain or render this skill's
  YAML/Markdown format. Do not use for general status reports, task trackers,
  BI/analytics dashboards, or live monitoring/observability UIs.
compatibility: >-
  Core instructions are agent-runtime agnostic. The bundled renderer requires
  Python 3.11+ and the dependencies declared in pyproject.toml; uv is optional.
---

# MOLS Markdown Dashboard

스펙과 현재 검증 근거를 바탕으로 **개발 상태와 남은 공백**을 Markdown 대시보드로 표현한다.

## Core Contract

기본 대시보드는 세 가지를 구분한다.

1. `Development Progress` — 구현·검증 상태와 정확한 `n/n`
2. `Implementation Gaps` — 아직 구현되지 않은 Requirement
3. `Verification Gaps` — 실패·미검증·blocked·manual-only Verification Target

Project dashboard는 `Domain`, domain dashboard는 `Capability`를 한 행으로 사용한다.

- 근거 없이 상태나 분모를 추측하지 않는다.
- Requirement와 Verification Target을 의미 단위로 센다.
- 프로젝트 합계는 분자·분모를 합산한다.
- 완료된 항목은 Gap에서 제거한다.
- YAML과 Markdown이 함께 있으면 YAML을 반복 생성의 정본으로 취급한다.

## References

조건에 해당하는 참조만 읽고, 여러 조건이 겹치면 필요한 참조를 조합한다.

| When | Load |
| --- | --- |
| status, progress, gap의 의미나 집계를 판단한다 | [Dashboard Method](references/dashboard-method.md) |
| 기존 dashboard를 현재 근거로 갱신한다 | [Update Workflow](references/update-workflow.md) |
| dashboard의 사실성·집계·gap을 리뷰한다 | [Review Workflow](references/review-workflow.md) |
| dashboard YAML을 읽거나 쓴다 | [Dashboard Schema](references/dashboard-schema.md) |
| bundled renderer를 실행하거나 결과를 검증한다 | [Render Workflow](references/render-workflow.md) |
| 표만으로 관계·추세를 설명하기 어렵다 | [Visual Selection](references/visual-selection.md) |
| 관련 reference를 읽고도 형식이 불명확하다 | [Domain Example](examples/domain-dashboard.md) 또는 [Project Example](examples/project-dashboard.md) |

예제는 필요한 reference를 읽은 뒤에도 형식이 불명확할 때만 사용한다.

## Workflow

1. dashboard level과 snapshot을 정한다.
2. Requirement, 구현 근거, Verification Target, 검증 근거를 조사한다.
3. 근거에서 status, progress, gaps를 결정한다.
4. 반복 가능한 산출물이면 YAML을 만들거나 갱신한다.
5. 사용할 수 있으면 bundled renderer로 Markdown을 생성하고 검증한다.

의미 판단은 에이전트가 담당한다. 스크립트는 입력 검증, 계산, 렌더링과 구조 검증만 담당한다.

## Output

- 기본 산출물: `dashboard.yml` + `dashboard.md`
- Markdown만 요구되면 YAML은 작업용으로만 사용할 수 있다.
- Review는 source dashboard를 수정하지 않고 verdict와 findings를 반환한다.
- 사용하지 않는 section, placeholder, 중복 visual은 제거한다.
