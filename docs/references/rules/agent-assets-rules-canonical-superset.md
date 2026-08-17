---
title: Rule Canonical Superset
description: 여러 harness에 투영할 Rule의 repository-local canonical authoring spec
---

# Rule Canonical Superset

Rule Superset은 지속 적용되는 policy와 constraint를 target-independent하게 보존한다.

## Schema

```yaml
---
name: <kebab-case>
description: <string>
targets: [<target>]

scope:
  level: <global|repository|directory|glob>
  include: [<path-or-glob>]
  exclude: [<path-or-glob>]

copilot:
  <copilot-only fields>

antigravity:
  <antigravity-only fields>
---

<rule body>
```

## Fields

| Field | Requirement | Contract |
| --- | --- | --- |
| `name` | Required | Rule identity. `kebab-case`. |
| `description` | Required | 무엇을 지속적으로 강제하는지 요약한다. |
| `targets` | Optional | 명시하면 지원 target을 제한한다. 생략하면 target-neutral로 취급한다. |
| `scope.level` | Required | Rule 적용 범위의 종류. |
| `scope.include` | Conditional | `directory` 또는 `glob` scope에서 적용 대상을 지정한다. |
| `scope.exclude` | Optional | canonical scope에서 제외할 경로/패턴. |
| `<target>` | Optional | 해당 harness에서만 필요한 scope/activation/metadata. |
| body | Required | 실제 policy와 constraint. |

## Scope

- `global` — 사용자/환경 수준에서 지속 적용.
- `repository` — repository 전체에 적용.
- `directory` — 하나 이상의 directory subtree에 적용.
- `glob` — path pattern에 일치하는 대상에 적용.

Target이 scope를 더 제한적으로만 표현할 수 있으면 target block에서 그 차이를 보존한다.

## Target Extensions

```yaml
copilot:
  applyTo: "**/*.md"

antigravity:
  trigger: glob
  globs: ["**/*.md"]
```

위 필드는 target extension 예시다. Canonical authority는 `scope`와 body에 있고, target block은 공통 schema로 표현할 수 없는 native semantics만 둔다.

## Body Contract

Body는 지속 적용할 policy, 금지/필수 constraint, 필요한 예외와 precedence 조건만 소유한다.

일회성 작업 절차는 Prompt, 재사용 capability는 Skill, 독립 role/authority는 Agent로 분리한다.

## Minimal Example

```yaml
---
name: markdown-style
description: Repository Markdown authoring rules
scope:
  level: glob
  include: ["**/*.md"]
---

Use repository Markdown conventions.
Run the configured Markdown auto-fixer before committing.
```

## Projection Requirements

- Common fields와 body의 의미를 우선 보존한다.
- Target-native path, filename, selector syntax는 projection 단계에서 결정한다.
- Target이 표현하지 못하는 scope나 activation 차이는 명시적으로 기록한다.

## References

- [Rule Projections](agent-assets-rules-projections.md)
- [GitHub Copilot custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)
- [Google Antigravity IDE](https://codelabs.developers.google.com/getting-started-agy-ide)
