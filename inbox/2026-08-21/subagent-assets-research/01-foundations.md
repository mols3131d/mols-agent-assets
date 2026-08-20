# Loops 1–5 — Foundations, Routing, Context, Delegation, Return

## 1. What Is a Good Subagent Asset?

### Finding

좋은 subagent asset의 핵심은 **persona가 아니라 delegation boundary**다.

Subagent asset은 parent/orchestrator가 특정 일을 별도 실행 context에 위임할 수 있도록 다음 중 필요한 부분을 선언하는 reusable asset으로 볼 수 있다.

- identity / routing cue
- bounded responsibility
- role-specific instructions
- tool/capability intent
- execution/context expectation
- return expectation

“세계 최고의 전문가” 같은 persona는 domain tone이나 perspective를 보조할 수 있지만, 언제 선택되고 무엇을 맡고 무엇을 반환할지 설명하지 못하면 좋은 delegation asset이 되지 않는다.

### Working model

```text
parent / orchestrator
        │
        ├─ select candidate
        ├─ give bounded task + relevant context
        ▼
 specialist subagent
        │
        ├─ focused role
        ├─ matched capabilities
        ├─ isolated/focused work context
        └─ completion / blocker
        ▼
 distilled result + evidence + uncertainty
        │
        ▼
 parent integrates / decides / routes onward
```

Subagent를 추가하는 것 자체는 품질 향상이 아니다. 별도 context, capability boundary, independence, parallelism 중 실제 이득이 있을 때 구조적 이유가 생긴다.

## 2. Routing Is Part of the Asset

### Finding

여러 current runtime에서 `description`은 단순한 인간용 설명이 아니라 **실제 candidate selection surface**다.

GitHub Copilot SDK는 request를 custom agent의 `name`과 `description`에 맞춰 intent matching한다. OpenAI Agents SDK handoff의 `handoff_description`도 routing hint가 된다. Gemini CLI 역시 description을 delegation 판단에 사용하도록 안내한다.

### Good routing description

대체로 다음 두 질문에 답하면 충분하다.

```text
What does this agent specialize in?
When is it a good candidate?
```

인접 agent와 반복적으로 혼동되는 경우에만 negative boundary나 example을 늘리는 편이 유지보수에 유리하다.

### Implication

Description과 body의 책임을 구분할 수 있다.

- description → candidate discovery / selection
- body → selected-agent execution

이 구분은 routing failure를 body prompt 문제로 오진해 asset을 불필요하게 비대하게 만드는 것을 줄인다.

## 3. Responsibility Should Be Distinguishable

### Finding

좋은 specialist는 “아주 좁다”기보다 **다른 agent와 구별 가능한 coherent responsibility**를 가진다.

대표적인 좋은 경계:

- repository exploration / mapping
- correctness + regression review
- adversarial counterexample / failure-path review
- bounded implementation worker
- focused test execution
- source/document research
- orchestration/reconciliation lead

### Anti-pattern

`research + plan + implement + review + approve + merge`처럼 parent와 거의 같은 responsibility를 가지면서 이름만 specialist인 agent는 별도 subagent가 되는 이유가 약해질 수 있다.

반대로 지나치게 잘게 쪼개 agent 수를 늘리면 routing ambiguity와 coordination cost가 커진다. 목표는 micro-agent가 아니라 **meaningful delegation unit**이다.

## 4. Context Boundary and Delegation Packet

### Finding

Subagent의 강한 구조적 장점은 **noisy intermediate context를 parent에서 분리할 수 있다는 것**이다.

Anthropic의 multi-agent research와 context-engineering 글은 worker가 광범위한 탐색을 자기 context에서 수행하고 lead에 compressed result를 반환하는 형태를 중요한 설계 원리로 설명한다. GitHub/VS Code/Gemini도 별도/isolated context를 subagent의 주요 특징으로 둔다.

다만 “별도 context”의 정확한 inheritance는 runtime마다 다르다. Parent conversation history는 분리돼도 project instructions, workspace, tool config 등이 적용될 수 있다.

### Parent → child task packet

Reusable agent definition이 좋아도 invocation이 모호하면 결과가 흔들린다. 다음 정보를 필요한 만큼 전달하는 것이 좋은 출발점이다.

```text
Goal / question
Target / bounded scope
Relevant constraints
Relevant context or source location
Expected result / evidence
```

Rigid schema가 목적은 아니다. Child가 parent intent와 target을 다시 추측하느라 context를 낭비하지 않게 하는 것이 목적이다.

### Context economy

Parent history 전체를 무조건 child에 복제하는 것도, 아무 relevant context 없이 task 한 줄만 주는 것도 좋은 일반 default가 아니다. **필요한 context만 전달하고 탐색 noise는 child에 남기는 것**이 핵심이다.

## 5. Return Boundary

### Finding

좋은 subagent는 작업 transcript 전체가 아니라 **parent가 다음 결정을 내리는 데 필요한 distilled result**를 반환한다.

대표적으로 유용한 요소:

- answer / findings
- evidence / location
- important uncertainty or validation limit
- blocker / partial state if relevant
- useful follow-up only

### Why

Subagent를 context isolation 목적으로 사용하면서 raw search hits, logs, exploratory dead ends를 parent에 그대로 복사하면 isolation의 이점이 사라진다.

Structured JSON이 항상 필요한 것은 아니다. Automation이 stable fields를 소비할 때 schema가 유용하고, human/LLM lead가 종합하는 review/research는 concise Markdown/text가 더 단순할 수 있다.

### Result ownership

Leaf result는 final truth가 아니라 parent/coordinator가 검증·통합할 evidence일 수 있다. 특히 review/research system에서는 specialist가 final approval/merge decision까지 가져가는 것보다 final owner를 분리하는 구성이 명확하다.

## Foundation Synthesis

Loops 1–5의 가장 작은 결론은 다음과 같다.

> 좋은 subagent asset은 **언제 선택할지, 무엇을 맡길지, 어떤 focused context/capability에서 일할지, parent에 무엇을 돌려줄지**를 이해하기 쉽게 만든다.
>
> Persona, 긴 workflow, 많은 tools는 이 경계를 더 잘 만들 때만 가치가 있다.

## Loop Ledger

| Loop | Question | Material delta |
| ---: | --- | --- |
| 1 | subagent asset의 본질은 무엇인가? | persona prompt보다 delegation boundary라는 working definition을 확정했다. |
| 2 | automatic selection은 무엇에 의존하는가? | name/description/handoff description이 실제 routing surface임을 교차 확인했다. |
| 3 | specialist의 적정 책임 폭은? | narrow 자체보다 distinguishable coherent responsibility가 중요하다고 정리했다. |
| 4 | child에 무엇을 전달해야 하는가? | context isolation과 goal/target/constraints/context/result expectation task packet을 결합했다. |
| 5 | child가 무엇을 반환해야 하는가? | raw transcript보다 distilled result + evidence + uncertainty/blocker를 핵심 return boundary로 정리했다. |

## Sources

- OpenAI Agents SDK — orchestration: https://openai.github.io/openai-agents-python/multi_agent/
- OpenAI Agents SDK — handoffs: https://openai.github.io/openai-agents-python/handoffs/
- GitHub Copilot — custom agents/subagents: https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents
- VS Code — Subagents: https://code.visualstudio.com/docs/agents/run/subagents
- Gemini CLI — Subagents: https://geminicli.com/docs/core/subagents/
- Anthropic — Effective context engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic — Multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
