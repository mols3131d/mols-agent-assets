---
title: Agent Canonical Superset
description: 여러 custom-agent harness에 투영할 Agent의 repository-local canonical superset 기준
---

# Agent Canonical Superset

여러 custom-agent harness에 같은 Agent를 배포할 때의 권장 Superset은 **role/instructions core와 target-scoped runtime capabilities를 함께 보존하는 `<name>.agent.md` source model**이다.

하나의 target-native schema를 모든 harness의 공통분모로 삼지 않는다. Agent의 role과 authority는 공통 core로 유지하고, tool/model/delegation/runtime capability 차이는 canonical source에서 target-scoped semantics로 명시한다.

```text
<name>.agent.md Superset
├─ role / responsibility
├─ authority / guardrails
├─ shared instructions
├─ target A runtime semantics
└─ target B runtime semantics
        ↓
   target-native custom agents
```

## Superset Owns

- Agent의 role과 responsibility boundary
- 허용/금지 authority와 mutation boundary
- shared behavioral instructions와 output responsibility
- 필요한 tool capability와 model requirement
- delegation/subagent/handoff semantics
- target별 runtime capability 차이와 unsupported behavior

Front matter는 실행 capability를 표현하는 surface이고 Markdown body는 role, instructions, authority와 guardrail의 중심이다.

## Target-Scoped Runtime Surface

현재 repository validator는 VS Code와 GitHub Copilot cloud custom agent가 동일한 field 집합을 지원하지 않는다는 사실을 명시적으로 구분한다.

공통 또는 조건부 surface에는 `name`, `description`, `tools`, `model`, invocation control 등이 있고, VS Code 쪽에는 `argument-hint`, `agents`, `handoffs`, `hooks`, GitHub cloud 쪽에는 `mcp-servers`, `metadata` 같은 target-specific capability가 존재한다.

따라서 Superset은 이 차이를 삭제하지 않고 보존하되, target projection은 해당 harness가 실제로 지원하는 field만 출력한다.

## Projection

```text
Agent Superset
├─ VS Code custom agent
├─ GitHub Copilot cloud custom agent
└─ other target-native agent
```

Projection은 다음을 검증한다.

- role과 authority boundary가 유지되는가
- 필요한 tool capability가 target에서 실제 제공되는가
- delegation/handoff가 native, approximated, unsupported 중 무엇인가
- model 또는 permission 차이가 Agent의 책임을 바꾸는가
- target-only extension이 shared Agent 의미를 조용히 변경하지 않는가

지원되지 않는 tool이나 delegation을 단순히 삭제해서 동일 Agent라고 주장하지 않는다. 핵심 capability를 보존할 수 없으면 compatibility gap 또는 별도 target specialization으로 다룬다.

## Source Placement

이 저장소의 reusable Agent source는 `src/agents/<name>.agent.md`에 둔다. 현재 `target` metadata가 명시된 source는 해당 native target에 최적화된 authority일 수 있으며, 다른 target으로 옮기는 작업만으로 generic ownership으로 승격하지 않는다.

## Boundary

- 이 문서는 Agent 유형의 **최적 canonical Superset**을 소유한다.
- Superset은 모든 vendor field를 무조건 한 runnable file에 섞으라는 뜻이 아니다.
- target adapters가 필요한 경우 canonical semantics와 native projection을 분리한다.
- Agent의 본질적 authority/tool/delegation 차이를 Prompt나 Rule 차이로 축소하지 않는다.
- target harness의 실제 runtime contract와 platform authority가 이 repository convention보다 우선한다.
