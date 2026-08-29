# Clarify Code — Enhancement Plan

이 계획은 [Clarify Code Enhancement Research](clarify-code-enhancement-research.md)의 초안 가설을 바탕으로 작성한 첫 계획입니다.

현재 단계는 초안입니다. 심층 조사에서 근거와 반례를 검토한 뒤 구현 범위와 acceptance를 갱신합니다.

## Goal

`clarify-code`를 “주석과 docstring을 추가하는 Skill”이 아니라 **code-adjacent explanation의 순가치를 판단하고, 필요한 설명만 가장 가까운 stable surface에 남겨 이해 비용을 줄이는 Skill**로 고도화합니다.

## Preserve

다음 responsibility split은 유지합니다.

- executable code refactor → `code-comprehension-refactor`
- code-adjacent explanatory prose → `clarify-code`
- user-facing/standalone documentation → 별도 문서 capability

`clarify-code`는 executable statement, identifier, type/signature, representation, control/state flow와 abstraction을 바꾸지 않습니다.

## Initial Design

### 1. Explanation Value

설명을 추가하기 전에 다음을 판단합니다.

- 이 설명이 없으면 reader가 무엇을 추론하거나 찾아야 하는가?
- 그 mental operation은 실제로 불필요한 comprehension cost인가?
- 설명을 읽고 유지하는 비용보다 제거되는 비용이 큰가?
- 이미 code/name/type이 같은 정보를 충분히 표현하는가?

설명 자체를 improvement로 보지 않고 **net comprehension benefit**이 있을 때만 남깁니다.

### 2. Placement and Scope

설명은 의미가 적용되는 가장 좁고 가까운 stable surface에 둡니다.

- API contract → docstring
- local branch/order/invariant → 해당 code 근처 comment
- module-local convention → module-level explanation
- broad policy → canonical owner, source에는 필요한 projection만

Comment가 실제 invariant보다 넓게 읽히거나 너무 먼 위치에서 관계를 추론하게 만들지 않는지 확인합니다.

### 3. High-Value Explanation Types

현재 documentation guidance를 다음 의미 중심으로 보강할 후보입니다.

- hidden caller contract
- invariant / constraint
- consequence / failure impact
- ordering rationale
- external system constraint
- rejected alternative / negative knowledge

단순 implementation narration과 historical note는 계속 피합니다.

### 4. Final Pass 강화

기존 Final Pass에 다음 질문을 추가할 후보입니다.

- 이 설명은 어떤 추론·탐색·오해 비용을 제거하는가?
- 의미가 적용되는 가장 가까운 위치인가?
- scope가 실제 contract/invariant와 일치하는가?
- 미래 maintainer가 자연스럽게 시도할 잘못된 alternative를 예방하는가?
- 설명이 code보다 빠르게 stale될 가능성이 높은가?

## Candidate File Changes

### `src/rulesync/.rulesync/skills/clarify-code/SKILL.md`

기본적으로 작은 변경만 고려합니다.

- core workflow에 “설명 추가 자체가 목적이 아니다”라는 signal을 짧게 추가
- explanation이 제거할 comprehension cost를 먼저 확인하도록 보강
- locality/scope는 상세 reference로 남겨 core 비대화를 피함

### `src/rulesync/.rulesync/skills/clarify-code/references/documentation.md`

주요 개선 owner입니다.

후보 section:

- `Explanation Value`
- `Placement and Scope`

기존 Docstrings, Comments, Module-Level Explanation, Contract Projection, Machine-Consumed Text와 중복되지 않게 통합합니다.

새 reference 파일은 만들지 않는 것을 기본으로 합니다.

### `evals/skills/clarify-code/cases.json`

초기 capability 보강 후보:

| Case | Expected behavior |
| --- | --- |
| redundant obvious comment | prose를 추가하지 않음 |
| high-value ordering rationale | consequence/invariant 중심 comment |
| rejected alternative | 현재도 유효한 constraint를 가까운 위치에 설명 |
| distant rationale request | 가장 가까운 stable surface를 선택 |
| overly broad comment | 실제 scope에 맞게 좁힘 |
| stale implementation narration | 제거 또는 현재 invariant 중심으로 교정 |
| hidden caller consequence | caller가 사용 전에 알아야 하면 docstring |
| structural opacity disguised as comment request | `code-comprehension-refactor`로 route |

## Guardrails

- explanation quantity나 coverage를 KPI로 사용하지 않음
- 모든 public API에 docstring을 요구하지 않음
- “why”라는 이유만으로 comment를 유지하지 않음
- historical discussion을 현재 rationale처럼 복제하지 않음
- broad policy를 source prose가 소유하지 않음
- structural problem을 comment로 보상하지 않음
- source-level explanation을 standalone documentation으로 확장하지 않음

## Validation

구현 시 다음을 확인합니다.

1. `clarify-code`와 `code-comprehension-refactor` responsibility가 다시 겹치지 않는지 review
2. positive/negative capability fixture semantic review
3. generated route sync가 필요한 frontmatter 변경 여부 확인
4. repository deterministic tests
5. 가능하면 model/runtime capability eval; 실행하지 않으면 fixture review만 보고

## Acceptance

- 설명을 추가하지 않는 것이 더 좋은 경우 no-op할 수 있음
- 필요한 rationale/contract는 reader가 다른 곳을 덜 탐색하도록 가까운 위치에 둠
- comment는 code narration보다 constraint/consequence/rationale를 전달함
- rejected alternative를 history가 아니라 현재 유효한 constraint로 설명함
- code와 explanation의 responsibility boundary를 유지함
- Skill package를 불필요하게 늘리지 않음

## Status

Draft. 심층 조사 후 우선순위와 exact change set을 갱신합니다.
