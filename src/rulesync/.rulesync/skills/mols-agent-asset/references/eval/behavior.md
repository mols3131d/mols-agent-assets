# Behavior Eval

Behavior Eval은 **선택된 뒤 자산이 의도한 행동과 결과를 실제로 얼마나 잘 수행하는지** 평가한다.

## Evaluate

Claim에 필요한 범위만 본다.

- task outcome과 correctness
- required action과 prohibited action
- tool use, permission, approval와 side effect
- guardrail과 failure handling
- subagent handoff, result usability와 termination
- output quality, completeness와 evidence quality
- safety와 harmful overreach
- latency, token/context use, 불필요한 call처럼 측정 가능한 efficiency
- 반복 실행에서의 stability와 failure pattern

## Outcome and trajectory

기본적으로 outcome을 먼저 평가한다. Agent가 유효한 다른 경로를 사용할 수 있는데 특정 tool sequence나 문장 형태를 정답으로 고정하지 않는다.

다만 잘못된 authority 사용, 필수 confirmation, 금지된 mutation, handoff 누락처럼 중간 행동 자체가 계약이면 trajectory도 평가한다.

## Cases and trials

Positive, failure, adversarial, regression case는 평가 방법이다. Repeated trial은 같은 조건에서 stochastic variability가 material할 때 사용한다. Trial 사이의 model, runtime, fixture, tool access가 달라지면 같은 measurement로 단순 합치지 않는다.

Observable outcome은 deterministic grader로 평가할 수 있고 semantic quality는 model/human rubric이 필요할 수 있다. Grader failure와 target failure를 구분한다.
