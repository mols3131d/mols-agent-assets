# Loops 21–25 — Evaluation, Regression, Maintainability

## 21. Routing Eval: 먼저 “잘 선택되는가”를 분리해서 본다

### Finding

Subagent의 `description`, name, invocation metadata가 실제 automatic delegation에 쓰이는 runtime에서는 **routing 자체가 독립적인 behavior surface**다.

GitHub Copilot SDK는 user prompt를 각 agent의 `name`과 `description`에 맞춰 intent matching한 뒤 candidate를 고르고, `infer` 설정으로 automatic selection 자체를 끌 수 있다고 설명한다. OpenAI Agents SDK의 handoff도 `handoff_description`을 routing hint로 사용한다.

따라서 agent 본문이 훌륭해도 잘못 선택되면 전체 시스템 behavior는 나쁘다. 반대로 본문 behavior 테스트만으로 description 품질을 판단할 수 없다.

### Recommended eval shape

Routing fixture는 다음 세 종류가 유용하다.

```text
positive
→ 이 specialist가 분명히 적합한 요청

negative
→ 이름/keyword는 비슷하지만 맡으면 안 되는 요청

near-miss / overlap
→ 인접 specialist와 구분이 필요한 요청
```

현재 review trio에 적용한다면 desired behavior를 먼저 명시한 뒤 다음 같은 case를 만들 수 있다.

| Intent | Expected candidate |
| --- | --- |
| quality와 adversarial 두 독립 검토를 조정해 final assessment를 달라 | `review-lead` |
| correctness, regression, validation만 독립 검토하라 | `review-quality` |
| hidden assumption과 reachable failure path를 공격적으로 찾아라 | `review-adversarial` |
| 코드를 직접 구현하라 | none of these reviewers |
| 단순 설명/요약만 달라 | 보통 none; 실제 project routing policy에 따름 |

실제 runtime이 parent가 직접 이름으로 호출하는 구조라면 automatic-selection eval의 우선순위는 낮아질 수 있다.

### Key principle

**Discovery/routing eval과 selected-agent behavior eval을 섞지 않는다.** 잘못 route된 실패를 body prompt 결함으로 오진하면 description과 본문을 모두 불필요하게 비대하게 만들 수 있다.

## 22. Behavior Eval: 선택된 뒤 무엇을 하고 무엇을 하지 않는가

### Finding

Subagent behavior eval은 final prose 품질보다 **역할의 observable contract**에 가깝게 설계하는 편이 안정적이다.

Anthropic의 2026 agent eval guidance는 agent 평가에서 transcript/trajectory와 최종 environment outcome을 구분하고, deterministic/code-based grader와 model-based grader를 함께 쓰는 것을 권장한다. OpenAI Agents SDK 역시 tool call, handoff, guardrail 등을 trace로 관찰할 수 있다.

### Useful axes

```text
Task completion
→ 맡은 질문/작업을 실제로 닫았는가

Scope
→ 다른 specialist나 parent 책임까지 침범하지 않았는가

Tool behavior
→ 필요한 tool을 썼는가 / 금지된 side effect를 하지 않았는가

Evidence quality
→ finding이 검증 가능한 근거와 연결되는가

Uncertainty
→ 모르는 것, 실행하지 못한 것을 과장하지 않는가

Return quality
→ parent가 재탐색 없이 다음 판단을 할 만큼 distilled 되었는가
```

### Current review specialists

`review-quality`의 좋은 regression case는 다음처럼 만들 수 있다.

- correctness defect를 evidence와 함께 발견
- style-only issue를 중요한 finding으로 승격하지 않음
- focused test만 실행하고 full-suite pass라고 주장하지 않음
- dependency installation/autofix를 임의 수행하지 않음
- adversarial speculation으로 scope를 넓히지 않음

`review-adversarial`은 다음을 볼 수 있다.

- reachable counterexample를 찾음
- existing guard가 hypothesis를 막으면 finding을 철회/낮춤
- theoretical possibility를 confirmed defect로 표현하지 않음
- general maintainability/style review로 역할을 바꾸지 않음

Final wording의 exact match보다 이런 behavior assertion이 model revision에 덜 취약하다.

## 23. Orchestration Eval: lead는 final answer만 평가하면 부족하다

### Finding

Coordinator/lead asset은 final prose가 좋아 보여도 내부 delegation이 계약과 다를 수 있다. 따라서 중요한 orchestration은 **trace/trajectory evidence**로 평가하는 것이 좋다.

OpenAI Agents SDK tracing은 agent runs, turns, tool calls, handoffs, guardrails를 span으로 기록한다. GitHub Copilot SDK도 subagent lifecycle event를 parent session에 스트리밍한다. 이런 runtime에서는 orchestration을 observable하게 만들 수 있다.

### `review-lead` eval candidates

```text
Delegation
→ quality + adversarial 모두 호출했는가

Independence
→ 한 reviewer의 finding을 다른 reviewer의 initial prompt에 anchor로 넣지 않았는가

No redundant third pass
→ lead가 specialist와 같은 전체 review를 또 수행하지 않았는가

Reconciliation
→ duplicate/root-cause finding을 통합하고 disagreement/unknown을 숨기지 않았는가

Failure propagation
→ 한 reviewer가 blocked/failed라면 최종 assessment에서 누락하지 않았는가

Authority
→ source edit / merge / approve 같은 금지 side effect를 하지 않았는가
```

병렬 실행 자체는 runtime과 task independence에 따라 optional일 수 있다. Asset이 “지원되면 병렬”이라고 정의한다면 parallelism은 optimization evidence이지 correctness의 단일 pass/fail 조건으로 두지 않는 편이 자연스럽다.

### Why traces matter

Final answer만 grading하면 다음 실패가 숨을 수 있다.

- 한 specialist를 아예 호출하지 않고 lead가 역할을 흉내 냄
- 금지된 tool을 썼지만 결과는 좋아 보임
- reviewer failure를 숨김
- 필요 이상으로 여러 agent를 fan-out해 비용을 폭증시킴

## 24. Regression, Trials, and Model Variance

### Finding

Agent runtime output은 non-deterministic하므로 **한 번의 semantic PASS/FAIL을 절대적인 asset 품질로 취급하면 안 된다.**

Anthropic은 task, trial, grader, transcript, outcome을 구분하고 model output variance 때문에 여러 trial을 실행해 더 안정적인 측정을 만들 것을 권장한다. 또한 capability eval과 regression eval을 구분한다.

### Layered validation

Subagent asset에는 다음 계층이 실용적이다.

```text
Level 1 — static / deterministic
frontmatter, target projection, links, tool identifiers, forbidden metadata drift

Level 2 — routing / plumbing smoke
candidate discovery, generated config, invocation wiring

Level 3 — semantic behavior eval
representative positive / negative / failure cases

Level 4 — runtime orchestration / trace
actual subagent invocation, tool calls, handoff, permission, result integration

Level 5 — repeated / cross-model evidence
important or unstable cases만 multiple trials / model matrix
```

모든 level을 모든 PR에서 실행할 필요는 없다. 빠르고 안정적인 lower level은 merge gate 후보가 되고, 비용과 variance가 큰 runtime eval은 selected/manual/nightly evidence로 시작할 수 있다.

### Capability vs regression

- **Capability suite**: 아직 어려운 case를 넣고 어느 정도까지 할 수 있는지 hill-climb한다.
- **Regression suite**: 이미 안정적으로 수행하는 behavior를 거의 항상 지키는지 본다.

반복적으로 안정된 failure pattern과 grader가 확보된 뒤 regression gate로 승격하는 편이 single-run semantic judge를 즉시 CI blocker로 만드는 것보다 신뢰도가 높다.

### Grader choice

가능하면 가장 싼 직접 evidence부터 쓴다.

```text
schema / exact state / tool trace
→ deterministic assertion

semantic quality / evidence sufficiency
→ rubric/model grader

subjective or high-stakes calibration
→ periodic human review
```

같은 model이 자기 결과를 채점하는 구성이 편할 수는 있지만 독립 judge나 deterministic outcome을 쓸 수 있다면 correlated blind spot을 줄이는 데 도움이 된다.

## 25. Maintainability and Human Comprehension

### Finding

Subagent asset은 model만 읽는 prompt가 아니라 사람이 routing, tool, authority, target behavior를 유지보수하는 **configuration asset**이기도 하다.

최신 capable model에 맞는 좋은 방향은 “모든 edge case를 prose로 선제 차단”하기보다 **작고 명확한 semantic boundary + 실제 실패를 반영한 최소 correction**에 가깝다.

OpenAI의 current model guidance도 관련 tool만 노출하고 system prompt 중복을 줄이는 lean configuration이 최신 모델의 효율과 eval 결과에 도움이 될 수 있음을 보여준다. 이는 subagent prompt를 무조건 짧게 만들라는 뜻은 아니지만, 지침 하나하나가 material behavior를 소유하는지 묻는 근거가 된다.

### Maintenance checklist

- `description`이 실제 routing 책임을 설명하는가
- body가 description을 반복하기보다 execution guidance를 소유하는가
- tool list가 역할과 맞고 stale vendor identifier가 아닌가
- target-specific config가 portable semantic core와 섞이지 않았는가
- project instructions/Skill/reference를 불필요하게 복사하지 않았는가
- failure/unknown을 표현할 길이 있는가
- final decision owner가 명확한가
- 새 instruction이 실제 failure/eval evidence를 해결하는가
- agent가 커졌다면 progressive disclosure 또는 external reference가 더 적합한가

### Relationship to current repository patterns

현재 repository의 최근 reference patterns와도 연결된다.

- **Progressive Context Routing**: description/index로 후보를 좁힌 뒤 필요한 agent-local context만 로드한다.
- **Asset Configuration Surface**: reusable semantic core와 project/target-specific model, permission, path, schema delta를 분리할 수 있다.
- **Routing & Index Assets**: agent catalog/discovery가 커질 때 candidate location과 routing intent를 별도 surface에서 관리할 수 있다.

이들은 subagent-specific contract가 아니라 설계 선택을 설명하는 reference pattern으로 활용하는 편이 맞다.

## Proposed Eval Matrix for Current Review Trio

| Surface | `review-lead` | `review-quality` | `review-adversarial` |
| --- | --- | --- | --- |
| Routing | dual independent review coordination | correctness/regression/validation | counterexample/failure/trust boundary |
| Negative routing | single specialist work, implementation | adversarial-only, implementation | ordinary quality/style, implementation |
| Tools | can invoke allowed reviewers; no source mutation | read/search/test; no edit/agent | read/search only; no edit/agent |
| Core behavior | fan-out, reconcile, final assessment | evidence-linked quality findings | evidence-linked adversarial hypotheses/findings |
| Non-action | no merge/approve/source edit | no mutation/final approval | no mutation/final approval |
| Failure | reviewer failure visible | unverified stays unverified | speculation stays speculation |
| Trace | both reviewers called independently | no nested delegation | no nested delegation |
| Output | synthesized assessment | concise evidence for lead | concise hypothesis/evidence for lead |

이 matrix는 바로 rigid schema로 만들기보다 실제 supported runtime에서 먼저 representative cases를 돌린 뒤 stable contract를 결정하는 출발점으로 보는 것이 좋다.

## Loop Ledger

| Loop | Question | Material delta |
| ---: | --- | --- |
| 21 | 잘못된 agent 선택을 어떻게 검증할까? | routing을 body behavior와 분리하고 positive/negative/near-miss fixture를 도출했다. |
| 22 | specialist body는 무엇을 평가할까? | prose match보다 scope/tool/evidence/uncertainty/result behavior를 우선하는 eval 축을 만들었다. |
| 23 | lead orchestration을 어떻게 검증할까? | final text 외 delegation/independence/reconciliation/failure/authority를 trace로 검사하는 matrix를 추가했다. |
| 24 | model variance와 CI gate를 어떻게 다룰까? | static→routing→semantic→runtime→repeated evidence의 validation ladder와 capability/regression 분리를 정리했다. |
| 25 | 시간이 지나도 관리 가능한 asset은? | lean semantic boundary, evidence-gated instruction growth, target drift와 human comprehension checklist를 도출했다. |

## Sources

- GitHub Copilot SDK — custom agents and orchestration: https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents
- OpenAI Agents SDK — handoffs: https://openai.github.io/openai-agents-python/handoffs/
- OpenAI Agents SDK — tracing: https://openai.github.io/openai-agents-python/tracing/
- OpenAI Agents SDK — orchestration: https://openai.github.io/openai-agents-python/multi_agent/
- Anthropic — Demystifying evals for AI agents: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- OpenAI latest model guidance: https://developers.openai.com/api/docs/guides/latest-model
