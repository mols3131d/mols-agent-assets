---
title: Agent Canonical Superset
description: 여러 custom-agent harness에 투영할 repository-local canonical Agent authoring spec
---

# Agent Canonical Superset

Agent Superset은 독립 role, authority와 runtime capability 요구사항을 target-independent하게 보존한다.

## Schema

```yaml
---
name: <kebab-case>
description: <string>

targets: [<target>]

capabilities:
  - <read|search|edit|execute|web|delegate|other>

authority:
  read: <boolean>
  write: <boolean>
  execute: <boolean>
  delegate: <boolean>

copilot:
  <copilot-only fields>

antigravity:
  <antigravity-only fields>
---

<agent body>
```

## Fields

| Field | Requirement | Contract |
| --- | --- | --- |
| `name` | Required | Agent identity. `kebab-case`. |
| `description` | Required | role, 책임과 사용 시점을 요약한다. |
| `targets` | Optional | 명시하면 지원 target을 제한한다. |
| `capabilities` | Required | Agent가 필요로 하는 abstract capability set. Vendor tool name을 직접 넣지 않는다. |
| `authority` | Required | 읽기/쓰기/실행/위임 권한의 canonical boundary. |
| `<target>` | Optional | model/tool/MCP/handoff 등 해당 harness에서만 필요한 runtime configuration. |
| body | Required | role, constraints와 행동 contract. |

## Capabilities

Canonical capability는 vendor tool identifier가 아니다.

- `read` — 파일/문서/데이터 조회
- `search` — 저장소나 외부 source 탐색
- `edit` — artifact 수정
- `execute` — command/script 실행
- `web` — 외부 웹 접근
- `delegate` — 다른 Agent/subagent 호출

Target projection은 이 capability를 실제 native tool 또는 permission으로 매핑한다.

## Authority

`capabilities`가 할 수 있는 기능을 표현한다면 `authority`는 **해도 되는 범위**를 표현한다.

```yaml
authority:
  read: true
  write: false
  execute: false
  delegate: true
```

Body의 자연어 guardrail과 metadata authority가 충돌하면 더 제한적인 쪽을 적용하고 spec을 수정한다.

## Target Extensions

```yaml
copilot:
  model: <model>
  tools: [<native-tool>]

antigravity:
  model: <model>
  tools: [<native-tool>]
  command-execution-policy: <mode>
```

Vendor-specific tool 이름과 runtime option은 공통 field로 승격하지 않는다.

## Body Contract

```markdown
# <Role>

## Responsibility
<이 Agent가 책임지는 결과>

## Constraints
<중요한 guardrail과 금지 사항>

## Procedure
<필요한 경우의 실행 절차>
```

Heading 이름은 고정 schema가 아니다. Role, responsibility와 authority boundary가 명확해야 한다.

## Minimal Example

```yaml
---
name: reviewer
description: Review changes for correctness without modifying source files.
capabilities: [read, search]
authority:
  read: true
  write: false
  execute: false
  delegate: false
---

# Reviewer

Review the requested change and report evidence-backed findings.
Do not modify source or repository state.
```

## Projection Requirements

- Role, `capabilities`, `authority`와 body semantics를 우선 보존한다.
- Native model/tool/MCP/handoff configuration은 target block과 projection이 소유한다.
- 핵심 capability 또는 authority boundary를 target에서 표현할 수 없으면 동일 Agent로 가장하지 않는다.

## References

- [GitHub Copilot custom agents](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents)
- [Google Antigravity IDE](https://codelabs.developers.google.com/getting-started-agy-ide)
