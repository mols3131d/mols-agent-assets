---
title: Agent Canonical Superset
description: Rulesync Subagent format을 사용하는 repository-local canonical Agent spec
---

# Agent Canonical Superset

Canonical Agent는 **`.rulesync/subagents/<name>.md`** 로 작성한다.

Rulesync에서는 cross-target custom Agent surface를 `subagents`라고 부른다. 이 문서의 Agent는 repository taxonomy의 **독립 role + authority + tools/delegation boundary**와 대응한다.

## Schema

```yaml
---
name: <string>
description: <string>
targets: ["*"]

claudecode:
  model: <model|inherit>
  tools: [<tool>]
  disallowedTools: [<tool>]
  permissionMode: <default|acceptEdits|bypassPermissions|plan>
  maxTurns: <integer>
  skills: [<skill>]
  memory: <user|project|local>
  effort: <low|medium|high|xhigh|max>
  isolation: <worktree>
  background: <boolean>
  initialPrompt: <string>
  mcpServers: <mapping>
  hooks: <mapping>

copilot:
  tools: [<tool>]

antigravity-ide:
  tools: [<tool>]
  mainAgent: <boolean>
  subagent: <boolean>
  model: <inherit|flash|pro>
  commandExecutionPolicy: <off|auto|eager|sandbox>
  mcpServers: <mapping-or-list>
  skills: [<skill>]
  plugins: [<plugin>]

opencode:
  mode: <subagent|...>
  model: <model>
  temperature: <number>
  tools: <mapping>
  permission: <mapping>

# 기타 target-specific block 허용
<target>: <mapping>
---

<agent system prompt / instructions>
```

## Fields

| Field | Requirement | Meaning |
| --- | --- | --- |
| `name` | **Required** | Agent identity |
| `description` | **Required** | role + 언제/왜 사용할지 |
| `targets` | **Required** | `"*"` 또는 Rulesync target 목록 |
| `<target>` | Optional | model/tool/permission/delegation 등 native runtime contract |
| body | **Required** | role, authority, workflow, guardrails를 담는 system-prompt body |

## Body Contract

Body는 최소한 다음 semantic contract를 표현한다.

```markdown
# <Agent Role>

## Responsibility
<이 Agent가 책임지는 결과>

## Authority
<허용된 읽기/쓰기/변경 범위>

## Constraints
<금지 사항과 중요한 guardrail>

## Procedure
<필요할 때만 실행 절차>
```

Heading 이름 자체는 고정 schema가 아니다. **role / authority / constraints가 모호하지 않은 것**이 요구사항이다.

## Repository Constraints

1. Role과 behavioral authority는 body가 canonical authority다.
1. Model/tool/permission/delegation은 harness마다 의미가 다르므로 **공통분모로 축소하지 않고 target block에 둔다.**
1. 동일한 runtime setting이 여러 target에 존재해도 semantics가 다르면 별도 target field로 유지한다.
1. Target에서 핵심 tool 또는 delegation capability를 표현할 수 없으면 동일 Agent로 간주하지 않고 compatibility gap으로 처리한다.
1. Read-only Agent는 body의 authority와 target tool permission이 모두 read-only intent와 일치해야 한다.
1. Agent가 다른 Agent를 호출해야 하면 해당 target의 subagent/delegation capability를 명시적으로 요구한다.

## Minimal

```yaml
---
name: reviewer
description: Review changes for correctness and regressions without modifying source files.
targets: ["*"]
---

# Reviewer

## Responsibility
Produce the final review.

## Authority
Read relevant files and evidence only.

## Constraints
Do not modify source files or repository state.
```

## Extended

```yaml
---
name: reviewer
description: Review changes for correctness and regressions without modifying source files.
targets: ["claudecode", "copilot", "antigravity-ide"]

claudecode:
  model: inherit
  tools: ["Read", "Grep"]
  disallowedTools: ["Write", "Bash"]

copilot:
  tools:
    - web/fetch

antigravity-ide:
  tools: ["read", "search"]
  mainAgent: true
  subagent: true
  model: inherit
  commandExecutionPolicy: off
---

# Reviewer

Review the requested change. Do not mutate source or repository state.
```

## Projection Contract

- VS Code/GitHub Copilot/Antigravity/Claude Code 등의 native Agent file은 이 source의 projection이다.
- Body의 role/authority를 유지하면서 target runtime field를 native schema로 변환한다.
- Unsupported tool, permission, handoff, background, isolation 기능을 조용히 삭제하지 않는다.
- Target-specific native field를 다른 target의 공통 contract로 승격하지 않는다.

## Validation

```bash
rulesync generate --dry-run --features subagents --targets <targets>
rulesync generate --check --features subagents --targets <targets>
```

생성 후 각 target의 native validator가 있으면 추가로 검증한다.

## References

- [Rulesync File Formats — subagents](https://rulesync.dyoshikawa.com/reference/file-formats.html#rulesync-subagents-md)
