# 좋은 Subagent Asset 설계 리서치

> 상태: completed working research artifact
> 기준: `main` @ `c948a79bf105027323aac3ecebe3035da8597006`
> Research loops: **30 / 30**
> 범위: coding/knowledge agent harness에서 재사용하는 subagent definition과 orchestration boundary

## Conclusion

좋은 subagent asset의 핵심은 **강한 persona나 긴 workflow가 아니라, parent가 신뢰성 있게 위임할 수 있는 delegation boundary**다.

가장 중요한 설계 요소는 다음 순서로 수렴했다.

1. **Distinguishable responsibility** — 왜 이 일을 별도 agent에게 맡기는지 분명하다.
2. **Routing / invocation boundary** — 언제 이 agent를 후보로 선택할지 설명한다.
3. **Context boundary + task packet** — 필요한 context만 넘기고 탐색 noise는 child에 격리한다.
4. **Role-capability fit** — tool과 action surface가 실제 책임과 맞는다.
5. **Distilled return** — parent가 다시 탐색하지 않고 판단할 evidence와 uncertainty를 돌려준다.
6. **Clear orchestration owner** — worker와 final decision/synthesis owner가 구분된다.
7. **Portable semantics vs runtime config** — 역할의 본질과 vendor-specific 실행 설정을 분리한다.
8. **Behavioral evidence** — routing, behavior, orchestration을 실제 eval/trace로 검증한다.

현재 repository의 `review-lead`, `review-quality`, `review-adversarial`은 이 구조에 이미 상당히 잘 맞는다. 이번 research에서 **즉시 prompt를 더 길게 고쳐야 할 구조적 defect는 발견하지 못했다.** 가장 높은 다음 가치는 rewrite보다 routing/orchestration eval을 추가해 실제 실패를 찾는 것이다.

## Definition

이 문서에서 **subagent asset**은 실제 실행 중인 process 자체가 아니라, parent/orchestrator가 focused work를 위임할 수 있게 역할·지침·capability·routing 정보를 선언하는 reusable asset을 뜻한다.

Subagent의 구조적 특징은 단순한 specialization보다 **delegated execution boundary**에 있다.

```text
parent / orchestrator
        │
        ├─ candidate routing
        ├─ bounded task + relevant context
        ▼
 specialist subagent
        │
        ├─ focused responsibility
        ├─ matched capability
        ├─ isolated/focused work context
        └─ completion / partial / blocker
        ▼
 distilled result + evidence + uncertainty
        │
        ▼
 parent integrates / decides / routes onward
```

Skill이나 prompt도 specialized behavior를 제공할 수 있다. Subagent를 따로 두는 이유는 **별도 context, capability boundary, independent perspective, parallel workstream, delegated execution** 중 하나 이상이 실제 가치를 줄 때 강해진다.

## High-Confidence Principles

### 1. Responsibility Before Persona

좋은 specialist는 “세계 최고의 전문가” 같은 identity보다 **구별 가능한 coherent responsibility**가 먼저다.

좋은 경계의 예:

- read-only repository exploration
- correctness/regression review
- adversarial failure-path review
- focused test execution
- bounded implementation worker
- documentation/source research
- review/reconciliation coordinator

너무 넓어서 parent와 같은 일을 전부 하거나, 반대로 너무 잘게 쪼개 routing/coordination overhead만 늘리는 형태는 피하는 편이 좋다.

핵심은 narrowness 자체가 아니라 **meaningful delegation unit**이다.

### 2. Description Is Often Runtime Routing Surface

GitHub Copilot SDK는 request를 custom agent의 `name`과 `description`에 맞춰 intent matching한다. OpenAI Agents SDK의 handoff도 description을 routing hint로 쓴다. Gemini CLI도 description이 delegation 판단에 도움이 되도록 expertise와 사용 시점을 설명하라고 안내한다.

따라서 description은 가능한 한 다음 두 가지를 설명하면 좋다.

```text
What does this agent specialize in?
When is it a good candidate?
```

반복적인 near-miss가 확인되기 전부터 keyword와 negative rule을 과도하게 나열할 필요는 없다.

### 3. Context Isolation Is a Structural Benefit, Not Magic

Subagent의 큰 장점은 search hit, raw log, 여러 파일 탐색, 실패한 hypothesis 같은 **intermediate noise를 parent context에서 분리**할 수 있다는 것이다.

하지만 “separate context”의 exact semantics는 runtime마다 다르다. Parent conversation history는 분리돼도 project instructions, workspace, tools, model, permissions 일부는 상속될 수 있다.

따라서 portable asset은 “완전히 격리된다”고 가정하기보다 target runtime의 inheritance를 확인하는 편이 안전하다.

### 4. Delegation Quality Is Not Only an Asset Problem

좋은 reusable agent라도 parent가 `조사해`처럼 모호하게 위임하면 흔들릴 수 있다.

필요에 따라 parent가 다음을 전달하면 유용하다.

```text
Goal / question
Target / bounded scope
Relevant constraints
Relevant context or source location
Expected result / evidence
```

Rigid schema가 목적은 아니다. Child가 parent intent를 처음부터 재구성하느라 context를 낭비하지 않게 하는 것이 목적이다.

### 5. Tool Surface Should Match the Role

Tool 최소화는 security만의 문제가 아니다. Tool이 많으면 model의 decision surface와 tool-description context도 늘어난다.

다만 “도구 수가 적을수록 좋다”가 아니라 **role-capability fit**이 핵심이다.

- read-only reviewer → read/search/test처럼 필요한 capability
- implementation worker → edit/test 등 실제 작업에 필요한 capability
- coordinator → 필요한 child invocation capability

반대로 prompt에 “수정하라”고 적고 edit capability가 없거나, read-only reviewer에게 무관한 destructive tool을 주는 것은 모두 mismatch다.

### 6. Capability, Delegation, Authority Are Different

```text
Role capability
→ 이 agent가 무엇을 할 수 있게 구성됐는가

Delegated task
→ parent가 이번 invocation에 무엇을 맡겼는가

Operational authority
→ user / policy / runtime가 실제 action을 허용하는가
```

Asset text나 parent prompt만으로 새로운 user/runtime authority가 생기는 것은 아니다.

특히 side effect가 큰 worker나 nested handoff에서는 parent→child delegation boundary 자체를 trust boundary로 볼 필요가 있다.

### 7. Leaf Specialist and Coordinator Are Different Roles

Leaf specialist의 일반적인 책임:

- assigned task 수행
- 필요한 evidence 수집
- 자기 scope 안의 판단
- concise result 반환

Coordinator/lead가 소유하기 좋은 책임:

- decomposition
- specialist selection
- parallel/sequential scheduling
- retry/fallback
- reconciliation
- final decision / answer

Nested delegation 자체는 나쁜 것이 아니지만 vendor 지원 차이가 크다. Portable baseline에서는 leaf가 다른 agent 호출에 의존하지 않고, coordinator만 필요할 때 orchestration capability를 갖는 구조가 다루기 쉽다.

### 8. Parallelism Requires Independent Work

Read-heavy research, 서로 다른 review lens, independent test 같은 workstream은 병렬화와 잘 맞는다.

Write-heavy work는 다음이 없으면 충돌 위험이 커진다.

- file/module ownership
- workspace/worktree/branch isolation
- shared-state protocol
- reconciliation owner
- deterministic validation

Subagent asset에 “항상 병렬”을 박기보다 parent orchestration이 task dependency를 보고 선택하는 편이 일반적이다.

### 9. Return the Result, Not the Exploration History

Parent가 필요한 것은 child의 raw transcript보다 다음에 가깝다.

```text
answer / findings
evidence / location
important uncertainty / validation limits
partial result or blocker when relevant
useful follow-up only
```

Structured JSON은 automation이나 repeated field omission 같은 필요가 있을 때 쓰면 된다. Human/LLM lead가 종합하는 경우 concise Markdown/text가 더 낮은 ceremony일 수 있다.

### 10. Failure Is a Normal Result

Subagent는 항상 성공하지 않는다. Parent가 안전하게 이어갈 수 있게 다음 semantic state를 표현할 수 있으면 좋다.

- completed
- partial
- blocked
- not applicable

반드시 enum schema가 필요하다는 뜻은 아니다. 중요한 것은 “찾지 못함”을 “없음”으로 승격하거나, 수행하지 않은 validation을 pass로 표현하거나, failed child를 coordinator가 조용히 누락하지 않는 것이다.

## Portable Semantics vs Runtime Configuration

좋은 reusable source는 다음 두 layer를 구분하면 여러 harness에서 유지하기 쉽다.

### Portable semantic core

- identity / name
- delegation description
- responsibility / scope
- expected result
- essential capability intent

### Target/runtime projection

- exact tool identifiers
- model / reasoning effort
- timeout / max turns
- automatic inference / user visibility
- permissions / sandbox
- MCP wiring
- concurrency / nesting
- workspace isolation
- vendor-specific paths / schema

```text
Portable semantic core
        ↓
Rulesync / projection layer
        ↓
Copilot / Antigravity / other runtime config
        ↓
actual routing + behavior smoke
```

Canonical source가 parse된다는 것만으로 target behavior까지 검증된 것은 아니다.

## Runtime Divergence Worth Testing

Target별로 특히 차이가 큰 부분:

- parent history inheritance
- repository/project instruction inheritance
- tool inheritance/override
- model inheritance
- direct user invocation vs model-only invocation
- nested subagent support
- permission/sandbox behavior
- workspace/write isolation
- timeout/turn behavior

예를 들어 Gemini CLI는 current subagent recursion을 제한하는 반면, VS Code/Cursor에는 nested invocation surface가 있다. 이런 feature를 portable semantic core가 무조건 전제로 삼으면 target drift에 취약해진다.

## Subagent vs Other Asset Choices

| Need | Usually start with | Reason |
| --- | --- | --- |
| 항상 또는 path별로 적용되는 rule | instruction / Rule | structural scope에 자동 적용 |
| task에 따라 필요한 capability, knowledge, workflow | Skill | on-demand composition / progressive context |
| 사람이 명시적으로 실행하는 반복 task | prompt / command | 작은 reusable invocation unit |
| deterministic check/action | tool / script / hook | LLM 판단을 불필요하게 쓰지 않음 |
| 다른 instructions/tools를 가진 specialist role | custom agent | persistent role/config boundary |
| parent가 focused work를 별도 context에 위임하고 result만 필요 | subagent | delegated execution + context isolation |
| specialist가 conversation ownership을 이어받아야 함 | handoff | ownership transfer가 핵심 |
| fixed coordination / predictable sequence | workflow / code | deterministic control flow |

이 taxonomy는 배타적이지 않다.

2026년 VS Code에는 Skill을 forked context에서 subagent처럼 실행하는 experimental 기능도 있다. 즉 **Skill은 behavior/capability package이고 subagent는 execution mode가 될 수 있다.** Custom agent 역시 Skill을 사용하고 다시 subagent로 실행될 수 있다.

따라서 다음 두 질문을 분리하면 더 오래 간다.

```text
What behavior / knowledge package is needed?

How should this task execute and isolate context?
```

## Minimal Sufficient Asset Shape

아래는 규격이 아니라 **참고할 수 있는 작은 출발점**이다.

```markdown
---
name: <identity>
description: <bounded specialty + when useful>
<target capability/config only when needed>
---

# <Role>

<one-paragraph purpose / responsibility>

## Scope / Working Guidance

- <material role-specific boundaries>
- <material evidence/action guidance>

## Return

<what the parent needs back, when not obvious>
```

필요가 확인되면 다음을 확장한다.

- explicit Can / Cannot
- failure / blocker semantics
- tool/permission detail
- references
- structured output
- orchestration detail
- target-specific config

핵심은 모든 섹션을 채우는 것이 아니라 **각 instruction이 실제 material behavior를 소유하는 것**이다.

## Lean-Prompt Review

Subagent body의 문장마다 다음을 물을 수 있다.

1. 없으면 실제 routing/behavior/result failure가 생길 가능성이 있는가?
2. 상위 repository/project instruction이 이미 소유하는가?
3. runtime/tool permission이 deterministic하게 강제하는 내용을 prose로 반복하는가?
4. 이 specialist 고유의 책임인가?
5. 실제 failure/eval evidence를 해결하기 위해 추가된 문장인가?

지속적으로 아니면 제거하거나 더 자연스러운 owner로 옮길 후보가 된다.

최신 capable model을 약하다고 가정해 모든 edge case를 prose로 봉쇄하는 방식은 좋은 default가 아니다.

## Evaluation Strategy

### 1. Routing

Positive / negative / near-miss를 분리한다.

```text
explicitly appropriate
semantically adjacent but wrong
ambiguous between nearby specialists
```

Routing failure와 selected-agent body failure를 섞지 않는다.

### 2. Specialist behavior

- task completion
- scope
- tool behavior
- evidence quality
- uncertainty handling
- prohibited non-action
- return quality

Exact prose match보다 observable behavior를 우선한다.

### 3. Orchestration

Coordinator는 final text뿐 아니라 trace/trajectory가 중요하다.

- expected specialists called
- independence preserved where required
- no redundant imitation pass
- failures not hidden
- disagreement reconciled
- forbidden side effects absent

OpenAI Agents SDK 등 trace가 있는 runtime에서는 agent/tool/handoff spans로 이런 behavior를 관찰할 수 있다.

### 4. Layered validation

```text
static / deterministic
→ projection + routing smoke
→ semantic behavior eval
→ actual runtime orchestration / trace
→ repeated / cross-model evidence for important cases
```

모든 level을 모든 PR에 돌릴 필요는 없다.

### 5. Capability vs Regression

- capability suite → 아직 어려운 case에서 개선 여지를 측정
- regression suite → 이미 안정된 behavior가 계속 유지되는지 확인

Single-run semantic judge를 바로 merge blocker로 만들기보다 반복적으로 안정된 failure와 grader가 확보된 case를 regression gate로 승격하는 편이 안전하다.

## Current Repository Assessment

### `review-lead`

강점:

- review process와 final assessment의 owner가 분명함
- quality/adversarial을 독립적으로 위임
- lead가 제3의 중복 full review를 하지 않도록 경계
- delegated output/automation을 conclusive evidence로 취급하지 않음
- source mutation, merge/approve 같은 action을 제한

현재 개선 hypothesis:

- description routing이 실제 near-miss를 만드는지 eval
- downstream automation에서 field omission이 반복될 때만 return structure 검토

지금 prompt를 늘릴 근거는 부족하다.

### `review-quality`

강점:

- correctness/regression/maintainability/validation이라는 coherent lens
- read/search/test 중심 capability와 role fit이 좋음
- source mutation, nested delegation, final approval을 배제
- smallest relevant validation, evidence limitation, no full-suite extrapolation
- adversarial reviewer와 역할 경계가 분명함

### `review-adversarial`

강점:

- reachable counterexample, unsafe boundary, failure/recovery, trust boundary에 집중
- speculation을 confirmed defect로 승격하지 않음
- existing protection이 hypothesis를 막는지 확인
- read/search-only capability가 role과 잘 맞음
- general quality/style review를 반복하지 않음

### Overall

**구조적 rewrite 권장 없음.**

가장 높은 다음 작업 우선순위:

1. review trio routing fixtures
2. `review-lead` actual orchestration eval
3. specialist non-action / capability eval
4. Copilot/Antigravity generated projection validation
5. blocked/unknown reviewer result propagation case

Failure evidence가 나오면 그때 description/body/tool mapping을 가장 작은 delta로 개선하는 편이 좋다.

## Proposed Review Trio Eval Matrix

| Surface | `review-lead` | `review-quality` | `review-adversarial` |
| --- | --- | --- | --- |
| Routing | dual independent review coordination | correctness/regression/validation | counterexample/failure/trust boundary |
| Negative routing | single specialist work, implementation | adversarial-only, implementation | ordinary quality/style, implementation |
| Tools | may invoke allowed reviewers; no source mutation | read/search/test; no edit/agent | read/search; no edit/agent |
| Core behavior | delegate, reconcile, final assessment | evidence-linked quality findings | evidence-linked adversarial hypotheses/findings |
| Failure | child failure/unknown visible | unverified stays unverified | speculation stays speculation |
| Trace | both reviewers independently invoked | no nested delegation | no nested delegation |
| Return | synthesized assessment | concise evidence for lead | concise hypothesis/evidence for lead |

이 matrix는 rigid schema가 아니라 representative cases를 만들기 위한 시작점이다.

## Anti-Patterns

- **Persona-first** — identity는 화려하지만 routing/scope/result가 없음
- **Duplicate parent** — child가 parent와 똑같이 research/plan/implement/review/finalize 전부 수행
- **Tool buffet** — 역할과 무관한 tool까지 무차별 제공
- **Context dump** — parent history/repository knowledge를 무조건 child에 선주입
- **Raw transcript return** — isolation 후 모든 탐색 noise를 다시 parent에 복사
- **Prompt-only authority** — asset text가 runtime/user permission을 mint한다고 가정
- **Implicit final owner** — 누가 specialist output을 검증·수용하는지 불명확
- **Unlimited fan-out** — nesting과 parallelism 자체가 목적이 됨
- **Same critic N times** — 다른 이름만 붙인 동일 lens/model/context reviewer
- **Framework-driven proliferation** — subagent 기능이 있다는 이유로 모든 reusable behavior를 agent화
- **Over-specified micro-procedure** — capable model의 판단까지 긴 workflow로 고정
- **Blind inheritance** — tools/model/project context가 target마다 똑같이 상속된다고 가정

## Final Challenge to the Principles

최종 loop에서 앞선 결론을 반박해 본 결과 다음처럼 완화해야 정확했다.

- 좁은 역할이 항상 좋은 것은 아니다 → **distinguishable responsibility**가 중요
- tool이 적을수록 좋은 것은 아니다 → **role-capability fit**이 중요
- separate context가 total token을 항상 줄이지 않는다 → main context는 보호해도 total inference는 늘 수 있음
- structured output이 항상 낫지 않다 → downstream consumer/eval 필요가 있을 때 사용
- 모든 boundary를 body에 반복할 필요 없다 → higher owner/runtime가 소유하면 중복하지 않음
- subagent가 최신 모델 정확도를 보정하기 위한 장치만은 아니다 → context architecture, specialization, independence, parallelism의 선택

## Source Confidence

### High confidence — current official/vendor documentation

- OpenAI Agents SDK — Agents, Handoffs, Agent orchestration, Tracing
- GitHub Copilot — custom agents, subagents, customization cheat sheet, Agent Skills
- VS Code — custom agents, subagents, tools, Skills, prompt files
- Gemini CLI — subagents
- Anthropic engineering — context engineering, multi-agent research, agent evals, building effective agents

이 문서들의 **current runtime behavior**는 2026-08 기준이며 vendor update로 바뀔 수 있다.

### Medium confidence — cross-framework generalization

- leaf/coordinator separation
- role-capability fit
- distilled result boundary
- routing/body eval separation
- portable semantic core vs execution projection

여러 vendor에서 반복 관찰된 공통점을 repository-friendly pattern으로 일반화한 결론이다.

### Evidence-gated hypotheses

다음은 현재 repo에 아직 defect로 확정하지 않았다.

- review-agent description을 더 자세히 써야 한다
- specialist return을 schema화해야 한다
- model을 agent별로 고정해야 한다
- nested delegation을 추가해야 한다
- reviewer 수를 늘리거나 줄여야 한다

이들은 actual routing/orchestration eval failure가 생길 때 검토하는 편이 낫다.

## Durable Knowledge Candidate

향후 실제 eval evidence까지 쌓이면 `docs/references/patterns/`에 다음 reference capsule로 승격할 가치가 있다.

> **Subagent Asset Design** — delegation responsibility, routing, context/capability/result boundary, portable semantics와 runtime projection의 분리를 설명하는 reusable reference pattern.

현재 단계에서는 inbox research로 유지한다. 이 문서가 설명하는 것은 project mandatory contract가 아니라 이후 agent/subagent 설계에서 참고할 evidence-backed pattern candidate다.

## Loop Index

| Loops | Note | Theme |
| --- | --- | --- |
| 1–5 | [`01-foundations.md`](01-foundations.md) | definition, routing, responsibility, context, delegation, return |
| 6–10 | [`02-capability-orchestration.md`](02-capability-orchestration.md) | tools, authority, lead/leaf, parallelism, model/cost |
| 11–15 | [`03-portability-runtime-divergence.md`](03-portability-runtime-divergence.md) | inheritance, invocation, nesting, target projection, drift |
| 16–20 | [`04-failure-independence-repo-review.md`](04-failure-independence-repo-review.md) | failure, independent review, current repo, anti-patterns |
| 21–25 | [`05-evaluation-maintainability.md`](05-evaluation-maintainability.md) | routing/behavior/orchestration eval, regression, maintenance |
| 26–30 | [`06-final-challenge-synthesis.md`](06-final-challenge-synthesis.md) | alternatives, asset matrix, minimal shape, final challenge |

## Primary Sources

- OpenAI Agents SDK — https://openai.github.io/openai-agents-python/
- OpenAI Agent orchestration — https://openai.github.io/openai-agents-python/multi_agent/
- OpenAI Handoffs — https://openai.github.io/openai-agents-python/handoffs/
- OpenAI Tracing — https://openai.github.io/openai-agents-python/tracing/
- OpenAI latest model guidance — https://developers.openai.com/api/docs/guides/latest-model
- GitHub Copilot custom agents/subagents — https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents
- GitHub Copilot custom agent concepts — https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents
- GitHub Copilot customization cheat sheet — https://docs.github.com/en/copilot/reference/customization-cheat-sheet
- GitHub Copilot Agent Skills — https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- VS Code custom agents — https://code.visualstudio.com/docs/agent-customization/custom-agents
- VS Code subagents — https://code.visualstudio.com/docs/agents/run/subagents
- VS Code tools — https://code.visualstudio.com/docs/agents/concepts/tools
- VS Code Agent Skills — https://code.visualstudio.com/docs/agent-customization/agent-skills
- VS Code prompt files — https://code.visualstudio.com/docs/agent-customization/prompt-files
- Gemini CLI subagents — https://geminicli.com/docs/core/subagents/
- Cursor subagents — https://cursor.com/changelog/2-4
- Anthropic effective context engineering — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic multi-agent research — https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic agent evals — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Anthropic building effective agents — https://www.anthropic.com/engineering/building-effective-agents
- Rulesync — https://github.com/dyoshikawa/rulesync
