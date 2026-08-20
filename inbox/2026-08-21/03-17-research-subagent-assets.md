# 좋은 Subagent Asset 설계 리서치

> 상태: working research artifact
> 기준: `main` @ `c948a79bf105027323aac3ecebe3035da8597006`
> 범위: coding/knowledge agent harness에서 재사용하는 subagent definition과 그 orchestration boundary

## Research Question

좋은 **subagent asset**은 무엇을 정의해야 하며, 무엇을 정의하지 않는 편이 좋은가? 최신 고성능 모델과 여러 agent harness를 전제로 할 때 routing, context, capability, delegation, output, portability, evaluation을 어떻게 설계하는 것이 실용적인가?

여기서 subagent asset은 실제 실행 중인 agent process 자체가 아니라, parent/orchestrator가 특정 일을 위임할 수 있도록 역할·지침·capability·routing 정보를 선언한 재사용 가능한 자산을 뜻한다. Skill, tool, prompt, workflow와 겹치는 부분은 있지만 동일한 개념으로 취급하지 않는다.

## Executive Synthesis

좋은 subagent asset의 핵심은 **persona가 아니라 delegation boundary**다.

대표적으로 다음을 분명하게 만들수록 재사용성과 orchestration 품질이 좋아진다.

1. **언제 선택할지** — 이름보다 `description`과 routing cue가 실제 delegation에 중요하다.
2. **무엇을 맡는지** — 하나의 좁고 구별 가능한 책임과 종료 가능한 task boundary를 가진다.
3. **무엇을 보게 할지** — parent 전체 context를 복제하기보다 task에 필요한 context를 넘기고, noisy exploration은 별도 context에 가둔다.
4. **무엇을 할 수 있게 할지** — 필요한 tool/capability만 제공하고 read-only research/review와 write worker를 구분한다.
5. **무엇을 돌려줄지** — parent가 바로 판단·종합할 수 있는 distilled result, evidence, uncertainty, blocker를 반환한다.
6. **누가 최종 판단하는지** — leaf specialist와 coordinator/final decision owner를 구분한다.

Subagent를 추가하는 것 자체는 품질 향상이 아니다. 별도 context, 전문화, 독립 병렬 작업이 실제 이득을 주는 task에서 사용해야 한다. 여러 vendor와 framework 모두 multi-agent가 추가 token·latency·coordination cost를 만든다는 점을 전제로 한다.

## Working Model

```text
parent / orchestrator
        │
        ├─ routing signal
        │    name + description + invocation policy
        │
        ├─ bounded task handoff
        │    goal + target + constraints + relevant context + expected result
        │
        ▼
   specialist subagent
        │
        ├─ focused instructions
        ├─ matched tools / permissions
        ├─ local context / references
        └─ completion / failure boundary
        │
        ▼
 distilled result
 evidence + uncertainty + blocker
        │
        ▼
 parent integrates / decides / routes onward
```

이 모델은 manager-as-tools, spawned subagent, selector, agent-as-tool 같은 orchestration에 가장 자연스럽다. Handoff처럼 specialist가 conversation ownership을 넘겨받는 패턴은 result integration과 context semantics가 다를 수 있으므로 별도 선택지로 본다.

## Evidence Across Current Runtimes

| Source | 관찰 | 설계 시사점 |
| --- | --- | --- |
| OpenAI Agents SDK | manager가 specialist를 agent-as-tool로 호출하거나 handoff로 대화권을 넘기는 두 패턴을 구분하며, 전문화된 agent와 eval을 권장한다. | subagent asset은 orchestration ownership을 암묵적으로 섞지 않는 편이 좋다. |
| OpenAI model guidance | 최신 모델에서도 lean prompt와 관련 tool만 노출하는 구성이 token/cost와 eval 성능에 도움이 될 수 있다고 안내한다. | 더 많은 instruction/tool이 항상 더 좋지 않다. |
| GitHub Copilot | `name` + `description`으로 intent matching 후 isolated subagent를 선택하며, built-in agents도 explore/task/code-review/research처럼 책임·capability가 분리돼 있다. | description은 문서 설명이면서 runtime routing surface다. |
| VS Code | subagent 호출은 stateless하고 parent는 최종 result만 받는다. 모든 관련 context와 expected output을 task에 포함하라고 권장한다. | parent→child handoff 자체도 설계 대상이다. |
| VS Code tools | tool 수는 model의 decision space와 context를 늘리므로 관련 tool로 좁히는 것을 권장한다. | capability 최소화는 보안뿐 아니라 context/decision 효율 문제다. |
| Gemini CLI | description의 expertise/when/examples가 delegation reliability를 높이며, subagent는 독립 context와 제한된 tools를 가진다. 현재 nested subagent는 막는다. | semantic core는 nesting 같은 vendor feature에 의존하면 안 된다. |
| Cursor | subagent는 별도 context에서 병렬·전문화된 작업을 하며 prompt/tool/model을 조정할 수 있다. 최신 SDK는 nested subagent도 지원한다. | nesting과 inheritance는 runtime별 capability로 분리해야 한다. |
| Anthropic engineering | subagent는 깊은 탐색 context를 격리하고 lead에 distilled summary를 반환하는 context engineering 수단이다. | context isolation과 result compression이 핵심 가치다. |
| Anthropic multi-agent research | lead가 child에 objective, output format, tool/source guidance, clear boundary를 줘야 중복·누락을 줄일 수 있다고 보고한다. multi-agent token cost도 크다. | 좋은 asset만큼 좋은 delegation task packet이 중요하다. |
| LangChain/LangGraph | multi-agent 핵심을 context engineering으로 보고, subagents/skills/handoffs/router를 task shape에 따라 구분한다. | subagent가 필요 없는 문제를 skill이나 single-agent로 해결할 수 있다. |
| AutoGen | agent `description`을 selector가 실제 speaker 선택에 쓰며 termination 조건을 별도로 둔다. | role description과 termination/coordination이 execution behavior에 직접 관여한다. |

## Core Design Principles

### 1. Routing Contract

많은 runtime에서 `description`은 단순 UI 설명이 아니라 parent가 specialist를 선택하는 **routing input**이다. 따라서 좋은 description은 가능한 한 짧게 다음을 구별한다.

- 무엇에 전문화되어 있는가
- 언제 이 agent가 좋은 후보인가
- 인접 agent와 구별되는 핵심 경계가 무엇인가

Trigger phrase를 과도하게 나열하기보다 의미 경계를 분명히 하는 편이 최신 capable model과 유지보수 모두에 유리하다. Near-miss가 반복될 때만 negative cue나 example을 추가하는 방식이 낫다.

### 2. Narrow Responsibility

좋은 specialist는 일반적으로 한 가지 **판단 관점 또는 작업 책임**을 소유한다.

좋은 예:

- read-only codebase mapping
- correctness/regression review
- adversarial failure-path review
- focused test execution
- bounded implementation worker
- documentation/source research

나쁜 방향은 `research + plan + implement + review + final decision`처럼 parent 역할까지 한 asset에 흡수하는 것이다. 넓은 agent가 항상 나쁜 것은 아니지만, 별도 subagent로 둘 이유가 약해진다.

### 3. Context Boundary

Subagent의 가장 강한 구조적 장점 중 하나는 **noisy intermediate context를 parent와 분리하는 것**이다.

- search hit, raw logs, 여러 파일 탐색, 실패한 가설은 child context에서 소화한다.
- parent에는 결론뿐 아니라 그 결론을 판단하는 데 필요한 evidence와 uncertainty를 압축해서 돌려준다.
- parent history 전체를 무조건 child에 복제하는 것도, child에 아무 context도 주지 않는 것도 좋은 기본값은 아니다.

Context isolation은 runtime마다 완전한 격리를 뜻하지 않는다. project instruction, workspace, tools, memory의 inheritance 방식은 harness에 따라 다르므로 asset은 실제 runtime의 inheritance를 전제로 검증해야 한다.

### 4. Delegation Task Packet

재사용 agent definition만 잘 만들어도 parent가 `조사해`처럼 모호하게 위임하면 성능이 흔들린다. Anthropic의 multi-agent 연구에서도 vague task description은 worker 중복과 coverage gap을 만들었다.

일반적으로 parent가 child에 전달하면 유용한 정보는 다음과 같다.

```text
Goal / question
Target / bounded scope
Relevant constraints
Relevant context or source location
Expected result / evidence
```

모든 invocation에 rigid schema가 필요한 것은 아니다. 핵심은 child가 parent intent를 처음부터 재구성하느라 context를 낭비하지 않게 하는 것이다.

### 5. Result Contract

좋은 subagent는 작업 history 전체가 아니라 **parent가 다음 결정을 내리는 데 필요한 result**를 반환한다.

대표적인 내용:

- findings / answer
- evidence 또는 location
- 중요한 uncertainty
- blocked / not verified 상태
- parent가 알아야 할 follow-up

정형 JSON이 항상 필요한 것은 아니다. downstream automation이 실제로 schema를 소비할 때 structured output을 쓰고, 사람이 종합하는 review/research라면 짧고 추적 가능한 Markdown/text가 더 단순할 수 있다.

## Initial Anti-Patterns

- **Persona-first agent** — “세계 최고의 전문가” 같은 정체성은 길지만 실제 selection, scope, output이 불명확함.
- **Everything agent** — parent와 거의 같은 responsibility/tool surface를 가지면서 이름만 전문화됨.
- **Tool buffet** — 역할과 무관한 tool까지 전부 상속해 model decision space와 blast radius를 늘림.
- **Context dump** — parent history나 repository 전체 knowledge를 무조건 child에 선주입함.
- **Raw transcript return** — child가 탐색한 모든 로그와 사고 경로를 parent에 그대로 되돌려 context isolation 이점을 잃음.
- **Authority by prompt** — instruction에 “수정 가능”이라고 쓰는 것만으로 runtime permission/approval을 얻었다고 간주함.
- **Implicit final owner** — worker 결과를 누가 검증·통합·수용하는지 불명확함.
- **Forced multi-agent ceremony** — single agent/skill/tool로 충분한 작은 task도 무조건 여러 agent로 나눔.

## Current Repository: First Read

현재 `src/rulesync/.rulesync/subagents/`의 세 자산은 이 리서치의 주요 원칙과 상당히 잘 맞는다.

### `review-lead`

강점:

- orchestration과 final judgment를 명확히 소유한다.
- `review-quality`와 `review-adversarial`을 독립적으로 위임한다.
- specialist 결과를 결정적 증거로 취급하지 않는다.
- source 수정/merge 같은 권한과 final review 작성 권한을 분리한다.
- scope drift와 제3의 중복 full review를 막는다.

검토 후보:

- `description`이 역할은 정확히 설명하지만 automatic routing을 더 명확히 해야 하는 실제 실패 사례가 있는지 eval로 확인할 가치가 있다.
- 항상 두 reviewer를 호출하는 것은 이 agent가 “dual independent review lead”라면 일관된 선택이다. 작은 변경에서 비용이 크다는 이유만으로 일반화해 약화할 필요는 없다.

### `review-quality`

강점:

- correctness/regression/maintainability/validation이라는 한 관점을 소유한다.
- write/subagent/final-decision 권한을 배제한다.
- smallest relevant validation과 evidence limitation을 명확히 한다.
- adversarial 역할을 모방하지 말라는 경계가 있어 specialist diversity를 보존한다.

### `review-adversarial`

강점:

- reachable counterexample, trust boundary, failure/recovery에 특화돼 quality reviewer와 의미상 구별된다.
- speculation과 confirmed finding을 구별한다.
- write/orchestration/final-decision 권한을 가지지 않는다.

이 세 agent에서 당장 확인되는 큰 구조 결함은 없다. 이후 loop에서는 routing description, result shape, target portability, generated tool mapping, eval 가능성을 더 엄격하게 검토한다.

## Loop Ledger

| Loop | Question | Material delta |
| ---: | --- | --- |
| 1 | subagent asset의 본질은 무엇인가? | persona prompt보다 delegation boundary라는 working definition을 확정했다. |
| 2 | 자동 선택은 무엇에 의존하는가? | 여러 runtime에서 `description`이 실제 routing surface임을 교차 확인했다. |
| 3 | specialist의 적정 책임 폭은? | narrow/opinionated/single-viewpoint specialization을 기본 방향으로 정리했다. |
| 4 | child에 무엇을 전달해야 하는가? | goal/target/constraints/relevant context/expected result를 delegation packet의 핵심으로 정리했다. |
| 5 | child가 무엇을 반환해야 하는가? | raw transcript 대신 distilled result + evidence + uncertainty + blocker를 핵심 result contract로 정리했다. |

## Sources — Primary / Official

- OpenAI Agents SDK — Agent orchestration: https://openai.github.io/openai-agents-python/multi_agent/
- OpenAI Agents SDK — Agents: https://openai.github.io/openai-agents-python/agents/
- OpenAI model guidance: https://developers.openai.com/api/docs/guides/latest-model
- GitHub Copilot — custom agents and sub-agent orchestration: https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents
- GitHub Copilot — About custom agents: https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents
- VS Code — Custom agents: https://code.visualstudio.com/docs/agent-customization/custom-agents
- VS Code — Subagents: https://code.visualstudio.com/docs/agents/run/subagents
- VS Code — Tools: https://code.visualstudio.com/docs/agents/concepts/tools
- Gemini CLI — Subagents: https://geminicli.com/docs/core/subagents/
- Cursor — Subagents release: https://cursor.com/changelog/2-4
- Cursor SDK update / nested subagents: https://cursor.com/changelog/sdk-updates-jun-2026
- Anthropic — Effective context engineering for AI agents: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic — How we built our multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic — Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- LangChain/LangGraph — Multi-agent patterns: https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/
- AutoGen — Selector Group Chat: https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/selector-group-chat.html

## Research Status

5 / 30 planned substantive review loops complete. Next: capability/authority/orchestration/parallelism/model-cost, then portability, failure handling, current-repo critique, eval strategy, adversarial compression and final synthesis.
