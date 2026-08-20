# Loops 11–15 — Portability and Runtime Divergence

## 11. “Separate Context” Is Not One Universal Semantic

### Finding

여러 vendor가 subagent의 핵심 이점으로 별도 context window를 말하지만, **무엇이 상속되는지**는 runtime마다 다르다.

VS Code는 현재 subagent가 main conversation history를 상속하지 않고 task prompt, applicable instruction files, current agent configuration을 받는다고 설명한다. Gemini CLI도 independent context loop를 강조한다. Antigravity는 parent conversation history 없이 clean slate에서 시작한다고 설명한다. 반면 workspace, project instructions, tools, model, runtime policy 등의 inheritance는 각 harness의 규칙을 따른다.

### Design consequence

Canonical asset에서 다음처럼 절대적으로 말하는 것은 피하는 편이 좋다.

- “parent context를 전혀 상속하지 않는다”
- “parent와 완전히 격리된다”
- “project instruction은 child에 적용되지 않는다”

대신 semantic expectation을 더 좁게 둔다.

> Subagent는 parent의 noisy working history와 분리된 focused execution context를 활용하는 것이 주된 목적이며, 실제 inherited instructions/tools/workspace는 target runtime이 결정한다.

### Verification implication

Portability가 중요하면 generated target별로 최소한 다음을 확인한다.

- conversation history inheritance
- project/root instruction inheritance
- tool inheritance/override
- model inheritance
- workspace/write isolation
- permission/approval inheritance

이것은 문서만 읽고 끝내기보다 실제 runtime smoke/eval로 확인할 가치가 큰 부분이다.

## 12. Invocation Policy Is a First-Class Dimension

### Finding

“agent가 존재한다”와 “누가 언제 호출할 수 있다”는 별개의 문제다.

VS Code의 current custom-agent surface는 다음을 분리한다.

- user dropdown에서 직접 선택 가능한가
- model이 subagent로 자동 호출 가능한가
- coordinator가 어떤 subagent를 allowlist로 호출할 수 있는가

GitHub Copilot SDK도 automatic inference를 끌 수 있는 agent 개념을 제공한다. Gemini CLI는 automatic delegation과 explicit forcing을 모두 지원한다. Antigravity는 `mainAgent`와 `subagent` 가능 여부를 별도 metadata로 둘 수 있다.

### Design consequence

Subagent asset에는 역할에 따라 다음 유형이 있을 수 있다.

```text
user-facing specialist
→ 사람이 직접 선택 + parent도 delegation 가능

internal specialist
→ UI에는 숨김 + coordinator가 delegation

explicit-only specialist
→ 자동 routing은 막고 사람이 의도적으로 호출

coordinator-only worker
→ 특정 lead의 allowlist 안에서만 사용
```

이 구분은 description wording만으로 흉내 내기보다 runtime이 invocation metadata를 지원하면 그 기능을 쓰는 편이 더 명확하다.

### Repository implication

현재 reusable subagent source가 여러 target을 생성하므로 “main agent로도 선택 가능해야 하는가 / subagent로만 써야 하는가”는 target-specific projection에서 의미가 달라질 수 있다. Semantic role에 필요한 경우에만 canonical metadata로 표현하고, 지원되지 않는 target에서는 graceful degradation이 필요하다.

## 13. Nested Delegation Is Not Portable Core

### Finding

2026-08 현재 agent nesting은 vendor divergence가 크다.

- Gemini CLI subagent는 recursion protection으로 다른 subagent를 호출하지 못한다.
- VS Code는 agent allowlist와 nested invocation 설정을 제공한다.
- Cursor는 nested subagents를 지원하며 SDK/제품에 따라 nesting depth semantics도 변해 왔다.
- Antigravity는 background subagent와 custom subagent orchestration을 지원하지만 구체적인 recursive capability는 runtime/version에 따라 검증이 필요하다.

즉 `A → B → C`가 특정 runtime에서 잘 된다는 사실만으로 reusable canonical agent가 B의 nested delegation을 필수 behavior로 요구하면 안 된다.

### Recommended default

- **leaf agent**: 다른 agent 호출에 의존하지 않는 편이 가장 portable하다.
- **coordinator/lead**: nested/child invocation이 역할의 본질이면 명시하되 target capability를 검증한다.
- 깊은 recursion보다 얕은 manager→specialist 구조가 portable baseline으로 다루기 쉽다.

이것은 recursion 자체를 금지하는 규칙이 아니다. 복잡한 hierarchy가 실제 이득을 주고 runtime이 지원하면 확장할 수 있다.

## 14. Separate Portable Semantics from Target Execution Config

### Finding

Vendor별 frontmatter/config는 공통점도 많지만 차이도 크다.

공통적으로 반복되는 의미:

- identity / name
- description / routing cue
- role instructions
- tools/capability
- model selection 또는 inheritance

더 target-specific한 의미:

- primary-agent visibility
- model auto-invocation policy
- subagent allowlist
- permission mode / command policy
- background/asynchronous execution
- workspace/worktree isolation
- MCP server schema
- nested delegation depth
- handoff UI
- turn/time limit

### Design model

```text
Portable semantic core
├─ role / purpose
├─ delegation description
├─ scope / responsibility
├─ expected result
└─ essential capability intent

Target execution projection
├─ tool identifiers
├─ model / reasoning
├─ invocation flags
├─ permission / sandbox
├─ MCP wiring
├─ nesting / concurrency
└─ vendor paths / schema
```

Rulesync 같은 source-of-truth layer의 가치는 이 경계를 다루는 데 있다. 하지만 source format에 필드를 넣었다고 모든 target에서 동일 semantic이 보장되는 것은 아니다. **Generated projection의 실제 behavior를 검증하는 단계가 여전히 필요하다.**

### Important distinction

Tool 이름 자체보다 capability intent가 오래 간다.

예:

```text
semantic intent: read-only repository inspection
Copilot tools: read + search + usages ...
Antigravity tools: view_file + grep_search ...
```

현재 repository의 `review-quality`와 `review-adversarial`이 target별 tool 목록을 따로 두는 방식은 이 관점과 잘 맞는다.

## 15. Scope, Discovery, Version Control, Drift

### Finding

대부분의 current harness는 project/repository-scoped agent와 user/global agent를 구분한다.

- VS Code/Copilot: workspace/project와 user/profile surface
- Gemini CLI: `.gemini/agents`와 user scope
- Cursor: project customization/plugin 등
- Antigravity: workspace agent와 global custom agent
- Codex: project `.codex/agents`와 user `~/.codex/agents`

Project agent는 팀과 함께 version control하기 좋고, user agent는 개인 workflow에 적합하다. 재사용 asset repository에서는 canonical source를 두고 target projection을 생성하는 방식이 이 둘 사이의 drift를 줄일 수 있다.

### Drift risks

1. Vendor frontmatter가 바뀌었는데 generator가 예전 schema를 계속 출력한다.
2. Tool alias가 target에서 더 이상 존재하지 않는다.
3. 지원하지 않는 field가 조용히 무시된다.
4. Invocation semantics가 버전 업그레이드로 변한다.
5. “동일한 Markdown”이 여러 runtime에서 다른 inheritance/permission behavior를 갖는다.

Rulesync upstream 자체도 여러 vendor target 변화를 따라가며 projection 지원을 갱신한다. 따라서 portable asset의 correctness는 **canonical file syntactic validity만으로 끝나지 않는다.**

### Recommended validation layers

```text
canonical source parse
→ generator / target projection
→ target schema / known tool names
→ routing smoke
→ behavior / permission smoke where important
```

모든 agent마다 모든 vendor를 실시간 E2E 테스트할 필요는 없다. 실제 지원 대상과 risk에 비례해 matrix를 좁히면 된다.

## Portability Matrix

| Concern | Portable semantic core? | Usually target/runtime config? |
| --- | --- | --- |
| name / identity | Yes | naming constraints may differ |
| delegation description | Yes | matching algorithm differs |
| responsibility | Yes | No |
| expected result | Yes | structured-output mechanism may differ |
| read/write intent | Yes | exact tools/permissions differ |
| tool identifiers | No | Yes |
| model ID | Usually no | Yes |
| reasoning effort | No | Yes |
| user-visible vs internal | Intent may be portable | exact flags differ |
| nesting | Role may require it | capability differs strongly |
| concurrency | No | orchestration/runtime |
| worktree/isolation | No | runtime |
| MCP schema | No | target config |
| timeout/max turns | Usually no | runtime/default/config |

## Loop Ledger

| Loop | Question | Material delta |
| ---: | --- | --- |
| 11 | separate context는 정확히 무엇을 의미하는가? | history isolation과 instruction/tool/workspace inheritance를 분리하고 runtime smoke 필요성을 추가했다. |
| 12 | 누가 agent를 호출할 수 있는가? | user-facing, internal, explicit-only, coordinator-only invocation policy를 독립 축으로 추가했다. |
| 13 | nested delegation을 core로 써도 되는가? | vendor divergence를 근거로 leaf portability baseline과 coordinator exception을 정리했다. |
| 14 | canonical asset과 vendor config를 어떻게 나눌까? | portable semantic core와 target execution projection 모델을 도출했다. |
| 15 | project/global scope와 drift를 어떻게 다룰까? | version-controlled source + generated projection + target smoke라는 validation chain을 추가했다. |

## Sources

- VS Code — Custom agents: https://code.visualstudio.com/docs/agent-customization/custom-agents
- VS Code — Subagents: https://code.visualstudio.com/docs/agents/run/subagents
- Gemini CLI — Subagents: https://geminicli.com/docs/core/subagents/
- Cursor — Subagents: https://cursor.com/changelog/2-4
- Cursor — SDK nested subagents: https://cursor.com/changelog/sdk-updates-jun-2026
- Google Antigravity — Subagents: https://antigravity.google/docs/subagents
- Rulesync repository / target matrix: https://github.com/dyoshikawa/rulesync
