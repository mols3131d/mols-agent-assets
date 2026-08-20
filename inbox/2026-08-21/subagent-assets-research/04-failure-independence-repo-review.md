# Loops 16–20 — Failure, Independent Critique, Current Repository Review

## 16. Failure and Partial Results Are Part of the Contract

### Finding

Subagent는 성공 결과만 반환하는 함수가 아니다. 별도 context, tool, timeout, permission, retrieval 경계를 가지므로 partial result와 blocker가 정상적인 runtime outcome이다.

VS Code는 subagent invocation을 stateless하게 다루며 parent가 follow-up을 같은 child에 보낼 수 없는 surface가 있다. GitHub의 built-in `task` agent는 성공 시 짧은 요약, 실패 시 더 많은 failure output을 반환하는 식으로 결과 밀도를 다르게 한다. Anthropic의 orchestrator-worker 연구도 worker가 충분한 결과를 얻은 뒤 불필요하게 계속하거나 잘못된 tool을 쓰는 failure mode를 관찰했다.

### Design consequence

좋은 subagent result는 최소한 다음 상태를 표현할 수 있으면 parent가 안전하게 이어가기 쉽다.

```text
completed
→ requested result + evidence

partial
→ 얻은 것 + 남은 gap + 왜 못 닫았는지

blocked
→ blocker + 필요한 authority/context/capability

not_applicable
→ 왜 이 agent의 책임 범위가 아닌지
```

모든 agent에 enum schema를 강제할 필요는 없다. 중요한 것은 failure를 성공처럼 포장하지 않고 parent가 retry, fallback, re-route, stop을 결정할 정보를 돌려주는 것이다.

### Anti-pattern

- 실패한 child를 coordinator가 조용히 누락
- “찾지 못함”을 “없음”으로 승격
- 실행하지 못한 validation을 pass로 간주
- child가 scope 밖 문제를 스스로 확장하여 해결

현재 repository의 review agents가 uncertainty와 수행하지 않은 검증을 구분하도록 한 것은 이 원칙과 잘 맞는다.

## 17. Independence Is Useful When the Perspectives Are Actually Different

### Finding

여러 reviewer를 쓰는 목적은 같은 분석을 두 번 하는 것이 아니라 **correlated blind spot을 낮추는 것**이다.

VS Code는 correctness/security/accessibility처럼 서로 다른 perspective를 병렬 subagent로 분리하는 예를 제공한다. GitHub Copilot의 `rubber-duck` agent는 의도적으로 main session과 다른 model family를 critic에 사용해 single-model blind spot을 줄이려 한다.

### Design consequence

Independent review가 가치 있으려면 최소 하나 이상이 실제로 달라야 한다.

- review objective / lens
- prompt / instructions
- evidence method
- model family or reasoning profile
- source/context subset

단지 agent 이름만 다르고 같은 prompt, same context, same objective라면 redundancy cost에 비해 diversity gain이 작을 수 있다.

### Independence hygiene

Critic/reviewer가 다른 reviewer의 결론을 먼저 보면 anchoring이 생길 수 있다. 따라서 independent pass가 목적이라면:

1. 동일한 base target과 constraints는 공유한다.
2. 서로의 findings는 초기 분석 전에 공유하지 않는다.
3. coordinator가 나중에 충돌과 중복을 reconcile한다.

현재 `review-lead`가 quality/adversarial의 독립 분석을 유지하도록 한 설계는 이 점에서 강하다.

## 18. Deep Review — `review-lead`

현재 source: `src/rulesync/.rulesync/subagents/review-lead.md`

### Strong design choices

**Clear orchestration ownership**

- review process와 final assessment를 lead가 소유한다.
- quality/adversarial 두 specialist를 호출하는 이유와 관계가 분명하다.
- specialist가 final merge/approval judgment를 가지지 않는다.

**Independent fan-out, central reconciliation**

- 두 reviewer에게 같은 target/intent/constraint/relevant context를 제공한다.
- 서로의 conclusion을 기준점으로 주지 않는다.
- lead는 세 번째 full review를 하지 않고 evidence validation, conflict resolution, synthesis에 집중한다.

이 구조는 manager-as-tools/orchestrator-workers pattern과 잘 맞으며 context duplication도 비교적 통제한다.

**Authority boundary**

- final review document 외 source/test/config/repository state를 수정하지 않는다.
- commit/push/merge/approve/dismiss를 배제한다.
- delegated result와 automation을 conclusive proof로 취급하지 않는다.

### Improvement hypotheses — not yet findings

1. **Routing description**
   - 현재 description은 역할을 정확하게 말한다.
   - automatic routing에서 “언제 이 lead를 고르고 단일 reviewer는 언제 고르지 않는가”가 실제 near-miss를 만드는지 eval할 가치가 있다.
   - 실제 misrouting evidence가 없으므로 지금 문장을 늘릴 근거는 부족하다.

2. **Result shape**
   - final assessment를 쓴다는 것은 분명하지만 최소 result structure가 없다.
   - downstream에서 finding location/evidence/severity/status를 안정적으로 소비해야 할 필요가 생기면 lightweight output guidance가 가치 있을 수 있다.
   - 현재 human-readable review가 목적이라면 schema를 추가하는 것은 ceremony일 수 있다.

3. **Always-two-reviewers policy**
   - 일반론으로는 작은 change에서 dual review가 비쌀 수 있다.
   - 하지만 이 asset의 정체성이 “independent quality + adversarial review coordinator”라면 둘 다 호출하는 것이 오히려 핵심 behavior다.
   - 따라서 cost 이유만으로 약화할 finding은 아니다.

### Assessment

현재 evidence 기준으로 구조적 재설계 필요 없음. 가장 가치 있는 다음 단계는 prompt expansion보다 **routing + orchestration eval**이다.

## 19. Deep Review — `review-quality` and `review-adversarial`

### `review-quality`

강점:

- intended behavior, correctness, regression, maintainability, validation이라는 coherent lens
- source mutation과 nested agent invocation 없음
- smallest relevant validation을 실행하도록 하되 dependency install/autofix/shared external access를 무단 수행하지 않음
- focused test에서 full-suite pass를 추론하지 않음
- adversarial reviewer 역할을 모방하지 말라는 explicit separation

관찰:

- tool surface가 Antigravity에서는 `run_command`, read/search 위주이고 Copilot에서는 test/read/search 계열이라 semantic capability와 target tool mapping이 대체로 맞는다.
- “validation 실행 가능성”이 역할의 일부이므로 완전 read-only critic보다 capability가 넓은 이유가 설명 가능하다.

### `review-adversarial`

강점:

- reachable failure / unsafe boundary / recovery / trust boundary라는 명확한 lens
- speculative scenario를 confirmed defect로 승격하지 않음
- 기존 guard가 hypothesis를 무효화하는지 먼저 확인
- file mutation, nested agent invocation, final decision 없음

관찰:

- read/search-only capability가 역할과 잘 맞는다.
- quality reviewer와 overlapping “general review”가 아니라 실패 경로 탐색에 집중한다.

### Improvement hypotheses

**Return protocol**

두 specialist 모두 “간결하고 독립 검증 가능한 finding”을 요구하지만 exact shape는 자유롭다. 최신 capable model 기준으로 이는 충분할 가능성이 높다. Structured return은 다음 경우에만 추가할 가치가 크다.

- lead reconciliation에서 반복적으로 field 누락이 발생함
- automated eval/grader가 stable fields를 필요로 함
- target runtime이 structured output을 직접 지원함

**Description routing**

둘의 description은 서로 잘 구별된다. keyword를 늘리는 것보다 positive/negative routing fixture로 실제 separation을 검증하는 편이 낫다.

## 20. Anti-pattern Stress Test

앞의 원칙을 뒤집어 좋은 subagent asset을 망가뜨리는 패턴을 검토했다.

### A. Role cosplay

```text
You are an elite world-class principal engineer.
Be meticulous, thoughtful, creative, comprehensive...
```

문제: task boundary, routing, capability, result가 없다. Persona가 필요한 tone/domain expertise를 줄 수는 있지만 delegation contract를 대신하지 못한다.

### B. Duplicate parent

```text
Use all tools. Research, plan, code, test, review, merge, and report.
```

문제: 별도 agent가 되는 structural reason이 context isolation 외에는 거의 없다. General-purpose child가 필요한 경우도 있지만 reusable specialist asset으로서는 distinction이 약하다.

### C. Prompt-only permission

```text
You are authorized to edit/delete/deploy anything needed.
```

문제: asset text가 user/runtime authority를 mint한다고 오해한다.

### D. Blind inheritance

Tool/model/project history를 전부 상속한다고 가정한다. Target runtime에 따라 사실이 아니며 hidden coupling이 된다.

### E. Over-specified micro-procedure

Capable model이 task evidence를 보고 판단할 수 있는 부분까지 30단계 workflow로 고정한다. Instruction bottleneck과 maintenance debt가 커진다.

### F. Under-specified delegation

Parent가 reusable asset을 믿고 `investigate this`만 던진다. Objective, target, boundary, expected output이 없으면 specialist도 task를 잘못 해석할 수 있다.

### G. Unlimited fan-out

모든 child가 모든 child를 자유롭게 호출하고 동일 work를 중복한다. Token/latency가 폭증하고 final ownership이 흐려진다.

### H. Raw result flooding

Subagent를 context isolation 목적으로 썼는데 raw logs/search hits/transcript를 parent에 다시 복사한다.

### I. Same critic N times

같은 prompt/model/context로 reviewer 수만 늘린다. 일부 ensemble benefit은 있을 수 있지만 “독립 perspective”라고 부르기는 어렵다.

### J. Framework-driven agent proliferation

Runtime이 subagent 기능을 지원한다는 이유로 Skill/tool/prompt로 충분한 capability까지 별도 agent로 만든다.

## Loop Ledger

| Loop | Question | Material delta |
| ---: | --- | --- |
| 16 | child가 실패하거나 일부만 끝냈을 때? | completed/partial/blocked/not-applicable의 semantic result 상태와 parent fallback 책임을 추가했다. |
| 17 | independent reviewer가 왜 필요한가? | duplicate pass가 아니라 objective/context/model diversity와 anchoring 방지가 핵심임을 정리했다. |
| 18 | 현재 review-lead는 좋은가? | 구조적 강점을 확인하고 routing/result-shape는 eval 전에는 hypothesis로 유지했다. |
| 19 | 현재 두 specialist는 좋은가? | lens/tool/authority 분리가 적절함을 확인하고 schema 추가는 evidence-gated로 남겼다. |
| 20 | 원칙을 뒤집으면 어떤 anti-pattern이 생기나? | role cosplay부터 framework-driven proliferation까지 10개 failure pattern으로 stress-test했다. |

## Sources

- VS Code — Subagents: https://code.visualstudio.com/docs/agents/run/subagents
- VS Code — Agents concepts: https://code.visualstudio.com/docs/agents/concepts/agents
- GitHub Copilot — About custom agents: https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents
- GitHub Copilot — Rubber duck agent: https://docs.github.com/en/copilot/concepts/agents/copilot-cli/rubber-duck
- Anthropic — Multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
