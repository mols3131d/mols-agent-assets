# Clarify Code — Enhancement Research

이 문서는 `clarify-code`를 **실행 코드를 바꾸지 않고 code-adjacent explanation으로 이해 비용을 줄이는 Skill**로 고도화하기 위한 조사 기록입니다.

현재 단계는 초안입니다. 먼저 지금까지의 조사와 Skill split 결과를 기준으로 가설을 적고, 이후 외부 연구와 repository 원칙을 심층 조사해 갱신합니다.

## 현재 결론

`clarify-code`의 다음 개선 포인트는 comment/docstring을 더 많이 추가하는 것이 아니라 **설명 자체가 지불할 가치가 있는지 판단하고, 필요한 mental reconstruction을 가장 가까운 source surface에서 제거하는 것**입니다.

`code-comprehension-refactor`가 executable code에서 이해 비용을 제거한다면 `clarify-code`는 다음 영역을 맡습니다.

> 코드 구조 자체를 바꾸지 않아야 하거나 바꿀 필요가 없는 상황에서, code만으로 안정적으로 복원하기 어려운 contract·constraint·rationale·consequence를 가까운 설명 surface에 남긴다.

## 현재 가설

### 설명도 comprehension cost를 만든다

Comment와 docstring은 무료 정보가 아닙니다. Reader는 code와 prose 중 무엇을 읽을지 판단하고, prose의 scope와 freshness를 검증하고, code와 explanation을 연결해야 합니다.

따라서 설명을 추가했다는 사실 자체를 개선으로 보지 않습니다.

초기 판단 기준:

> 설명을 읽고 유지하는 비용보다 그것이 제거하는 추론·탐색·오해 비용이 클 때만 남긴다.

### `why`보다 더 정확한 설명 대상을 정의할 필요가 있다

현재 일반적인 guidance인 “comment는 what보다 why”만으로는 충분하지 않습니다. 모든 `why`가 가치 있는 것은 아니며, 다음처럼 code만으로 안정적으로 복원하기 어려운 의미가 더 중요한 후보입니다.

- constraint와 invariant
- consequence와 failure impact
- ordering reason
- rejected alternative 또는 더 단순해 보이는 접근을 사용할 수 없는 이유
- external system/protocol constraint
- caller가 의존하는 hidden contract

### Locality가 중요하다

정확한 설명도 적용되는 code와 멀리 떨어져 있으면 reader가 다시 관계를 복원해야 합니다.

초기 원칙:

> 의미가 적용되는 가장 좁고 가까운 stable surface에 설명을 둔다.

예:

| Meaning | Candidate surface |
| --- | --- |
| API 전체 caller contract | docstring |
| 특정 branch의 비자명한 이유 | 해당 branch 근처 comment |
| statement ordering invariant | ordering 바로 위 comment |
| module 전체 local convention | module-level explanation |
| repository/domain-wide policy | canonical owner, local에는 필요한 projection만 |

### 설명은 mental operation을 제거해야 한다

좋은 explanation은 reader가 해야 하는 다음 작업 중 하나 이상을 줄입니다.

- 다른 symbol/file/document/history 탐색
- hidden convention 복원
- side effect·exception·ordering 추론
- 이상한 implementation의 이유 추측
- 자연스럽지만 잘못된 alternative를 검토

설명이 제거하는 mental operation을 말하기 어렵다면 가치가 낮을 가능성이 큽니다.

### Negative knowledge가 중요하다

미래 maintainer가 자연스럽게 시도할 법한 변경이 실제로는 잘못된 경우, **왜 그 대안을 선택하면 안 되는지**는 높은 가치의 comment가 될 수 있습니다.

다만 단순히 과거에 시도했다는 history가 아니라 현재도 유효한 constraint와 consequence를 설명해야 합니다.

## 현재 `clarify-code`에서 이미 잘하는 부분

현재 Skill은 다음 책임을 이미 비교적 명확히 가집니다.

- caller-facing hidden contract → docstring
- maintainer-only local rationale → comment
- module-local explanation 허용
- code가 표현하는 `what` 반복 금지
- structural opacity는 `code-comprehension-refactor`로 route
- canonical policy의 최소 projection
- machine-consumed comment/docstring 구분
- stale prose와 implementation-detail explanation 억제

따라서 새로운 taxonomy나 reference package를 크게 늘리기보다 기존 `references/documentation.md`의 판단력을 높이는 편이 우선입니다.

## 조사 질문

심층 조사에서 다음을 검증합니다.

1. Comment/docstring이 실제 comprehension에 도움이 되는 조건과 방해하는 조건은 무엇인가?
2. Explanation locality와 code-prose consistency는 comprehension에 어떤 영향을 주는가?
3. Rationale, constraint, rejected alternative 같은 정보가 maintenance에서 어떤 가치를 가지는가?
4. Comment decay/staleness의 주요 원인은 무엇이며 Skill이 예방할 수 있는 수준은 어디까지인가?
5. 좋은 API docstring은 signature/type과 어떤 정보를 분담해야 하는가?
6. Comment quantity나 coverage 같은 단순 proxy를 피하면서 explanation value를 어떻게 operationalize할 수 있는가?
7. 현재 `clarify-code`에 추가할 내용과 추가하지 말아야 할 내용을 어디서 나눌 것인가?

## 초기 개선 후보

- `Explanation Value` 판단 추가
- `Placement and Scope` 판단 추가
- constraint / consequence / rejected alternative를 comment의 주요 가치로 명시
- Final Pass에 “이 설명이 어떤 mental operation을 제거하는가?” 추가
- 설명을 읽는 비용과 stale risk를 함께 판단
- code와 설명이 conflict하면 prose보다 code/current contract를 신뢰하고 stale explanation을 제거하거나 교정
- capability eval에 redundant comment, distant rationale, rejected alternative, overly broad comment scope 같은 case 보강

## 초기 비목표

- comment density, comment-to-code ratio 같은 score 도입
- 모든 public symbol에 docstring 강제
- 모든 non-obvious code에 comment 추가
- documentation style guide 전체를 `clarify-code`에 복제
- 새 analyzer나 comment linter 구축
- `code-comprehension-refactor` 책임을 다시 가져오기

## Status

Draft. 심층 조사 후 근거, 우선순위, 반례와 최종 권고를 갱신합니다.
