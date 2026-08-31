# Durable Progress Handoff

Status: **promising candidate**

## Idea

Long-running work가 session, model, agent 또는 human boundary를 넘어갈 때 **다음 작업자가 반복 탐색 없이 이어갈 수 있는 최소한의 durable handoff surface**를 두는 것을 고려합니다.

핵심은 모든 작업 로그를 남기는 것이 아니라, 다음 실행에서 다시 알아내는 비용이 큰 상태와 판단만 남기는 것입니다.

## Useful Handoff Content

상황에 따라 다음이 특히 유용할 수 있습니다.

- 현재 목표와 완료된 범위
- 아직 남은 work item
- 현재 repository가 정상인지와 최소 verification 방법
- 중요한 decision과 이유
- 실패한 접근과 다시 시도하지 말아야 할 이유
- known limitation 또는 unresolved blocker
- 다음 작업자가 시작할 명확한 지점

## Why It May Be a Pattern

Long-running agent 작업에서는 context reset이나 session boundary 자체보다 **무엇을 durable하게 넘길 것인가**가 반복되는 문제입니다. Git history만으로 충분한 경우도 있지만, commit이 왜 그런 방향으로 갔는지 또는 어떤 접근이 실패했는지는 다시 조사해야 할 수 있습니다.

특히 실패한 접근을 남기는 것은 다음 agent가 같은 dead end를 반복하는 비용을 줄일 수 있습니다.

## Possible Surfaces

- active execution plan
- progress note / changelog
- structured task state
- PR description 또는 handoff comment
- repository-local feature status

어떤 surface를 쓰는지는 repository workflow에 따라 다릅니다. 새로운 progress file을 항상 만들 필요는 없습니다. 이미 PR, issue, plan 또는 task system이 필요한 정보를 durable하게 소유한다면 그것을 재사용하는 편이 단순합니다.

## What Not to Persist

다음은 보통 durable handoff의 가치가 낮을 수 있습니다.

- 쉽게 다시 계산하거나 검색할 수 있는 raw observation
- commit history와 동일한 변경 목록
- 이미 canonical document에 반영된 rule의 복제
- 매 session의 세세한 action log
- 현재 작업과 무관한 conversation transcript

## Limits

- progress artifact가 실제 state와 어긋나면 오히려 다음 작업자를 잘못된 방향으로 유도할 수 있습니다.
- 모든 판단을 기록하려 하면 documentation maintenance가 작업 자체보다 커질 수 있습니다.
- 여러 surface에 상태를 중복하면 어느 것이 최신인지 불명확해집니다.
- short-lived 작업은 handoff artifact 없이 Git/PR만으로 충분할 수 있습니다.

따라서 handoff surface는 **다음 실행의 재탐색 비용보다 유지비가 작은 경우**에만 충분한 정보를 남기는 쪽이 자연스럽습니다.

## Relationship to Existing Patterns

현재 `workflow/artifact-inbox.md`와 `docs/documentation/README.md`가 working artifact의 보존 위치와 durable knowledge의 기본 원칙을 다룹니다. 이 후보는 **무엇을 handoff content로 남기면 작업 연속성에 도움이 되는가**를 다룰 수 있지만, 기존 inbox/documentation 책임과 겹치지 않는지 엄격히 검토해야 합니다.

## Promotion Questions

- existing inbox/documentation principle에 흡수하는 편이 더 KISS하지 않은가?
- agent-specific memory workaround를 일반 workflow pattern으로 과도하게 일반화하고 있지 않은가?
- durable handoff의 최소 content를 특정 tool 없이 설명할 수 있는가?
- stale state에 대한 대응을 충분히 다룰 수 있는가?

## Research Notes

- Anthropic의 long-running scientific computing 사례는 progress file에 current status, completed work, failed approaches와 known limitations를 남겨 session 사이의 portable memory로 사용합니다.
- Anthropic의 long-running coding harness도 session 시작 시 progress note와 git history를 읽고 종료 시 progress를 갱신하는 구조를 사용합니다.
- OpenAI의 agent-first repository는 complex work의 execution plan과 progress/decision log를 repository-local durable artifact로 다룹니다.
