# Dashboard Method

## Objective

이 대시보드는 개발 활동량이 아니라 다음 두 질문에 답한다.

1. 스펙에서 요구한 기능이 어디까지 구현됐는가?
1. 구현됐다는 주장을 어디까지 검증했는가?

## Hierarchy

```text
Project
└─ Domain
   └─ Capability
      ├─ Requirement
      └─ Verification Target
```

| Dashboard level | Row unit |
| --- | --- |
| Project | Domain |
| Domain | Capability |

`Component`, package, module과 function은 구현 근거이지 기본 집계 계층이 아니다.

## Evidence Model

| Claim | Preferred evidence |
| --- | --- |
| Requirement exists | repository가 정의한 canonical spec 또는 contract |
| Requirement implemented | source code, completed task, implementation artifact |
| Target verified | current test result, execution artifact, review evidence |
| Target failed | current failure output 또는 reproducible result |
| Target blocked | 환경·의존성·결정 기록 |

Requirement authority와 source hierarchy는 host repository의 documented policy를 따른다. Proposal, plan, task, design 같은 work artifact는 host policy가 authoritative 또는 normative로 정의하지 않는 한 current Requirement의 canonical source를 대체하지 않는다.

근거가 충돌하면 host repository가 정의한 canonical source와 snapshot을 비교하고 `Unknown`, `Blocked`, `Failing` 또는 gap으로 보존한다.

## Status Vocabulary

### Implementation

| Code | Meaning |
| --- | --- |
| `not_started` | 구현 근거가 없고 시작하지 않음 |
| `planned` | 스펙은 있으나 구현 단계 전 |
| `in_progress` | 일부 Requirement만 구현 |
| `implemented` | 필수 Requirement 전체 구현 |
| `blocked` | 구현 진행을 막는 조건이 있음 |
| `unknown` | 근거가 부족해 판단할 수 없음 |

### Verification

| Code | Meaning |
| --- | --- |
| `unverified` | 필수 검증 근거가 없음 |
| `partial` | 필수 Verification Target 일부만 확인 |
| `passing` | 필수 Verification Target 전체 통과 |
| `failing` | 하나 이상의 필수 검증 실패 |
| `blocked` | 환경·의존성 때문에 검증 실행 불가 |
| `unknown` | 결과가 없거나 신뢰할 수 없음 |

Renderer가 상태 코드에 이모지와 영문 label을 붙인다. YAML에는 stable code만 저장한다.

## Implementation Progress

Requirement를 의미 단위로 센다.

- 문서 bullet 개수를 무비판적으로 세지 않는다.
- 같은 Requirement를 여러 파일에서 반복해도 하나로 센다.
- 부분 구현은 완료 분자에 포함하지 않는다.
- `Implemented`는 필수 Requirement가 모두 구현됐을 때만 사용한다.

## Verification Progress

Verification Target을 의미 단위로 센다.

- test function 개수를 세지 않는다.
- OpenSpec Scenario만으로 제한하지 않는다.
- invariant, 실패 경로, regression, integration, runtime도 필수 Target이 될 수 있다.
- 같은 Target을 여러 test function이 검증해도 하나로 센다.
- 현재 실행 결과가 있으면 통과와 실패 모두 progress 분자에 포함한다.
- 실패 여부는 `Verification Status`와 Verification Gap에서 별도로 드러낸다.
- 미검증, blocked, manual-only Target은 progress 분자에 포함하지 않는다.

## Core Tables

### Development Progress

상태는 판단, 진행률은 완료 범위다. 둘은 독립적이다.

```text
Verification Progress 10/10
Verification Status   🔴 Failing
```

모든 Target이 정의돼 있어도 현재 실행이 실패하면 `Failing`일 수 있다.

### Implementation Gaps

완료되지 않은 Requirement만 한 줄씩 둔다.

### Verification Gaps

실패·미검증·blocked·manual-only Target만 한 줄씩 둔다.

## Optional Sections

| Section | Include when |
| --- | --- |
| Risks / Blockers | 단순 gap과 구분되는 실제 진행 위험이 있음 |
| Progress Trend | 동일 denominator 또는 비교 가능한 snapshot이 여러 개 있음 |
| Dependency Diagram | 표 한 줄로 이해하기 어려운 의존·handoff가 있음 |
| References | 독자가 원문 근거를 찾아야 함 |

기본 템플릿에는 차트를 강제하지 않는다. 진행 바가 이미 현재 비율 비교를 담당한다.
