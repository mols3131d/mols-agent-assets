---
title: Prompt Canonical Superset
description: Rulesync Command format을 Prompt transport로 사용하는 repository-local canonical Prompt spec
---

# Prompt Canonical Superset

Canonical Prompt는 **`.rulesync/commands/<name>.md`** 로 작성한다.

이 저장소의 Prompt는 reusable invocation instruction을 뜻한다. Rulesync에서는 이 cross-target surface를 `commands`라고 부른다.

## Schema

```yaml
---
description: <string>
targets: ["*"]

copilot:
  description: <string>
  agent: <ask|agent|plan|custom-agent-name>

antigravity:
  trigger: </command>
  turbo: <boolean>

pi:
  argument-hint: <string>

codexcli:
  argument-hint: <string>

roo:
  mode: <mode-slug>

# 기타 target-specific block 허용
<target>: <mapping>
---

<prompt body>
```

## Fields

| Field | Requirement | Meaning |
| --- | --- | --- |
| filename/path | **Required** | Prompt identity와 command name. Nested path는 namespace가 될 수 있음 |
| `description` | **Required** | Prompt 목적/사용 맥락 |
| `targets` | **Required** | `"*"` 또는 Rulesync target 목록 |
| `<target>` | Optional | target-native invocation metadata |
| body | **Required** | 실제 reusable prompt/workflow |

`name`은 top-level front matter가 아니라 canonical file path에서 결정한다.

## Arguments

Canonical body는 Rulesync의 universal command syntax를 사용한다.

```text
$ARGUMENTS   # 전체 arguments
$1 ... $N   # positional arguments
```

Target이 다른 placeholder syntax를 요구하면 Rulesync가 generation/import 과정에서 변환한다.

Arguments를 사용하는 Prompt는 body 초반에 의미와 default를 명시한다.

```markdown
target_pr = $1

If target_pr is omitted, use the pull request for the current branch.
```

## Repository Constraints

1. Prompt의 task contract와 workflow는 body가 authority다.
1. Target-independent argument semantics를 target block에 복제하지 않는다.
1. Agent/model/mode 같은 execution selector는 실제 target에서 필요한 경우에만 target block에 둔다.
1. Target selector가 없으면 Prompt의 의미가 깨지는 경우 projection을 unsupported로 판정한다. 조용히 selector를 삭제하지 않는다.
1. Nested command path를 사용할 때는 flat-only target의 basename collision 가능성을 검증한다.
1. Skill과 Prompt가 동일 target에서 같은 slash-command namespace를 공유하는 경우 이름 충돌을 피한다.

## Minimal

```yaml
---
description: Review the requested pull request
targets: ["*"]
---

pr = $1

Review the pull request and report evidence-backed findings.
```

## Extended

```yaml
---
description: Review the requested pull request
targets: ["copilot", "antigravity-ide", "pi"]

copilot:
  agent: agent

antigravity:
  trigger: /review
  turbo: false

pi:
  argument-hint: "[pr-number]"
---

pr = $1

If pr is omitted, use the pull request for the current branch.
Review it and report evidence-backed findings.
```

## Projection Contract

- `.prompt.md`, slash command, saved prompt, Skill-backed command 등 target-native surface 차이는 projection concern이다.
- Target이 Prompt surface 대신 Skill surface만 제공하면 Prompt semantics를 보존한 projection만 허용한다.
- Target-specific execution metadata가 지원되지 않으면 loss를 명시한다.

## Validation

```bash
rulesync generate --dry-run --features commands --targets <targets>
rulesync generate --check --features commands --targets <targets>
```

## References

- [Rulesync File Formats — commands](https://rulesync.dyoshikawa.com/reference/file-formats.html#rulesync-commands-md)
- [Rulesync Command Syntax](https://rulesync.dyoshikawa.com/reference/command-syntax.html)
