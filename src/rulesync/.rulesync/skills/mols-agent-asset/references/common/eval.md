# Common Eval

Evaluation은 **표현된 계약이 실제로 얼마나 잘 작동하는지** 평가한다. Validation이 계약 준수를 판정한다면 Eval은 실제 선택과 행동의 성능을 본다.

## Choose the eval

| 종류 | 핵심 질문 | 추가 reference |
| --- | --- | --- |
| Routing Eval | 필요한 자산이나 실행 단위를 올바르게 선택하고 호출하는가? | `../eval/routing.md` |
| Behavior Eval | 선택된 뒤 의도한 행동과 결과를 얼마나 잘 수행하는가? | `../eval/behavior.md` |

하나의 scenario에 선택과 실행이 모두 중요하면 둘 다 평가한다. Orchestration은 별도 최상위 유형으로 만들지 않는다. 누구를 선택·위임했는지는 Routing Eval, 호출 이후 협력·handoff·결과는 Behavior Eval로 본다.

## Methods, not types

다음은 별도 Eval 유형이 아니라 Routing 또는 Behavior Eval에 적용하는 방법과 비교 조건이다.

- positive, negative, near-miss, ambiguous, failure case
- adversarial challenge
- baseline과 regression 비교
- stability와 repeated trials
- variant 또는 configuration 비교
- simulation, runtime output, observable state, trace

Repeated trial은 stochastic variability를 보기 위한 독립 실행이고 Review loop와 다르다. 같은 case를 여러 번 읽는다고 trial 수를 늘리지 않는다.

## Evidence and graders

Evidence level은 `../evidence.md`를 따른다. 실제 runtime을 실행하지 않았으면 실제 performance를 `verified`로 주장하지 않는다.

Observable state나 label로 판정할 수 있으면 deterministic grader를 우선할 수 있다. 의미 품질처럼 deterministic 판정이 부적절하면 model 또는 human judgment를 사용할 수 있다. **Grader가 deterministic하다는 이유로 Eval이 Validation이 되는 것은 아니다. 무엇을 측정하는지가 경계를 결정한다.**

Outcome을 먼저 평가하고, 특정 tool call, confirmation, authority gate, side effect처럼 trajectory 자체가 계약일 때만 필요한 중간 행동을 평가한다.

여러 reviewer, trial, grader 또는 evidence source를 합치면 `../eval/reconciliation.md`를 읽는다. Prior result나 baseline과 fresh하게 비교하면 `../revalidation.md`도 읽는다.
