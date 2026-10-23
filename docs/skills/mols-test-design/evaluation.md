---
description: mols-test-design의 선택·행동 평가에서 baseline, 테스트 오라클의 품질, 실행 근거와 비용을 어떻게 비교할지 판단할 때 사용합니다.
---

# Test Design Evaluation

이 문서는 `mols-test-design`의 **평가 목적과 비교 근거**를 유지한다. 실행 동작의 정본은 `src/rulesync/.rulesync/skills/mols-test-design/SKILL.md`이며 평가 사례의 원본은 `evals/skills/mols-test-design/cases.json`이다. 이식성·중복 방지 관점에서 모든 agent/harness가 동일한 evaluator를 갖는다고 가정하지 않는다.

## Core Claims

| 평가 질문 | 관찰할 결과 | 오해하면 안 되는 것 |
| --- | --- | --- |
| 필요한 시점에 선택되는가? | test strategy, oracle, sufficiency, fixture/isolation 요구에서 올바른 selection | metadata 문구가 충분하다는 정적 검토를 실측 routing success로 해석 |
| 필요 없을 때 물러나는가? | 일반 구현, runner debugging, CI admission, Agent Asset eval 요청에서 불필요한 선택 억제 | Skill 이름이 프롬프트에 있다는 이유로 모든 요청을 유효화 |
| 중요한 테스트를 설계하는가? | 실제 계약, 신뢰 가능한 oracle, 현실적인 결함 구별 사례, 최소 충분 경계 | test case 수, coverage, assertions를 correctness의 대리 지표로 사용 |
| 유효성의 경계를 이해하는가? | 정상 reference와 결함 구현, missing deliverable, flakiness/mocking의 서로 다른 위험 분리 | 현재 코드 또는 test PASS만으로 기능 완성 선언 |
| 두 방향의 오라클을 검증하는가? | 확정된 정상 동작의 수용과 중요한 결함 사례의 거부를 구분하며 잘못된 기대값을 수정 | mutation 점수 또는 현재 구현의 통과를 oracle의 정확성으로 해석 |
| 실패 원인과 수정 책임을 구분하는가? | 제품 코드/테스트·expectation/fixture·runner·환경의 근거를 분리해 조치 제안 | 알 수 없는 실패를 임의의 코드 변경이나 무조건 retry로 덮음 |
| 병렬 변경·테스트 독립성을 보존하는가? | 타 소유자의 private helper·상태·순서에 대한 불필요한 결합 축소, 독립 fixture/state와 좁은 검증 범위 | 폴더 수, 무조건 mocking 또는 test file 수로 독립성을 평가 |
| 실제 컴포넌트 간 호환성을 보호하는가? | 사용 중인 API·메시지 계약과 공유 트랜잭션/상태에 필요한 contract·integration evidence | 모든 상호작용 검증을 없애면 더 독립적이라고 가정 |
| 실행 근거를 정확히 보고하는가? | verified / inferred / unknown / not run 구분 | 정적 검토·시뮬레이션을 runtime PASS로 보고 |
| 전문 스킬로서 이득이 있는가? | 동일 모델·하네스·문맥·도구·예산에서 coding-context-only baseline과 비교 | 달라진 model이나 grader로 효과를 단정 |

## Case Ownership

- **Routing** — positive, negative, near-miss를 구분한다. 기능 구현 요청 중에 테스트 설계가 실제 하위 작업인지, 테스트 실행만 암묵적으로 필요한 상황인지 구분한다. 테스트 경계·독립 검증이 주제면 선택하되, 모듈 아키텍처 재설계 또는 작업 공간·worktree 격리만 요청한 경우는 선택하지 않는다. 유사한 전문 Skill이 후보에 있을 때에는 실제 작업의 주책임자가 선택되는지 별도로 확인한다.
- **Behavior** — oracle 오류(현재 구현 복제), 높은 coverage와 약한 검증, mock이 실제 경계를 가림, 회귀 결함의 재현, flaky test, no-new-test, 실행 불가를 포함한다. 정상 참조 동작의 부당한 실패, product/test/runner 오류 분류, 관찰·재현 불가능한 동작, 레퍼런스를 읽지 않아도 되는 단순 사례까지 구분한다. 타 컴포넌트 내부 구현 의존과 실제 소비자 계약 위반을 구분하고, 공유 fixture/state 충돌, 필요한 protocol 순서, 통합 예외를 점검한다.
- **Comparison** — 동일 사례를 일반 코딩 맥락 단독 조건과 새로운 Skill 적용 조건에서 평가한다. 독립적인 요구 명세·known-good/bad sample을 grader에 주되 테스트 대상 에이전트에는 정답을 누출하지 않는다.

## Conditional Reference

`references/oracle-validation.md`는 **불확실한 오라클·테스트 실패의 의미·강한 반례 검증**이 필요한 경우에만 로딩한다. 동일한 보통 테스트 설계 문제에서 불필요한 참조가 증가하거나 내용을 거의 항상 읽게 된다면 코어로 통합하거나 삭제할지 다시 평가한다. 평가 중 실제 로딩과 비용을 관찰하지 않았으면 progressive loading 효과를 주장하지 않는다.

## Interpretation

Fixture/schema 구조 검사는 deterministic test로 수행할 수 있으나 **행동 성능 검증은 실제 모델·런타임이 실행돼야 한다.** 관찰 가능한 defect discrimination을 실행할 수 있으면 deterministic oracle을 우선한다. 실제 코드를 실행할 수 없다면 모델의 설계 결과를 근거에 따라 평가하되 behavior execution 성공으로 올리지 않는다.

비교에서 개선과 퇴행을 함께 본다. 잘못된 oracle을 거부하는 비율이 올라가도 불필요한 E2E/mutation/서브에이전트 도입이나 토큰·실행 시간이 크게 증가하면 순편익을 다시 판단한다.

실제 model/runtime, harness, source commit, 반복 횟수, grader/기준과 실패를 기록하기 전에는 효과, 안정성, 범용 호환성을 검증했다고 주장하지 않는다. 현재 fixture는 평가 설계이며 **실행 결과를 보유하지 않는다.**
