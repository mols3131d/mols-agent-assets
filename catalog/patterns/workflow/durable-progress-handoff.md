---
description: 긴 작업이 session·agent·human 경계를 넘어갈 때 재탐색 비용을 줄이도록 resume-critical state를 durable artifact에 남기고 다시 이어가는 방식을 소개하는 패턴입니다.
---

# Durable Progress Handoff

긴 작업은 하나의 conversation이나 agent session 안에서 끝나지 않을 수 있습니다. Context가 초기화되거나 작업 주체가 바뀌면, 다음 작업자는 이미 끝난 조사와 판단을 다시 반복하거나 현재 상태를 잘못 추측하기 쉽습니다.

이때 **다시 알아내는 비용이 큰 작업 상태를 transient context 밖의 durable surface에 남겨, 다음 실행이 빠르게 현재 상태를 복구하고 이어갈 수 있게 하는 것**을 고려할 수 있습니다.

여기서 `durable`은 영구 보존이나 canonical documentation을 뜻하지 않습니다. **예상하는 handoff boundary를 지난 뒤에도 필요한 상태를 다시 찾을 수 있을 만큼 지속되는 것**을 뜻합니다. 같은 workspace의 context reset만 넘기면 되는 artifact도 있고, 다른 사람·agent·machine까지 이어야 해서 repository나 project system에 남겨야 하는 artifact도 있을 수 있습니다.

## Core

핵심은 모든 작업 기록을 남기는 것이 아니라 **minimum sufficient resumption state**를 남기는 것입니다.

```text
진행 중인 작업
    ↓
다시 알아내기 비싼 상태를 선택
    ↓
예상 handoff boundary를 버틸 surface에 기록
    ↓
context / session / worker 전환
    ↓
현재 source와 state에 맞는지 다시 확인
    ↓
명확한 다음 지점에서 작업 재개
```

좋은 handoff는 과거를 완전히 재현하지 않습니다. 다음 작업자가 다음 세 질문에 빠르게 답할 수 있게 합니다.

- 지금 무엇을 하고 있는가?
- 지금까지 무엇을 알았고 어디까지 왔는가?
- 무엇을 확인한 뒤 어디서 다시 시작하면 되는가?

Handoff의 상대는 반드시 다른 agent일 필요도 없습니다. 같은 agent가 context reset 뒤 돌아오는 경우, 다른 session이나 model이 이어받는 경우, 사람이 작업을 인계받는 경우에도 같은 문제가 생길 수 있습니다.

## 언제 유용한지

다음 조건이 많이 겹칠수록 durable handoff의 가치가 커질 수 있습니다.

- 작업이 여러 session이나 context window를 넘길 가능성이 큽니다.
- 다른 agent나 사람이 이어받을 수 있습니다.
- 조사 결과나 결정 이유를 다시 복구하는 비용이 큽니다.
- 코드와 Git diff만으로는 현재 의도나 남은 작업을 쉽게 알기 어렵습니다.
- 실패한 접근을 다음 실행이 다시 시도할 가능성이 큽니다.
- 현재 known-good / known-broken 상태와 verification 방법이 continuation에 중요합니다.

반대로 짧은 작업이거나 현재 상태를 source, Git history, issue와 canonical documentation에서 쉽게 재구성할 수 있다면 별도 handoff artifact를 만들지 않는 편이 더 단순할 수 있습니다.

## 무엇을 남길지

다음은 handoff content로 가치가 높은 대표적인 상태입니다. 모두 필요하다는 뜻은 아닙니다.

| State | 남기는 이유 |
| --- | --- |
| 현재 목표와 scope | 다음 작업자가 다른 문제를 풀기 시작하지 않게 함 |
| 완료·진행·남은 범위 | 이미 끝난 일을 반복하거나 미완료를 완료로 오인하지 않게 함 |
| 중요한 decision과 rationale | source만 보고 다시 같은 설계 논쟁을 반복하는 비용을 줄임 |
| validation과 current health | 현재 known-good / known-broken 상태와 확인 방법을 복구함 |
| 실패한 접근과 이유 | 같은 dead end를 반복하지 않게 함 |
| blocker와 residual uncertainty | 아직 사실로 확정되지 않은 것을 명확히 남김 |
| 다음 시작점 | 다음 실행이 탐색보다 실제 작업으로 빠르게 진입하게 함 |
| 관련 source와 artifact reference | canonical 내용이나 큰 evidence를 복제하지 않고 찾아갈 수 있게 함 |

특히 **실패한 접근의 이유**는 Git history나 최종 source에서 사라지기 쉽습니다. 재시도 비용이 크다면 짧게 남길 가치가 있습니다.

반대로 다음 내용은 보통 handoff의 핵심이 아닙니다.

- 매 command와 tool call의 전체 실행 로그
- conversation transcript 전체
- Git diff나 commit history를 그대로 옮긴 변경 목록
- canonical documentation에 이미 있는 규칙의 복제
- 쉽게 다시 계산하거나 검색할 수 있는 raw observation
- continuation에 필요하지 않은 장황한 배경 설명

Handoff는 **history archive가 아니라 resumption surface**에 가깝습니다.

## 기대하는 Boundary에 맞는 Surface를 선택합니다

하나의 정해진 파일이나 directory가 필요한 것은 아닙니다. 이미 필요한 상태를 소유하는 surface가 있다면 그것을 재사용하는 편이 단순합니다.

대표적인 형태는 다음과 같습니다.

- 기존 issue, task 또는 PR description의 progress section
- active plan이나 execution plan
- 짧은 progress / handoff note
- research, plan, change, review처럼 역할이 나뉜 여러 working artifact
- workflow나 task system의 structured state

중요한 것은 artifact 개수가 아니라 **예상하는 handoff boundary 뒤에도 필요한 상태를 찾을 수 있는가**입니다.

예를 들어 같은 workspace 안에서 context만 초기화된다면 local working artifact로 충분할 수 있습니다. 다른 machine이나 collaborator까지 이어야 한다면 shared project surface가 더 적합할 수 있습니다. 반대로 repository에 commit된 문서가 필요하지 않은 작업에 영구 파일을 추가할 이유는 없습니다.

여러 artifact를 사용하는 경우에는 서로의 관계를 다시 추측하지 않도록 stable task name, link, heading 또는 다른 가벼운 identity cue로 lineage를 연결할 수 있습니다. 그렇다고 모든 작업에 별도 ID schema나 artifact registry를 만들 필요는 없습니다.

## Handoff는 기록과 재개를 함께 봅니다

Durable artifact를 썼다는 사실만으로 continuation이 안전해지는 것은 아닙니다. Handoff는 **상태를 남기는 쪽과 다시 읽는 쪽이 함께** 성립할 때 유용합니다.

### 상태를 남길 때

- 현재 상태를 사실대로 갱신하고 완료되지 않은 일을 완료로 표시하지 않습니다.
- 다음 작업의 판단을 바꾸는 material delta를 우선 남깁니다.
- canonical source가 있는 내용은 복제하기보다 reference합니다.
- 여러 artifact가 있다면 어느 것이 현재 상태인지 알아볼 수 있게 합니다.
- 작업이 멈춘 이유와 다음 시작점이 중요하다면 명시합니다.

### 다시 시작할 때

Handoff artifact를 곧바로 현재 truth로 가정하지 않습니다. 먼저 source, Git state, canonical documentation이나 필요한 runtime 상태와 비교해 **artifact가 아직 현재 상태를 설명하는지** 확인합니다.

현재 health가 continuation에 중요하다면 가장 작은 유효한 verification을 다시 실행할 수도 있습니다. 예를 들어 이전 handoff가 `tests passing`이라고 적고 있어도 이후 branch가 움직였거나 environment가 달라졌다면 그 문장만 믿고 계속하지 않습니다.

Handoff는 다음 작업자의 탐색을 줄이는 **evidence와 navigation surface**이지, 현재 repository state보다 높은 authority가 아닙니다.

## Artifact-rich와 Compact Handoff는 둘 다 가능합니다

작업이 복잡할수록 research, plan, implementation evidence, review를 분리한 여러 artifact가 유용할 수 있습니다. 반대로 하나의 progress note와 Git history만으로 충분한 경우도 있습니다.

```text
Compact
Git / PR + 짧은 progress state
        ↓
progress note + active plan
        ↓
research + plan + change evidence + review
Artifact-rich
```

이것은 maturity ladder나 반드시 거쳐야 하는 단계가 아닙니다. **continuation cost를 충분히 낮추는 가장 작은 형태**를 선택합니다.

RPI workflow를 사용한다면 Research, Plan, Review 같은 기존 artifact가 이미 handoff state의 상당 부분을 소유할 수 있습니다. 이 경우 같은 내용을 별도 `handoff.md`에 다시 복제하기보다 기존 artifact를 continuation surface로 재사용할 수 있습니다.

## 비용과 수명

Handoff artifact도 유지비가 있습니다. 작업 상태가 자주 바뀌는데 artifact를 계속 동기화해야 한다면 기록 비용이 continuation에서 절약하는 비용보다 커질 수 있습니다.

따라서 모든 작은 변화마다 기록하기보다 **다음 실행의 판단이나 시작점을 바꾸는 material state가 달라졌을 때** 갱신하는 편이 자연스럽습니다.

작업이 끝난 뒤 artifact를 어떻게 처리할지도 별도 문제입니다. 현재와 미래의 판단을 계속 바꾸는 durable knowledge가 생겼다면 적절한 canonical owner로 승격할 수 있고, 단순한 working state라면 repository의 artifact lifecycle에 따라 유지·archive·삭제할 수 있습니다.

## Limits and Responses

### Handoff가 stale하면 오히려 재개를 방해할 수 있습니다

오래된 progress나 plan이 현재 source와 다르면 다음 작업자가 잘못된 상태에서 시작할 수 있습니다.

**대응:** handoff를 현재 truth가 아니라 resume candidate로 취급하고, continuation 전에 중요한 state와 verification을 현재 source에 맞춰 확인합니다. Material change가 생기면 같은 내용을 여러 곳에 복제하기보다 현재 owner를 갱신합니다.

### Artifact가 많아지면 새로운 탐색 문제가 생길 수 있습니다

Research, plan, note, review, task state가 계속 늘어나면 어느 것이 최신인지 찾는 일 자체가 새로운 비용이 됩니다.

**대응:** 기존 surface를 우선 재사용하고, 하나의 작업에 필요한 artifact만 둡니다. 여러 artifact가 실제로 필요할 때만 가벼운 lineage를 두고, artifact framework나 registry를 선제적으로 만들지 않습니다.

### 기록된 결정이 잘못된 가정을 오래 살릴 수 있습니다

Durable하다는 이유로 이전 판단이 더 옳아지는 것은 아닙니다. 잘못된 assumption도 잘 정리된 handoff를 통해 그대로 전달될 수 있습니다.

**대응:** decision과 evidence를 구분하고 residual uncertainty를 숨기지 않습니다. 현재 source나 새 evidence와 충돌하면 handoff를 수정하거나 폐기합니다.

### Canonical knowledge와 working state가 섞일 수 있습니다

Handoff에 project rule이나 architecture truth를 복제하면 시간이 지나며 canonical source와 다른 두 번째 authority가 생길 수 있습니다.

**대응:** handoff에는 현재 작업에 필요한 state와 reference를 남기고, 장기적으로 유효한 knowledge는 해당 canonical owner가 소유하게 합니다.

### 기록 자체가 작업보다 커질 수 있습니다

작은 작업까지 세세하게 기록하면 artifact maintenance가 실제 implementation보다 비싸질 수 있습니다.

**대응:** handoff probability, 재탐색 비용과 작업 규모에 비례해 기록합니다. Source와 Git만으로 충분하면 별도 artifact를 만들지 않습니다.

### 민감한 context가 불필요하게 지속될 수 있습니다

Conversation에만 있던 credential, 개인 정보나 민감한 운영 세부사항을 그대로 durable artifact에 복사하면 보존 범위가 불필요하게 넓어질 수 있습니다.

**대응:** continuation에 필요한 최소 정보만 남기고, 해당 workspace와 repository의 security·privacy policy보다 넓게 보존하지 않습니다.

## Boundary

이 패턴은 **작업 연속성을 위해 어떤 state를 transient context 밖에 남기고 어떻게 다시 이어갈지**를 다룹니다.

- [`Artifact Inbox`](artifact-inbox.md)는 working / non-canonical artifact를 canonical surface와 분리해 둘 저장 위치와 scope를 다룹니다.
- Repository의 knowledge lifecycle은 working artifact를 언제 canonical owner로 승격·유지·archive·삭제할지 다룹니다.
- RPI 같은 workflow method는 Research, Plan, Implementation, Review의 단계와 prerequisite 관계를 다룹니다.
- Git history는 repository가 어떻게 변했는지를 보존하지만, 그 자체가 모든 decision rationale이나 next action을 설명해야 하는 것은 아닙니다.

따라서 이 패턴은 특정 `inbox/`, `.tracking/`, plan filename, task ID, commit policy나 agent framework를 요구하지 않습니다.

## Grounding

- [Microsoft HVE Core, *Understanding the RPI Workflow*](https://github.com/microsoft/hve-core/blob/main/docs/rpi/README.md)는 research, plan, phase details, implementation changes와 review를 durable working artifact로 연결하고 stable task identity를 통해 단계 사이의 state를 이어가는 사례를 보여줍니다.
- [Microsoft HVE Core, *Context Engineering*](https://github.com/microsoft/hve-core/blob/main/docs/rpi/context-engineering.md)은 context reset 뒤 chat history 대신 `.copilot-tracking/` artifact를 다시 참조해 작업을 재개하는 방식을 설명합니다. 이 artifact는 gitignored일 수 있으므로 durable working state가 반드시 canonical 또는 repository-tracked일 필요는 없다는 사례이기도 합니다.
- [Anthropic, *Effective harnesses for long-running agents*](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)는 progress file과 Git history를 함께 사용해 새로운 session이 최근 작업과 다음 할 일을 빠르게 복구하는 사례를 설명합니다.
- [Anthropic, *Long-running Claude for scientific computing*](https://www.anthropic.com/research/long-running-Claude)는 current status, completed work, failed approaches, key checkpoints와 known limitations를 progress file에 남겨 portable long-term memory로 사용하는 사례를 보여줍니다.
- [OpenAI, *Harness engineering: leveraging Codex in an agent-first world*](https://openai.com/index/harness-engineering/)는 복잡한 execution plan에 progress와 decision log를 포함해 repository-local versioned artifact로 관리하는 사례를 소개합니다.

이 사례들은 artifact의 개수나 저장 경로에서는 서로 다르지만, **긴 작업의 중요한 상태를 transient model context에만 두지 않는다**는 공통점을 보여줍니다.

## Short Form

> **긴 작업에서 다시 알아내는 비용이 큰 목표·진행·결정·검증·실패·다음 시작점을 예상 handoff boundary를 버틸 최소한의 durable surface에 남깁니다. 재개할 때는 그 artifact를 현재 truth로 맹신하지 않고 source와 state에 맞는지 확인한 뒤 이어갑니다.**
