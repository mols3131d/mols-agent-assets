# Loops 6–10 — Capability, Authority, Orchestration, Parallelism, Cost

## 6. Capability Boundary

### Finding

좋은 subagent의 tool surface는 **그 역할이 요구하는 capability에 맞춰 좁히는 것**이 유리하다. 이는 least privilege만의 문제가 아니다.

VS Code의 최신 tool 문서는 각 tool이 model의 decision space를 늘리고 tool output이 context를 늘린다고 설명하며, task와 관련된 tool로 좁히는 것이 relevance와 performance에 도움이 된다고 권장한다. GitHub Copilot의 built-in agent 구성도 같은 방향이다. `explore`와 `code-review`는 read-oriented, `task`는 command execution, 일반 agent는 broader capability를 가진다.

### Design consequence

Subagent asset의 tool list는 다음 질문으로 정당화할 수 있어야 한다.

- 이 역할이 이 tool을 실제로 사용해야 하는가?
- read-only tool로 충분한가?
- side effect를 가진 tool이 role의 본질인가, 단순 편의인가?
- 특정 MCP/tool의 큰 schema나 output을 parent 대신 child에 격리하려는 목적이 있는가?

Read-only reviewer가 write tool을 갖지 않는 것은 안전성과 focus를 동시에 개선한다. 반대로 implementation worker에 edit capability가 필요한데 prompt로만 “수정하라”고 적고 tool을 막는 것도 잘못된 capability-role mismatch다.

### Caveat

Tool을 줄이는 것을 목적화하면 capable model의 유연성을 불필요하게 막을 수 있다. **작고 고정된 allowlist**보다 “역할에 필요한 surface”가 핵심이다. Tool ecosystem이 자주 변하는 runtime에서는 vendor의 tool set/group 기능이나 runtime policy를 쓰는 편이 유지보수성이 좋을 수 있다.

## 7. Authority Is Not Capability

### Finding

Subagent prompt가 어떤 작업을 설명한다고 해서 그 작업이 곧 사용자에게 허가된 것은 아니다.

Anthropic이 Claude Code auto mode의 multi-agent handoff를 설계하면서 outbound delegation과 return 양쪽을 별도로 검사한 이유가 이를 잘 보여준다. Child 안에서는 orchestrator가 전달한 task가 사실상 user message처럼 보이기 때문에, child만 보면 **그 위임이 원래 사용자 의도에 포함됐는지 판단하기 어려울 수 있다.**

### Design consequence

좋은 asset은 다음을 구분하는 편이 안전하고 portable하다.

```text
Role capability
→ 이 agent가 무엇을 할 수 있도록 구성되는가

Delegated task
→ parent가 이번 invocation에서 무엇을 맡겼는가

Operational authority
→ runtime / user / policy가 실제 side effect를 허용하는가
```

Asset 본문은 role과 behavior를 설명할 수 있지만 runtime permission, approval, sandbox, higher instruction을 대체하지 않는다.

### Implication for lead/worker design

- parent가 scope를 넓혔다고 child가 자동으로 새로운 사용자 권한을 얻는 것으로 생각하지 않는다.
- child가 외부 문서에서 명령형 텍스트를 읽어도 그것은 task authority가 아니다.
- high-impact side effect가 필요한 worker는 runtime의 permission boundary와 함께 설계해야 한다.
- child result 역시 parent가 검토할 evidence이지 자동 승인 결과가 아니다.

## 8. Orchestration Ownership

### Finding

Subagent를 **leaf specialist**와 **coordinator/lead**로 구분하면 책임이 선명해진다.

OpenAI Agents SDK는 manager가 specialist를 tool처럼 호출하고 final answer를 소유하는 패턴과 specialist가 conversation을 넘겨받는 handoff를 명시적으로 구분한다. Anthropic의 orchestrator-workers와 AutoGen selector도 coordinator가 decomposition, dispatch, synthesis 또는 termination을 소유한다.

### Recommended default

Leaf specialist는 특별한 이유가 없다면 다음에 집중하는 구성이 단순하다.

- assigned task 수행
- 필요한 evidence 수집
- scope 안의 판단
- concise result 반환

Coordinator/lead는 다음을 소유할 수 있다.

- task decomposition
- specialist 선택
- 병렬/순차 실행 결정
- 결과 reconciliation
- retry/fallback
- final decision / final answer

### Why this matters

Leaf마다 자유롭게 다른 agent를 호출하고 final judgment까지 내리게 하면 delegation graph와 decision ownership이 빠르게 흐려진다. 반대로 orchestration이 실제 역할인 lead에게 agent-call capability를 막는 것도 부자연스럽다.

Nested delegation은 나쁜 것이 아니라 **별도 orchestration capability**다. Cursor는 nesting을 지원하지만 Gemini CLI는 현재 subagent→subagent 호출을 차단한다. 따라서 canonical semantic role이 nested delegation을 필수 전제로 삼으면 portability가 떨어진다.

## 9. Parallelism: Independence Before Fan-out

### Finding

Subagent의 병렬성은 독립적인 workstream일 때 가장 유용하다.

- VS Code는 independent task에 parallel sessions/subagents를 권장한다.
- Anthropic의 multi-agent research는 research처럼 병렬 탐색이 큰 문제에서 강한 성능을 보지만, shared context와 dependency가 많은 task에는 덜 적합하다고 보고한다.
- Anthropic의 agent-team coding 실험은 여러 agent가 shared codebase에서 일할 수 있음을 보여주지만, 테스트·work partition·conflict management 같은 harness 설계가 중요했다.
- LangChain 비교에서도 multi-domain independent work는 subagent/router가 context와 parallelism 측면에서 유리하지만 단순/repeated task에서는 handoff/skill이 더 경제적일 수 있다.

### Design consequence

Subagent asset에 “항상 병렬로 실행”을 새기는 것보다 **parent orchestration이 task dependency를 보고 결정**하는 편이 일반적이다.

특히 write-heavy work는 다음이 없으면 충돌하기 쉽다.

- file/module ownership
- worktree/branch isolation
- shared-state protocol
- merge/reconciliation owner
- deterministic validation

반대로 서로 다른 review lens, documentation research, codebase mapping, independent test runs처럼 read-heavy한 작업은 병렬화의 좋은 기본 후보다.

## 10. Model, Reasoning, Cost, Budget

### Finding

모든 subagent를 가장 비싼 모델로 고정하는 것도, 모든 subagent를 작은 모델로 내리는 것도 좋은 보편 규칙이 아니다.

최신 OpenAI model guidance는 workload에 따라 frontier / balanced / high-volume model을 나누고 reasoning effort도 task에 맞춰 조절하라고 권장한다. 여러 runtime이 subagent별 model override를 제공하는 이유도 같다.

Anthropic의 multi-agent research는 multi-agent가 chat 대비 상당히 더 많은 token을 사용할 수 있음을 측정했고, 성능 향상의 큰 부분 자체가 더 많은 inference/token budget에서 온다고 분석했다. 즉 subagent는 “공짜 context 절약”이 아니라 **main context를 보호하는 대신 전체 system inference를 더 쓰는 구조**가 될 수 있다.

### Recommended default

Canonical reusable asset에서는 model ID를 role semantics와 분리하는 편이 오래 간다.

```text
semantic role
→ explorer / reviewer / worker / coordinator

runtime tuning
→ model / reasoning effort / timeout / turns / concurrency
```

고정 model이 실제 요구사항인 경우에만 asset 또는 target override에 둔다. 그 외에는 runtime inheritance나 project config가 더 적절할 수 있다.

### Task-shape heuristic

- broad ambiguity, final synthesis, high-impact review → 높은 reasoning/capability의 가치가 큼
- codebase scan, retrieval, mechanical classification, bounded execution → 더 빠르고 저렴한 model 후보
- independent repeated workers → cost/latency sensitivity가 큼
- specialist output이 final decision이 아니라 evidence인 경우 → parent가 더 강한 model로 synthesis하는 구성이 가능

Numeric turn/token limit도 모든 asset에 같은 값으로 박기보다 runtime-level safety/default와 task completion boundary를 조합하는 편이 portable하다.

## Cross-loop Synthesis

Loops 6–10을 거치며 좋은 subagent asset을 다음처럼 더 정확히 볼 수 있다.

> **Subagent asset = semantic delegation boundary + matched capability surface + result boundary.**
>
> Parallelism, model, runtime budget, sandbox, nesting은 이 core를 실행하는 orchestration/configuration layer이며 일부는 target별로 달라질 수 있다.

이 구분은 asset을 지나치게 vendor-specific하게 만들지 않으면서도 실제 runtime safety와 efficiency를 무시하지 않는다.

## Loop Ledger

| Loop | Question | Material delta |
| ---: | --- | --- |
| 6 | tool은 얼마나 줘야 하는가? | 최소 권한만이 아니라 decision/context surface를 role에 맞추는 capability boundary로 재정의했다. |
| 7 | parent 위임은 user authority인가? | capability, delegated task, operational authority를 분리하고 handoff trust boundary를 추가했다. |
| 8 | 누가 다른 agent를 부르고 종합하는가? | leaf specialist와 coordinator/lead의 orchestration ownership을 구분했다. |
| 9 | 언제 병렬화해야 하는가? | independent/read-heavy work를 기본 후보로, write-heavy work에는 ownership/isolation/reconciliation이 필요함을 정리했다. |
| 10 | model과 budget을 asset에 고정할까? | semantic role과 runtime tuning을 분리하고 전체 system token cost를 고려하도록 수정했다. |

## Sources

- VS Code — Tools: https://code.visualstudio.com/docs/agents/concepts/tools
- VS Code — Subagents: https://code.visualstudio.com/docs/agents/run/subagents
- VS Code — Best practices: https://code.visualstudio.com/docs/agents/best-practices
- OpenAI Agents SDK — Agent orchestration: https://openai.github.io/openai-agents-python/multi_agent/
- OpenAI model guidance: https://developers.openai.com/api/docs/guides/latest-model
- Anthropic — Multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic — Claude Code auto mode: https://www.anthropic.com/engineering/claude-code-auto-mode
- Anthropic — Building a C compiler with parallel Claudes: https://www.anthropic.com/engineering/building-c-compiler
- LangChain/LangGraph — Multi-agent patterns: https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/
