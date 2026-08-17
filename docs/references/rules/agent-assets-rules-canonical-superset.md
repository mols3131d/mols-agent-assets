---
title: Rule Canonical Superset
description: Rulesync Rule을 기준으로 한 repository-local canonical Rule spec
---

# Rule Canonical Superset

Canonical Rule은 **`.rulesync/rules/<name>.md`** 로 작성한다.

## Schema

```yaml
---
root: false
localRoot: false
targets: ["*"]
description: <string>
globs: ["<glob>"]

agentsmd:
  subprojectPath: <path>

copilot:
  name: <string>
  excludeAgent: <code-review|cloud-agent>

antigravity:
  trigger: <always_on|glob|manual|model_decision>
  globs: ["<glob>"]
  description: <string>

# 기타 target-specific block 허용
<target>: <mapping>
---

<rule instructions>
```

## Fields

| Field | Requirement | Meaning |
| --- | --- | --- |
| `root` | **Required** | `true`면 root/baseline Rule, `false`면 modular Rule |
| `localRoot` | Optional, default `false` | 개인·project-local root Rule |
| `targets` | **Required** | `"*"` 또는 Rulesync target 목록 |
| `description` | Recommended | Rule 목적/적용 조건. model-decided target에서 activation hint로도 사용 가능 |
| `globs` | Optional | file/path scoped Rule의 canonical glob |
| `<target>` | Optional | canonical field로 표현되지 않는 target-native semantics |
| body | **Required** | 실제 지속 적용 policy/constraint |

## Repository Constraints

1. `root: true`는 repository baseline처럼 실제 root semantics가 필요한 Rule에만 사용한다.
1. File scope는 target-specific selector보다 top-level `globs`로 표현 가능한 경우 `globs`를 authority로 둔다.
1. Directory subtree scope는 `agentsmd.subprojectPath`처럼 target이 요구하는 별도 구조가 있을 때 target block에 둔다.
1. 공통 의미를 target block에 복제하지 않는다. **공통 field → target override** 순서로 둔다.
1. Target block은 다른 target에 전파하면 안 되는 native-only 의미만 소유한다.
1. 여러 `root: true` fragment를 허용하더라도 동일 policy를 중복 정의하지 않는다.

## Minimal

```yaml
---
root: true
targets: ["*"]
description: Repository-wide development rules
---

# Development Rules

- Follow repository-local instructions.
- Do not commit generated secrets.
```

## Scoped

```yaml
---
root: false
targets: ["copilot", "antigravity-ide"]
description: Markdown authoring rules
globs: ["**/*.md"]

antigravity:
  trigger: glob
  globs: ["**/*.md"]
---

Use repository Markdown conventions.
```

## Projection Contract

- GitHub Copilot, Antigravity 등 target-native Rule은 이 source에서 생성되는 **projection**이다.
- Target이 지원하지 않는 field는 조용히 의미를 바꾸지 말고 omission/approximation으로 취급한다.
- 이미 하나의 native Rule이 authoritative인 경우에는 canonical migration 없이 Rulesync bridge를 사용할 수 있다.

## Validation

```bash
rulesync generate --dry-run --features rules --targets <targets>
rulesync generate --check --features rules --targets <targets>
```

설치된 Rulesync의 schema와 target adapter가 runtime authority다.

## References

- [Rulesync File Formats — rules](https://rulesync.dyoshikawa.com/reference/file-formats.html#rulesync-rules-md)
- [Rule Projections](agent-assets-rules-projections.md)
