---
description: mols-test-design만의 선택 경계, 오라클 품질, 독립적 테스트 가능성과 검증 비용을 평가할 때 참고합니다.
---

# Test Design — Evaluation

[Goal and Principles](goal.md)의 테스트 설계 품질을 평가한다. 실행 지침의 정본은 `src/rulesync/.rulesync/skills/mols-test-design/SKILL.md`, 평가 사례의 정본은 `evals/skills/mols-test-design/cases.json`이다.

## Skill-specific claims

| 평가 대상 | 구별할 결과 |
| --- | --- |
| **선택 경계** | 테스트 전략·오라클·충분성의 판단이 실제 요청이면 선택하고, 일반 구현·CI 운영·runner 문제만 있는 요청에는 불필요하게 개입하지 않음. 구현 중 **실질적인 테스트 설계 하위 작업**은 놓치지 않음 |
| **오라클 신뢰성** | 근거 있는 정상 사례를 통과시키고 중요한 결함 사례를 거부함. 현재 구현이나 mutation 점수가 잘못된 기대값을 정당화하지 않음 |
| **수용 범위** | 주어진 테스트가 통과해도 요청한 패키지·연결 경로·소비자 계약이 빠졌으면 미검증으로 남김 |
| **실패 진단** | 제품 결함과 잘못된 expectation/fixture, 실행 환경 문제를 구별하거나 근거가 부족함을 표시함 |
| **독립적 테스트 가능성** | 다른 컴포넌트의 비공개 구현에 대한 결합을 줄이되 실제 계약·트랜잭션의 통합 위험을 보존함 |
| **최소 충분성** | 중요한 미검증 실패를 우선하고, 불필요한 테스트·과도한 mocking·강한 검증의 비용을 줄임 |

## Discriminating cases

**Positive / negative:** 테스트 설계가 명시된 요청과 실제 구현 작업에 포함된 테스트 설계 요청을 구분한다. 반대로 테스트가 부수적인 일반 코드 수정, CI 정책, worktree 격리 요청은 제외한다.

**Behavior:** 정상 동작을 거부하는 테스트, 잘못된 구현을 기준으로 복제한 기대값, mutation 점수는 높지만 빠진 acceptance, product/test/environment 원인 불확정, 공유 mutable fixture와 실제 컴포넌트 호환성 위험을 다룬다.

**Conditional reference:** `references/oracle-validation.md`의 추가 판단이 필요한 복잡한 오라클·반례 문제와 필요하지 않은 단순 회귀 테스트를 비교한다. 레퍼런스가 항상 로드되거나 의미 있는 판단 없이 비용만 늘린다면 분리의 가치가 약하다.

## Available local evaluation path

`mise run eval-mols-test-design`은 현재 45개 case를 Trigger/Behavior로 실행하는 Promptfoo 설정을 호출한다. Trigger·Behavior만 실행하려면 각각 `mise run eval-mols-test-design-trigger`, `mise run eval-mols-test-design-behavior`를 사용한다. 이 entrypoint에는 Ollama model/runtime과 Promptfoo가 필요하다.

Behavior 평가에서는 허용된 `references/oracle-validation.md`의 필요 여부를 **별도 모델 요청**으로 먼저 판단하고 선택된 파일만 읽어 본 응답에 제공한다. 실제 선택된 경로를 provider metadata의 `loaded_references`로 남기며, 지정된 양성·음성 사례에서는 이를 검증한다. **참조하지 않은 경우에도 선택 요청 자체의 비용은 발생**한다.

이 경로는 원본 Skill의 선택적 참조를 실험하기 위한 **로컬 평가 하네스**로, 각 target-native Agent의 파일 로딩·도구 호출 동작을 그대로 재현하지 않는다. Fixture·mock-based deterministic test와 실제 Ollama 기반 결과를 구분해 해석한다.

## Differentiating value

일반적인 코딩 판단만 사용하는 기준 조건과 Skill이 활성화된 조건을 비교할 때, **결함 판별·잘못된 오라클 거부·과잉 테스트 감소의 순효과**에 집중한다. 강한 검증이 불필요하게 늘거나 선택 경계가 넓어져 비용이 증가하는 퇴행도 함께 본다.

이 문서는 평가의 **고유 대상**을 소유한다. 공통 실행 환경 설정, grader 운용, 결과 재현성, 검증과 실제 모델 평가의 구분은 적용되는 평가 체계의 계약을 따른다. 실제 모델 평가 결과는 아직 확보하지 않았다.
