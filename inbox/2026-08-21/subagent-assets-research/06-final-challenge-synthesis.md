# Loops 26–30 — Alternatives, Minimal Shape, Final Challenge

## 26. When NOT to Use a Subagent

### Finding

Subagent는 “specialized instructions가 있다”는 이유만으로 필요한 것이 아니다. **별도 execution context와 delegation boundary가 실제 이득을 줄 때** 가치가 커진다.

Anthropic은 agentic system을 설계할 때 가능한 가장 단순한 해법에서 시작하고, agent는 latency/cost를 대가로 task performance를 얻는 구조라고 설명한다. 최신 VS Code/GitHub customization도 instructions, prompt files, skills, custom agents, subagents를 서로 다른 목적의 surface로 구분한다.

### Subagent가 과할 가능성이 높은 경우

- 거의 모든 task에 적용되는 repository convention → standing/scoped instruction이 더 자연스러움
- 현재 parent가 수행할 task-specific procedure와 knowledge → Skill이 더 자연스러움
- 사람이 명시적으로 한 번 실행하는 reusable task template → prompt/command가 단순할 수 있음
- 결정론적 format/check/mutation → script/hook/tool이 더 안정적일 수 있음
- fixed sequence가 중요한 workflow → code/workflow orchestration이 더 예측 가능함
- specialist가 conversation ownership을 실제로 이어받아야 함 → runtime handoff가 더 직접적일 수 있음
- 별도 context에서 얻을 이득이 거의 없고 parent가 모든 intermediate state를 계속 알아야 함 → single agent가 단순함

### Subagent가 자연스러운 경우

- 깊은 탐색 intermediate context를 parent에서 격리하고 싶음
- 다른 tool/capability boundary가 필요함
- 독립적인 parallel workstream이 있음
- 다른 review/research lens를 독립적으로 유지하고 싶음
- parent가 decomposition/synthesis를 맡고 specialist가 bounded result를 반환하는 구조
- 큰 MCP/tool output을 좁은 worker context에 가두는 것이 유리함

즉 **specialization ≠ subagent requirement**다. Specialization은 Skill, prompt, tool, instruction으로도 만들 수 있고 subagent는 execution/context boundary라는 추가 특성이 있을 때 선택한다.

## 27. Asset Choice Matrix

### Working decision matrix

| Need | Usually start with | Why |
| --- | --- | --- |
| 모든/특정 path 작업에 계속 적용되는 rule | instruction / Rule | structural scope에 자동 적용 |
| task 의미에 따라 필요해지는 capability/knowledge/workflow | Skill | on-demand progressive context, parent capability composition |
| 사람이 명시적으로 실행하는 반복 task | prompt / command | 가장 작은 reusable invocation unit |
| deterministic action/check | tool / script / hook | LLM 판단을 불필요하게 쓰지 않음 |
| 다른 instructions + tools를 가진 지속 가능한 specialist role | custom agent | 명시적 role/config boundary |
| parent가 focused delegated work를 별도 context에서 시키고 result만 받을 필요 | subagent | context isolation + delegated execution |
| specialist가 conversation/user interaction ownership을 이어받음 | handoff | ownership transfer가 핵심 |
| fixed coordination / predictable sequence | workflow/code orchestration | deterministic control flow |

### 중요한 겹침

이 표는 배타적인 taxonomy가 아니다.

예를 들어 VS Code는 2026년에 Skill을 `context: fork`로 실행해 dedicated subagent에서 돌리는 experimental 기능도 제공한다. 즉 **Skill은 capability packaging이고 subagent는 execution mode**가 될 수 있다. GitHub Copilot에서도 custom agent가 Skill을 사용할 수 있고, custom agent 자체가 subagent로 실행될 수 있다.

따라서 자산을 “Skill vs Agent 중 하나”로만 분류하기보다 다음 두 질문을 분리하면 명확하다.

```text
What knowledge / behavior package is needed?
→ instruction / skill / prompt / tool / agent role

How should this task execute?
→ parent context / forked context / subagent / handoff / deterministic workflow
```

이 구분은 future runtime이 새로운 execution mode를 추가해도 semantic asset을 재사용하기 쉽다.

## 28. Lean-Prompt Challenge: 모든 문장이 있어야 하는가

### Finding

좋은 subagent asset을 만들다 보면 Scope, Authority, Guardrails, Workflow, Output, Failure, Tools를 모두 자세히 적고 싶어진다. 그러나 최신 capable model에서는 **중복된 defensive prose가 오히려 instruction bottleneck과 context noise를 만들 수 있다.**

OpenAI의 current model guidance는 prompt 중복을 줄이고 관련 tool surface만 노출하는 lean configuration을 최신 frontier model에서도 권장한다. 이는 “짧으면 무조건 좋다”는 뜻이 아니라, **각 instruction이 실제 material behavior를 소유해야 한다**는 방향이다.

### Compression test

Subagent body의 각 문장에 다음을 묻는다.

1. 이 문장이 없으면 실제 routing/behavior/authority/result failure가 생길 가능성이 있는가?
2. 상위 repository/project instruction이 이미 소유하는 내용인가?
3. tool/runtime permission으로 deterministic하게 강제되는 내용을 prose로 반복하는가?
4. specialist의 고유 책임인가, 모든 agent에 공통인 일반론인가?
5. 실제 failure/eval evidence 때문에 추가된 correction인가?

대답이 계속 “아니다”라면 제거하거나 더 자연스러운 owner로 옮기는 편이 좋다.

### Minimal sufficient anatomy

범용적인 참고 형태는 생각보다 작을 수 있다.

```markdown
---
name: <identity>
description: <what it specializes in + when it is a good candidate>
<target capability/config as needed>
---

# <Role>

<one-paragraph purpose / responsibility>

## Scope / Working Guidance

- <material boundaries or behavior only>
- <role-specific evidence / action guidance>

## Return

<what the parent needs back, when this is not obvious>
```

권한/금지사항/tool policy/result schema가 실제 역할이나 runtime에서 중요할 때만 확장한다. 섹션 이름과 이 layout 자체도 규격이 아니라 reference shape다.

### Description/body separation

가능하면:

- **description** → candidate routing에 필요한 의미
- **body** → 선택된 뒤의 execution behavior
- **frontmatter/tool config** → runtime capability/invocation projection
- **parent task packet** → 이번 invocation의 goal/target/context/output expectation

으로 책임을 나누면 같은 내용을 네 곳에 반복할 이유가 줄어든다.

## 29. Ideal Reusable Subagent Asset — Synthesis

30-loop research에서 반복적으로 살아남은 요소를 **필수 schema가 아니라 설계 관점**으로 정리한다.

### A. Identity and Routing

좋은 agent는 이름보다 `description`이 실제 역할 차이를 설명한다.

```text
Specializes in <bounded responsibility>.
Useful when <semantic situation>.
```

인접 agent와 반복적으로 혼동될 때만 negative cue/example을 늘린다.

### B. Responsibility

- bounded, meaningful, distinguishable
- parent와 중복되지 않음
- specialist끼리 서로 다른 lens/capability를 가짐
- task가 끝났다는 것을 판단할 수 있음

### C. Context

- parent entire history를 무조건 복사하지 않음
- invocation에 필요한 goal/target/constraints/source/output expectation은 전달
- noisy exploration은 child 안에서 소화
- parent에는 distilled result와 검증 가능한 evidence를 반환
- inherited instructions/tools/workspace semantics는 runtime-specific임을 인지

### D. Capability

- 역할과 tool surface가 일치
- read-only reviewer는 불필요한 mutation capability를 피함
- implementation worker는 필요한 edit/test capability를 실제로 가짐
- prompt text와 runtime authority를 혼동하지 않음

### E. Orchestration

- leaf specialist와 coordinator/final owner를 구분
- parallelism은 independent work에서 선택
- write-heavy parallelism은 ownership/isolation/reconciliation이 필요
- nested delegation은 capability가 있는 target에서만 의존

### F. Result

Parent가 다음 판단을 할 수 있게:

- answer/findings
- evidence/location
- uncertainty 또는 validation limits
- partial/blocker if relevant
- useful follow-up only

을 반환한다. Raw transcript를 결과로 삼지 않는다.

### G. Runtime Configuration

Portable role semantics와 다음을 가능한 한 분리한다.

- exact tool identifiers
- model/reasoning
- timeout/max turns
- invocation visibility/inference
- permission/sandbox
- MCP wiring
- concurrency/nesting

### H. Evaluation

- routing: positive / negative / near-miss
- behavior: task/scope/tool/evidence/non-action/failure
- orchestration: delegation/independence/reconciliation/trace
- target projection: schema/tool/config validity
- runtime: important case만 actual invocation
- noisy semantic result는 repeated evidence 후 regression gate로 승격

## 30. Final Adversarial Review and Repository Recommendation

마지막 loop에서는 앞선 결론을 일부러 공격했다.

### Challenge 1 — “좁은 역할이 항상 좋은가?”

아니다. 너무 잘게 쪼개면 routing ambiguity, fan-out, result reconciliation cost가 커진다. 핵심은 **좁음 자체가 아니라 distinguishable delegation boundary**다. 하나의 coherent responsibility라면 충분히 넓을 수 있다.

### Challenge 2 — “tool은 무조건 최소화해야 하나?”

아니다. 실제 task 수행에 필요한 tool을 빼면 agent가 불완전해진다. 핵심은 tool count가 아니라 **role-capability fit**이다.

### Challenge 3 — “별도 context가 항상 token을 아끼나?”

아니다. Main context pollution은 줄지만 전체 system token/inference는 더 커질 수 있다. Subagent는 context architecture와 parallelism을 위한 선택이지 자동 cost optimization이 아니다.

### Challenge 4 — “structured return을 모두 강제해야 하나?”

아니다. Automation이 field를 소비하거나 반복 omission이 나타날 때 가치가 크다. 최신 capable model과 human synthesis에서는 concise prose가 더 낮은 ceremony일 수 있다.

### Challenge 5 — “모든 agent에 explicit guardrail을 길게 써야 하나?”

아니다. Higher instruction/runtime/tool permission이 이미 소유하는 내용을 복사하면 drift와 noise가 늘어난다. Role-specific high-impact boundary만 asset에 남기는 편이 낫다.

### Challenge 6 — “현재 repo subagents를 지금 고쳐야 하나?”

현재 evidence로는 **아니다.**

`review-lead`, `review-quality`, `review-adversarial`은 이미 중요한 구조를 잘 갖고 있다.

- role/lens가 서로 구분됨
- lead와 leaf decision ownership이 분리됨
- quality/adversarial independence가 명시됨
- tool capability가 역할에 대체로 맞음
- source mutation/final decision authority가 specialist에 없음
- evidence/uncertainty limitation이 명시됨

이번 연구에서 나온 개선 아이디어 중 prompt text를 즉시 늘릴 만큼 검증된 defect는 발견하지 못했다.

### Highest-value next steps for this repository

우선순위는 **자산 rewrite보다 evidence 추가**다.

1. **Routing fixtures**
   - lead / quality / adversarial positive, negative, overlap case
2. **Orchestration eval**
   - lead가 두 reviewer를 독립 호출하고 결과를 reconcile하는지 actual target에서 관찰
3. **Non-action / capability eval**
   - specialists가 mutation/nested agent/final approval을 하지 않는지 확인
4. **Target projection validation**
   - Copilot/Antigravity generated tool identifiers와 invocation semantics가 현재 runtime과 맞는지 확인
5. **Failure propagation cases**
   - reviewer blocked/unknown이 lead final assessment에서 사라지지 않는지 확인

그 결과 반복 failure가 나오면 그때 description/body/tool mapping을 최소 delta로 고치는 편이 현재 repository의 KISS/DRY 방향과 맞다.

### Durable knowledge candidate

이 research가 반복 사용될 가치가 확인되면 `docs/references/patterns/`에 다음 성격의 reference capsule을 승격하는 것이 자연스럽다.

> **Subagent Asset Design** — specialist delegation boundary, context/capability/result separation, portable semantics와 runtime config의 구분을 설명하는 reference pattern.

다만 inbox 연구 결과를 곧바로 규칙이나 asset rewrite로 승격할 필요는 없다. 실제 subagent eval 결과와 함께 다시 review한 뒤 durable pattern으로 압축하는 것이 더 강한 근거를 갖는다.

## Final Ranking — What Matters Most

| Priority | Quality | Why |
| ---: | --- | --- |
| 1 | Distinguishable delegation responsibility | agent를 따로 둘 이유 자체 |
| 2 | Correct routing / invocation boundary | 좋은 body도 선택되지 않으면 무의미 |
| 3 | Context boundary + task packet | isolation benefit과 task fidelity를 동시에 결정 |
| 4 | Role-capability fit | 실제 수행 가능성, decision surface, blast radius |
| 5 | Distilled evidence-bearing return | parent integration 품질 결정 |
| 6 | Clear orchestration/final owner | duplicate judgment와 hidden failure 방지 |
| 7 | Portable semantics vs runtime config separation | multi-harness 유지보수성 |
| 8 | Behavior/orchestration eval evidence | prompt intuition 대신 regression feedback 제공 |
| 9 | Failure/unknown semantics | partial execution을 trustworthy하게 처리 |
| 10 | Lean human-readable instructions | context noise와 comprehension debt 억제 |

## Loop Ledger

| Loop | Question | Material delta |
| ---: | --- | --- |
| 26 | 언제 subagent를 쓰지 말아야 하는가? | instruction/Skill/prompt/tool/workflow/handoff/single-agent 대안을 task shape별로 분리했다. |
| 27 | 다른 asset과 무엇이 다른가? | behavior packaging과 execution mode를 두 축으로 나눈 asset-choice matrix를 도출했다. |
| 28 | 좋은 asset은 얼마나 써야 하는가? | lean-prompt compression test와 minimal sufficient anatomy를 만들었다. |
| 29 | 29개 loop에서 살아남은 공통 구조는? | routing/responsibility/context/capability/orchestration/result/runtime/eval 8축으로 최종 synthesis했다. |
| 30 | 앞선 원칙은 과도하지 않은가? 현재 repo를 바꿔야 하나? | 6개 반론으로 원칙을 완화하고, 현재 자산 rewrite보다 eval evidence가 우선이라는 최종 결론에 수렴했다. |

## Sources

- VS Code — Custom agents: https://code.visualstudio.com/docs/agent-customization/custom-agents
- VS Code — Agent Skills: https://code.visualstudio.com/docs/agent-customization/agent-skills
- VS Code — Prompt files: https://code.visualstudio.com/docs/agent-customization/prompt-files
- GitHub Copilot — Customization cheat sheet: https://docs.github.com/en/copilot/reference/customization-cheat-sheet
- GitHub Copilot — Agent skills: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- Anthropic — Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- OpenAI Agents SDK — Agent orchestration: https://openai.github.io/openai-agents-python/multi_agent/
- OpenAI latest model guidance: https://developers.openai.com/api/docs/guides/latest-model
