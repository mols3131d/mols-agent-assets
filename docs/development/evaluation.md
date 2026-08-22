---
description: Agent Asset의 behavioral evaluation을 설계·실행·해석하고 deterministic test, runtime evidence, regression contract를 구분할 때 사용하는 repository-local policy입니다.
---

# Evaluation

Evaluation은 repository correctness test만으로 충분히 판단하기 어려운 **Agent Asset의 behavior와 품질**을 평가합니다.

`evals/`가 behavioral contract를 소유합니다. Promptfoo 같은 도구는 contract의 authority가 아니라 실행·채점 backend입니다.

## Test와 Eval

Test와 Eval은 **grader가 deterministic인지가 아니라 무엇을 검증하는지**로 구분합니다.

- source, schema, generated artifact, repository invariant처럼 Agent behavior를 실행하지 않아도 판정할 correctness → `tests/`
- trigger 선택, instruction following, semantic quality, adversarial behavior, runtime/model 차이처럼 Agent behavior에 대한 claim → `evals/`
- behavioral eval도 observable outcome이나 state가 있으면 deterministic grader를 우선할 수 있습니다.
- runtime을 실제로 실행하지 않았다면 runtime behavior가 통과했다고 주장하지 않습니다.

## Ownership

- canonical Agent Asset → `src/rulesync/.rulesync/`
- repository correctness test → `tests/`
- behavioral contract와 fixture → `evals/`
- tool-specific eval config → `evals/promptfoo/`
- adapter와 runner → `scripts/evals/`
- Promptfoo 자체의 사용법과 upstream authority → [Promptfoo](../references/tooling/promptfoo.md)

`evals/` 내부 layout과 fixture ownership은 [`evals/README.md`](../../evals/README.md)가 소유합니다.

## Evaluation Contract

Eval을 만들기 전에 **무엇을 어떤 조건에서 증명하려는지** 먼저 고정합니다.

- **Claim** — 이 eval 결과가 뒷받침할 behavior 또는 quality claim
- **System under evaluation** — Agent Asset뿐 아니라 실제 model/runtime, projection, harness처럼 결과에 영향을 주는 실행 surface
- **Conditions** — 중요한 tool access, context, model/runtime 설정과 필요한 budget 또는 retry 조건
- **Success criteria** — 성공·실패를 가르는 observable outcome 또는 rubric

서로 다른 model, runtime, harness 또는 조건의 결과를 직접 비교하려면 차이가 결과를 왜곡하지 않을 정도로 evaluation setup을 맞춥니다. Setup이 바뀌면 그 차이를 결과와 함께 해석합니다.

## Eval을 추가할 때

다음 중 하나가 실제로 필요할 때 eval을 추가합니다.

- Agent Asset이 올바른 상황에서 선택되거나 동작하는지 확인
- 요구한 behavior와 금지한 behavior를 구분
- adversarial 또는 ambiguous input에서 중요한 boundary 확인
- model이나 runtime이 달라져도 핵심 behavior가 유지되는지 비교
- 반복해서 발견된 failure를 regression contract로 남김

단순히 case 수를 늘리기 위해 fixture를 추가하지 않습니다. 새 case는 보호하려는 behavior나 failure mode가 분명해야 합니다.

### Capability와 Regression

- **Capability eval**은 아직 불안정하거나 개선하려는 behavior의 현재 수준을 측정합니다. 낮은 pass rate 자체가 eval 실패를 의미하지 않습니다.
- **Regression eval**은 이미 지켜야 하는 behavior가 계속 유지되는지 확인합니다. 반복 가능한 성공 기준과 높은 신뢰도가 필요합니다.

Capability case가 충분히 안정되고 계속 보호할 가치가 생기면 regression contract로 승격할 수 있습니다. 불안정한 model judgment를 이름만 regression으로 바꿔 merge-blocking contract로 만들지 않습니다.

여기서 regression은 **평가 목적**을 뜻합니다. 파일 배치는 별개이며, `evals/regression/`은 [`evals/README.md`](../../evals/README.md)가 정의한 cross-asset deterministic invariant에만 사용합니다.

## Case Quality

- 실제 요구사항, 수동 검증, 반복된 failure에서 representative case를 우선합니다.
- behavior가 **발생해야 하는 case와 발생하면 안 되는 case**를 함께 검토해 한쪽으로만 최적화되는 것을 피합니다.
- task와 grader가 확인하는 조건은 서로 모순되거나 숨겨진 요구를 만들지 않아야 합니다.
- 정상적인 Agent가 해결할 수 없는 broken fixture, 잘못된 ground truth, flaky environment는 target failure와 분리합니다.
- 가능한 경우 known-good 또는 known-bad example로 task와 grader가 의도대로 판정하는지 sanity check합니다.
- target의 intended context보다 eval harness가 assertion, expected answer, hidden reference를 더 노출하면 contamination 가능성을 결과와 분리합니다.
- 같은 case를 반복 조정하며 Asset을 맞출수록 fixture 자체에 과적합할 위험이 커집니다. 새로운 evidence가 없는 cosmetic variation은 추가하지 않습니다.

## Outcome과 Trajectory

기본적으로 **목표 달성 outcome을 먼저 평가**합니다. Agent가 유효한 다른 경로를 찾을 수 있는데도 특정 tool sequence나 문장 형태를 강제하지 않습니다.

다만 다음처럼 중간 behavior 자체가 contract이면 trajectory도 평가할 수 있습니다.

- 잘못된 tool이나 authority surface를 사용하면 안 됨
- 필수 confirmation, scope gate, escalation을 건너뛰면 안 됨
- 최종 문장만으로는 실제 side effect 또는 state change를 확인할 수 없음

Trajectory grader는 필요한 invariant만 검사하고 하나의 정답 경로를 구현 세부로 고정하지 않습니다.

## Graders

- observable state나 구조로 판정할 수 있으면 code/deterministic grader를 우선합니다.
- semantic quality처럼 deterministic 판정이 부적절할 때 model grader를 사용합니다.
- 문자열 일치보다 의미가 중요한 contract를 억지 deterministic grader로 고정하지 않습니다.
- rubric은 한 번에 너무 많은 품질 개념을 섞지 말고 판정할 behavior를 구체적으로 적습니다.
- grader가 판단하기 위해 필요한 source/context가 있다면 실제 grading input에 제공되어야 합니다.
- model grader는 target과 별개의 failure source입니다. transport, parse, missing-context 같은 grader failure를 target failure로 간주하지 않습니다.
- 중요한 model grader는 representative sample을 사람의 판단이나 더 직접적인 evidence와 비교해 주기적으로 calibration합니다.

Grader를 바꾸면 같은 점수 이름이라도 이전 결과와 동일한 measurement라고 가정하지 않습니다.

## Evidence

먼저 **실제 target runtime을 실행했는지**를 구분합니다.

- **Fixture/plumbing evidence** — fixture, provider, adapter, assertion 연결이 작동하는지 검증합니다. Runtime behavior를 증명하지 않습니다.
- **Runtime evidence** — 실제 model/runtime과 harness를 실행한 결과입니다. 사용한 model/runtime, harness, fixture와 Agent Asset revision을 함께 해석합니다.

Runtime evidence의 신뢰도는 사용한 grader와 반복성에 따라 달라집니다. Observable outcome을 deterministic하게 판정할 수 있으면 가장 강한 merge evidence가 될 수 있습니다. Model-generated output이나 model grader에 의존하면 필요한 경우 여러 trial을 사용하고, 단일 PASS/FAIL을 기본 merge admission으로 사용하지 않습니다.

반복 가능한 failure pattern이 확인되면 원인을 Asset, fixture, harness/runtime/provider, grader로 분리합니다. 안정적인 contract로 만들 수 있을 때만 blocking regression으로 승격합니다.

Generated result는 기본적으로 disposable evidence입니다. Durable decision이나 regression contract가 생겼을 때만 canonical surface에 반영합니다.

## Promptfoo

Promptfoo는 현재 behavioral eval 실행 backend입니다. Repository-owned fixture를 Promptfoo 전용 contract로 복제하지 않습니다.

Fixture-mode smoke는 provider/generator/assertion plumbing을 검증하는 deterministic check이며 runtime behavior evidence가 아닙니다. 실제 model/runtime eval과 semantic grading은 기본적으로 비차단 evidence입니다.

Promptfoo-specific config와 실행 adapter는 `evals/promptfoo/`와 `scripts/evals/`가 소유합니다. Tool 사용법과 current upstream source는 [Promptfoo](../references/tooling/promptfoo.md), PR Gate 연결은 [Testing](testing.md)을 따릅니다.

## Review

Eval 변경이나 결과를 검토할 때 다음을 확인합니다.

- 이 eval이 뒷받침하려는 claim과 실제 tested system이 명확한가?
- 이 case가 실제 behavior 또는 failure mode를 보호하는가?
- repository test로 충분한 correctness를 behavioral eval로 중복하고 있지 않은가?
- outcome을 볼 수 있는데 불필요하게 특정 trajectory를 강제하고 있지 않은가?
- fixture가 특정 model/provider의 우연한 표현이나 현재 implementation에 과적합되지 않았는가?
- target이 eval-only fixture나 expected result를 볼 수 있어 점수가 오염되지 않았는가?
- grader와 harness의 실패를 target failure로 잘못 해석하지 않았는가?
- 결과의 증거 수준보다 강한 결론을 주장하고 있지 않은가?

특히 failure와 예상 밖의 PASS에서는 raw output 또는 필요한 trajectory를 표본 검토해 **target behavior, fixture, grader, harness 중 무엇이 결과를 만들었는지** 확인합니다.
