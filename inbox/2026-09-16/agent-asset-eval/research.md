# Promptfoo 기반 Agent Asset Eval 조사

이 문서는 이 repository의 Agent Asset을 Promptfoo로 평가하는 방법을 조사하고, 현재 eval 구조를 어떤 방향으로 확장할지 정리한다. 구현이나 canonical policy 변경은 이 문서의 범위가 아니다.

## 결론

이 repository에서 가장 적합한 방향은 **Promptfoo를 eval contract의 owner로 만들지 않고, 실제 runtime을 실행하는 비교·채점 backend로 사용하는 것**이다.

핵심 구조는 다음과 같다.

1. Eval은 먼저 **무슨 behavior claim을 증명할지** 정의한다.
2. Agent Asset 평가는 크게 **Routing**과 **Behavior**로 나눈다.
3. Promptfoo 실행은 두 lane으로 분리한다.
   - **Fast contract lane**: 현재 custom provider처럼 fixture·adapter·grader 연결과 좁은 routing/behavior contract를 빠르게 확인한다.
   - **Native runtime lane**: Claude Agent SDK, Codex SDK, OpenCode처럼 실제 agent harness가 Skill을 발견·호출하도록 실행해 runtime evidence를 얻는다.
4. Grader는 **observable outcome을 deterministic하게 확인하는 방법을 최우선**으로 사용한다.
5. `skill-used`, trace, model judge는 outcome을 보완한다. 호출되었다는 사실만으로 좋은 behavior를 증명하지 않고, trajectory가 contract가 아닌 경우 특정 실행 경로를 정답으로 고정하지 않는다.
6. Candidate 비교에서는 model, task, tools, permissions, workspace를 고정하고 **Agent Asset만 교체**한다.
7. Model judge는 calibration과 holdout 없이 merge truth로 취급하지 않는다.
8. Capability eval과 regression eval을 분리하고, 안정적으로 지켜야 할 behavior만 regression으로 승격한다.

즉, 목표는 “Promptfoo 기능을 최대한 많이 쓰는 것”이 아니라 **실제 Agent Asset의 선택과 결과를 가장 적은 오판으로 측정하는 것**이다.

## 현재 repository의 출발점

현재 repository policy는 이미 좋은 경계를 갖고 있다.

- behavioral contract와 fixture → [`evals/`](../../../evals/README.md)
- Promptfoo-specific config → `evals/promptfoo/`
- reusable adapter와 runner → `scripts/agent_assets/`
- 평가의 의미와 evidence discipline → [`docs/development/evaluation.md`](../../../docs/development/evaluation.md)
- Agent Asset Eval contract → `mols-agent-asset`의 routing/behavior/evidence references

특히 현재 정책은 다음을 명확히 구분한다.

- deterministic grader인지 여부가 아니라 **무엇을 측정하는지**로 Test와 Eval을 구분한다.
- Runtime을 실행하지 않았으면 runtime performance를 verified라고 주장하지 않는다.
- Outcome을 먼저 평가하고, trajectory 자체가 계약일 때만 중간 실행 경로를 평가한다.
- Promptfoo는 실행 backend이지 canonical eval contract가 아니다.

이 원칙은 외부 Agent Eval 권고와도 정합적이다.

### 현재 구현에서 잘 된 점

현재 `mols-loops` eval은 다음 장점이 있다.

- trigger/routing과 behavior를 분리한다.
- positive와 negative routing case가 함께 있다.
- fixture는 `evals/skills/mols-loops/cases.json`이 소유하고 Promptfoo config가 이를 소비한다.
- trigger selection은 Python assertion으로 deterministic하게 판정한다.
- behavior는 구조적 출력 확인과 semantic rubric을 분리한다.
- smoke와 runtime eval을 별도로 둔다.
- Promptfoo sharing/cache를 기본적으로 끄고 local evidence로 다룬다.

이 구조는 버릴 대상이 아니라 확장 기반으로 보는 편이 낫다.

### 현재 한계

현재 `evals/promptfoo/`에는 `mols-loops` 전용 config만 있고, runtime provider도 repository custom Python adapter + Ollama 중심이다.

따라서 현재 결과는 다음 질문에는 유용하지만:

- fixture와 adapter가 연결되는가?
- Skill text를 주어진 model이 읽었을 때 원하는 응답을 내는가?
- synthetic routing candidate set에서 기대 selection을 반환하는가?

다음 질문을 직접 증명하지는 않는다.

- 실제 Claude/Codex/OpenCode runtime이 Skill을 자동 discovery하고 호출했는가?
- 실제 runtime의 tool/permission/context behavior 안에서도 계약이 유지되는가?
- 같은 task에서 current asset과 candidate asset 중 어느 쪽이 더 안정적인가?
- runtime별 projection 또는 harness 차이에서 behavior가 어떻게 달라지는가?

따라서 **현재 lane을 유지하면서 native-runtime lane을 추가**하는 것이 자연스럽다.

## 외부 조사

### Promptfoo: Agent Skill 비교가 first-class use case가 됨

Promptfoo의 현재 공식 가이드는 Agent Skill 비교를 직접 다룬다.

[Testing Agent Skills](https://www.promptfoo.dev/docs/guides/test-agent-skills/)의 핵심은 다음과 같다.

- 같은 task를 두 Skill version에 실행한다.
- model, source fixture, permission은 고정하고 `SKILL.md`만 교체한다.
- “Skill이 필요할 때 실제로 사용되었는가?”와 “사용 후 결과가 더 좋아졌는가?”를 분리한다.
- neighboring Skill이 있을 때는 near-miss prompt를 추가해 잘못된 Skill을 호출하지 않는지도 본다.
- Claude Agent SDK, Codex SDK, OpenCode SDK에서 Skill 비교 예시를 제공한다.
- `skill-used`로 실제 Skill 호출 evidence를 확인할 수 있다.
- 필요하면 trace를 추가해 Skill file read, tool call, command 등을 확인한다.
- nondeterminism이 material하면 `--repeat`를 사용하고 candidate가 비슷하면 failure를 직접 읽는다.

이 방식은 현재 repository의 Routing Eval / Behavior Eval 구분과 거의 동일하다.

### Promptfoo: `skill-used`는 routing evidence이지 quality evidence가 아님

[Deterministic metrics](https://www.promptfoo.dev/docs/configuration/expected-outputs/deterministic/)는 `skill-used`와 `not-skill-used`를 제공한다.

현재 Promptfoo는 다음 provider에서 Skill usage metadata를 normalize한다.

- Claude Agent SDK
- OpenAI Codex SDK
- OpenCode SDK
- 일부 Codex Security operation

단, Skill이 호출되었다고 해서 결과가 좋은 것은 아니다. 따라서 다음처럼 사용해야 한다.

- Routing claim → `skill-used`, `not-skill-used`
- Behavior claim → deterministic outcome/state 또는 semantic grader
- 특정 tool/gate 자체가 계약 → trajectory assertion

이 세 층을 하나의 PASS로 뭉개지 않는 것이 중요하다.

### Promptfoo: outcome과 trajectory를 분리해 평가 가능

Promptfoo는 trace가 있는 agent run에서 다음 assertion을 제공한다.

- `trajectory:tool-used`
- `trajectory:tool-args-match`
- `trajectory:tool-sequence`
- `trajectory:step-count`
- `trajectory:goal-success`

Sources:

- [Tracing](https://www.promptfoo.dev/docs/tracing/)
- [Assertions & metrics](https://www.promptfoo.dev/docs/configuration/expected-outputs/)
- [Evaluate Coding Agents](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/)

이 repository에는 trajectory를 넓게 적용할 필요가 없다. 예를 들어 다음처럼 **중간 행동 자체가 계약인 경우**에 한정하는 것이 맞다.

- 반드시 특정 Skill 또는 subagent가 선택되어야 함
- 필수 confirmation/gate를 건너뛰면 안 됨
- 잘못된 authority/tool을 사용하면 안 됨
- 금지된 mutation이나 side effect가 없어야 함
- handoff 또는 termination이 observable contract임

반대로 동일한 outcome에 여러 정상 경로가 가능한 경우 tool sequence를 고정하면 Agent Asset이 아니라 현재 implementation detail에 과적합된다.

### Promptfoo: grader가 workspace evidence를 봐야 하면 `agent-rubric`

[Agent Rubric](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/agent-rubric/)은 grader가 repository나 artifact를 직접 확인해야 할 때 사용할 수 있다.

예:

- 최종 응답이 실제 생성 파일을 정확히 설명하는지
- repository의 특정 state와 응답 claim이 일치하는지
- 단순 output text만으로는 확인할 수 없는 artifact quality인지

이 경우에도 grader workspace는 가능한 read-only로 두고, candidate output과 workspace content를 **untrusted evidence**로 취급해야 한다.

단순 semantic output quality라면 `agent-rubric`까지 사용할 이유가 없고 `llm-rubric`이 더 싸고 단순하다.

### Promptfoo: model judge는 calibration이 선행되어야 함

[LLM as a Judge](https://www.promptfoo.dev/docs/guides/llm-as-a-judge/)는 다음을 권장한다.

- 처음에는 한 가지 명확한 pass/fail criterion으로 시작한다.
- human-labeled pass/fail sample로 judge agreement를 측정한다.
- development sample에서 rubric을 튜닝한 뒤 holdout에서 다시 확인한다.
- candidate output을 untrusted data로 취급하는 judge prompt를 사용한다.
- judge model과 설정을 가능한 고정한다.
- drift가 의심되면 human review로 재교정한다.

공식 가이드는 예시로 90% 이상 agreement를 calibration 목표로 제시한다. 이 수치는 universal contract로 복제하기보다, **우리 grader가 사람의 의도와 충분히 일치하는지 측정해야 한다는 원칙**으로 받아들이는 편이 적절하다.

### Promptfoo: candidate 비교는 `max-score`와 `select-best`의 역할이 다름

- [`max-score`](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/max-score/) — 이미 계산된 objective score를 조합해 가장 높은 candidate를 선택
- [`select-best`](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/select-best/) — model judge가 여러 output 중 상대적으로 더 좋은 것을 선택

따라서 Agent Asset 비교에서는 다음 순서가 적절하다.

1. correctness / routing / forbidden action 같은 objective metric을 먼저 측정
2. objective metric이 충분하면 `max-score`
3. subjective quality가 실제 결정 기준이고 objective signal로 구분하기 어려울 때만 `select-best`

“judge가 더 마음에 드는 답”을 primary winner metric으로 만드는 것은 피한다.

### Promptfoo: 반복 trial을 native하게 지원

[Test case configuration](https://www.promptfoo.dev/docs/configuration/test-cases/)은 case별 `options.repeat`를 제공하며, CLI `--repeat`도 사용할 수 있다.

Agent Skill 공식 가이드는 close comparison에서 repeat를 사용하도록 권장한다. Cache가 결과를 재사용하지 않게 fresh trial이 필요하면 `--no-cache`를 함께 사용한다.

초기 기본값으로는 다음 정도가 현실적이다.

- 빠른 개발 feedback → 1 trial
- candidate 비교 또는 flaky behavior 확인 → 3 trials
- high-risk regression 또는 결과가 경계선인 case → 필요한 case만 더 반복

반복 횟수를 ritual로 고정하기보다 stochastic variability가 decision을 바꿀 수 있는 곳에 집중한다.

### Anthropic: agent eval은 outcome, transcript, environment를 함께 봐야 함

Anthropic의 [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)는 agent eval에서 task, trial, grader, transcript, outcome, harness를 구분한다.

특히 이 repository에 직접 적용할 만한 원칙은 다음과 같다.

- 처음부터 수백 case를 만들 필요는 없다. 실제 수동 검증과 failure에서 대표 task를 먼저 모은다.
- positive와 negative를 균형 있게 둔다.
- task가 grader의 hidden requirement를 숨기면 안 된다.
- clean, isolated environment에서 trial을 실행한다.
- outcome을 deterministic하게 확인할 수 있으면 그것을 우선한다.
- model grader는 human judgment와 calibration한다.
- capability eval과 regression eval을 분리한다.
- transcript를 읽어 target failure와 eval failure를 구분한다.

Anthropic은 초기 일반 지침으로 20–50개의 representative task도 충분히 유용할 수 있다고 설명한다. 다만 이 repository에서는 **자산마다 20–50개를 기계적으로 채우는 목표로 쓰지 않는다.** 중요한 failure surface를 대표하는 최소 set에서 시작하고 family 단위로 dataset을 키우는 편이 KISS하다.

### OpenAI: broken eval은 model 성능보다 더 큰 문제를 만들 수 있음

OpenAI의 [Separating signal from noise in coding evaluations](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)는 2026년 SWE-Bench Pro audit에서 broken task의 주요 원인으로 다음을 지적한다.

- prompt에 없는 implementation detail을 test가 강제
- hidden test가 요구하는 조건이 prompt에 없음
- test coverage 부족으로 불완전한 solution이 통과
- prompt가 grader expectation과 충돌

Agent Asset eval에도 그대로 적용된다.

즉, eval case의 목적은 candidate를 함정에 빠뜨리는 것이 아니라 **실제 계약 위반을 식별하는 것**이다. Assertion이나 hidden reference가 user-visible task보다 더 많은 요구사항을 몰래 추가하면 안 된다.

## 권장 Evaluation Model

### 1. Claim-first

각 eval case 또는 suite는 먼저 하나의 명확한 claim에 연결한다.

예:

- “`mols-agent-asset`은 Agent Skill 수정 요청에서 선택된다.”
- “일반 제품 코드 리뷰에는 `mols-agent-asset`이 선택되지 않는다.”
- “선택된 뒤 Validation과 Eval을 구분한다.”
- “runtime evidence가 없는데 verified라고 주장하지 않는다.”

Promptfoo assertion은 claim을 구현하는 수단이다.

### 2. Routing Eval과 Behavior Eval을 분리

#### Routing

대표 case:

- positive
- negative
- near-miss
- ambiguous
- composite
- bypass/adversarial

측정:

- expected Skill/agent 선택 여부
- false positive / false negative
- sibling Skill 오선택
- primary/secondary routing 충돌
- 불필요한 double routing

Promptfoo mapping:

- native Skill runtime → `skill-used`, `not-skill-used`
- custom router → Python/JavaScript assertion
- 충분한 dataset → precision / recall / F1 집계

#### Behavior

측정 우선순위:

1. 최종 state / artifact / structured result
2. required / forbidden observable behavior
3. semantic quality
4. contract일 때만 trajectory
5. cost / latency / step count 같은 secondary efficiency

Promptfoo mapping:

- deterministic state → Python/JavaScript/custom assertion
- open-ended semantic quality → `llm-rubric`
- grader가 workspace를 직접 확인해야 함 → `agent-rubric`
- traced end-to-end goal → `trajectory:goal-success`
- required tool/gate → trajectory assertions

### 3. 두 개의 실행 lane

#### Lane A — Fast contract lane

목적:

- fixture schema
- case selection
- adapter wiring
- deterministic grader
- cheap semantic smoke
- description/routing 후보의 빠른 비교

현재 `skills_promptfoo.py` 기반 구조를 이 lane으로 유지할 수 있다.

이 lane의 결과는 실제 target runtime이 Skill을 discovery/call했다는 evidence로 확장 해석하지 않는다.

#### Lane B — Native runtime lane

목적:

- 실제 runtime discovery
- native Skill invocation
- tool/permission/context interaction
- 실제 runtime outcome
- cross-runtime difference

Skill의 경우 Promptfoo가 현재 직접 지원하는 Claude Agent SDK, Codex SDK, OpenCode SDK를 우선 활용할 수 있다.

각 runtime에서 같은 case bank를 최대한 재사용하되 결과를 하나의 평균으로 무조건 합치지 않는다. Runtime, model, tool set, projection은 system under evaluation의 일부다.

### 4. 같은 candidate 비교에서는 Asset만 바꾼다

A/B 비교의 기본 fixture는 다음을 같게 둔다.

- model과 reasoning setting
- task
- repository/workspace fixture
- tool access
- permission
- runtime/harness
- output schema
- grader

다르게 두는 것은 원칙적으로 Agent Asset revision뿐이다.

이 isolation이 깨지면 “candidate Skill이 좋아졌다”가 아니라 “system setup이 달라졌다”는 결과가 된다.

### 5. capability와 regression을 분리

#### Capability

- 아직 잘 못하는 어려운 case를 포함할 수 있다.
- pass rate가 낮아도 suite 자체의 실패가 아니다.
- asset improvement의 hill-climbing signal이다.

#### Regression

- 이미 안정적으로 지켜야 하는 핵심 behavior다.
- broken fixture가 아니며 반복해서 재현 가능해야 한다.
- merge admission에 쓰려면 grader와 runtime variance까지 감당할 수 있어야 한다.

Capability case가 충분히 안정되고 지속적으로 보호할 가치가 있을 때 regression으로 승격한다.

### 6. development와 holdout을 분리

Asset text와 rubric을 같은 case에 반복적으로 맞추면 eval overfitting이 생긴다.

따라서 case metadata에 최소한 다음 구분을 두는 것을 검토할 가치가 있다.

- `split: dev | holdout`
- `purpose: capability | regression`
- `risk: low | medium | high`
- `source: manual | incident | review | user-failure`

현재 fixture schema를 바로 바꾸자는 의미는 아니다. 구현 시 schema 확장이 실제 filtering/reporting 가치가 있는지 먼저 확인한다.

## Asset 유형별 적용

### Skill

Promptfoo와 가장 잘 맞는다.

권장 최소 eval:

1. positive routing
2. negative routing
3. sibling near-miss
4. 대표 behavior outcome
5. 한두 개의 중요한 forbidden behavior
6. 필요하면 repeated trial

Native runtime에서는 `skill-used` + outcome을 함께 본다.

### Rule / scoped instruction

현재 Promptfoo에는 Skill의 `skill-used`처럼 범용적인 `rule-used` signal이 없다. 따라서 Rule은 **적용되는 context와 적용되지 않는 context를 paired fixture로 구성하고 behavior delta를 평가**하는 편이 낫다.

예:

- matching path에서 rule behavior가 나타남
- non-matching path에서 같은 behavior를 강제하지 않음
- 더 좁은 instruction 또는 authority와 충돌 시 repository가 정의한 precedence를 따름

현재 `evals/README.md`는 Skill과 Subagent placement는 정의하지만 Rule eval placement는 별도로 정의하지 않는다. Rule eval을 실제 구현하기 전에 placement owner를 먼저 정해야 하며, research 단계에서 임의의 `evals/rules/`를 canonical path로 만들지 않는다.

### Agent / Subagent

평가 축은 다음 두 가지다.

- Routing/delegation — 필요한 상황에서 위임하는가, 불필요한 상황에서 위임하지 않는가
- Handoff/behavior — 위임 뒤 결과가 usable한가, authority/scope가 유지되는가, termination이 올바른가

Runtime이 delegation tool call을 trace로 노출하면 deterministic/custom trajectory assertion을 사용하고, 최종 결과는 별도 outcome grader로 본다.

특정 subagent 호출 횟수나 exact sequence를 계약으로 만들 필요가 없으면 경로를 고정하지 않는다.

## Grader 전략

우선순위는 다음과 같다.

| 상황 | 우선 grader |
| --- | --- |
| JSON/schema/state/selection이 명확함 | deterministic Python/JS |
| 실제 file/test/state로 판정 가능 | deterministic outcome check |
| output semantic quality가 핵심 | `llm-rubric` |
| grader가 workspace evidence를 조사해야 함 | `agent-rubric` |
| 여러 objective metric으로 candidate 선택 | `max-score` |
| subjective pairwise preference가 실제 결정 기준 | `select-best` |

Model judge를 사용할 때는 다음을 지킨다.

- rubric은 한 번에 너무 많은 개념을 섞지 않는다.
- task에 없는 hidden requirement를 추가하지 않는다.
- candidate output을 untrusted data로 취급한다.
- grader transport/parse/context failure와 target failure를 분리한다.
- representative human labels와 주기적으로 calibration한다.
- grader model/version이 바뀌면 이전 score와 동일 measurement라고 가정하지 않는다.

## Metrics

모든 metric을 하나의 total score로 합칠 필요는 없다.

### Primary

- routing accuracy / precision / recall / F1
- behavior success rate
- critical failure count
- deterministic outcome pass rate

### Stability

- repeated trial별 pass/fail
- case별 variance
- 같은 failure pattern의 반복 여부

작은 sample에서는 소수점 score에 통계적 의미를 과장하지 않는다.

### Secondary

- token/cost
- latency
- tool/command count
- unnecessary delegation

Efficiency는 correctness가 비슷한 candidate 사이의 tie-breaker로 쓰는 것이 기본이다. Budget 자체가 contract일 때만 primary gate로 올린다.

## Candidate 개선 루프

권장 workflow:

1. 현재 asset을 baseline으로 고정
2. 실제 failure 또는 명확한 capability claim에서 case 추가
3. baseline을 먼저 실행해 case/grader가 기대대로 작동하는지 확인
4. candidate asset 생성
5. 같은 runtime/setup에서 baseline과 candidate를 side-by-side 실행
6. deterministic outcome과 routing을 먼저 비교
7. 필요한 경우 semantic quality와 efficiency 비교
8. close result면 fresh repeated trial 실행
9. failure output/trace를 직접 표본 검토
10. improvement가 holdout에서도 유지되는지 확인
11. 안정적인 중요한 case만 regression으로 승격

이 흐름에서는 eval이 asset text를 “최적화하는 정답지”가 아니라 **실패를 재현하고 개선을 검증하는 measurement surface**가 된다.

## 이 repository에 대한 우선 적용 제안

첫 구현 대상은 모든 자산을 한 번에 덮는 universal evaluator보다 **Skill native-runtime eval**이 적합하다.

이유:

- 현재 fixture와 generic evaluator가 이미 Skill 중심으로 존재한다.
- Promptfoo가 현재 Skill invocation을 first-class로 지원한다.
- Routing/Behavior split이 이미 repository contract에 있다.
- 가장 적은 새 abstraction으로 runtime evidence를 추가할 수 있다.

우선순위 후보:

1. `mols-loops` — 기존 case bank와 baseline이 있어 native lane 비교에 가장 좋음
2. `mols-agent-asset` — routing boundary와 behavior contract가 명확함
3. `mols-agent-asset-find` — sibling near-miss와 ownership boundary eval에 적합함

특히 `mols-agent-asset` / `mols-agent-asset-find`는 서로의 near-miss가 되므로 routing precision을 확인하기 좋은 pair다.

## 구현 전 결정해야 할 사항

다음은 research에서 결론을 내리기보다 구현 단계에서 실제 cost와 runtime support를 확인해야 한다.

1. Native runtime lane의 첫 provider를 Codex SDK로 할지 Claude Agent SDK로 할지
2. Runtime fixture를 temporary directory로 만들지 repository fixture directory로 둘지
3. Asset revision A/B fixture를 copy 방식으로 둘지 provider가 동적으로 materialize할지
4. Repeated trial 결과의 canonical report를 저장할지 disposable evidence로 둘지
5. Rule eval placement를 어디서 소유할지
6. CI에서 native runtime eval을 blocking, bounded blocking, deferred 중 어디에 둘지

현재 repository policy상 실제 model/runtime eval은 기본적으로 non-blocking evidence이므로, 처음부터 PR Gate 전체에 넣기보다 local/deferred evidence로 시작하는 편이 자연스럽다.

## 제안하는 다음 단계

1. `mols-loops` 기존 eval을 baseline으로 보존한다.
2. Promptfoo direct agent provider를 사용하는 `mols-loops` native-runtime prototype을 하나 만든다.
3. 기존 trigger fixture 일부를 `skill-used` / `not-skill-used`로 재실행해 synthetic routing과 실제 runtime routing 차이를 확인한다.
4. behavior case 3–5개만 골라 deterministic outcome 또는 좁은 rubric으로 native result를 비교한다.
5. 3-repeat fresh run으로 variability와 cost를 측정한다.
6. 결과를 보고 공통 runner가 필요한지 판단한다.
7. 그 다음 `mols-agent-asset` / `mols-agent-asset-find` pair로 routing family eval을 확장한다.

처음부터 모든 runtime, 모든 asset type, 모든 metric을 일반화하지 않는다. **한 Skill에서 실제 runtime evidence를 end-to-end로 만드는 것이 첫 milestone**이다.

## Sources

### Repository

- [`docs/development/evaluation.md`](../../../docs/development/evaluation.md)
- [`evals/README.md`](../../../evals/README.md)
- `src/rulesync/.rulesync/skills/mols-agent-asset/references/common/eval.md`
- `src/rulesync/.rulesync/skills/mols-agent-asset/references/eval/routing.md`
- `src/rulesync/.rulesync/skills/mols-agent-asset/references/eval/behavior.md`
- `src/rulesync/.rulesync/skills/mols-agent-asset/references/evidence.md`
- `evals/skills/mols-loops/cases.json`
- `evals/promptfoo/mols-loops.yaml`
- `scripts/agent_assets/skills_promptfoo.py`

### Promptfoo official

- <https://www.promptfoo.dev/docs/guides/test-agent-skills/>
- <https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/>
- <https://www.promptfoo.dev/docs/configuration/expected-outputs/deterministic/>
- <https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/agent-rubric/>
- <https://www.promptfoo.dev/docs/guides/llm-as-a-judge/>
- <https://www.promptfoo.dev/docs/tracing/>
- <https://www.promptfoo.dev/docs/configuration/test-cases/>
- <https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/max-score/>
- <https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/select-best/>

### Agent eval practice

- Anthropic, *Demystifying evals for AI agents*: <https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
- OpenAI, *Separating signal from noise in coding evaluations*: <https://openai.com/index/separating-signal-from-noise-coding-evaluations/>
