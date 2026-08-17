---
title: Skill Canonical Superset
description: Rulesync Skill과 Agent Skills core를 결합한 repository-local canonical Skill spec
---

# Skill Canonical Superset

Canonical Skill은 **`.rulesync/skills/<name>/SKILL.md` + supporting files** 로 작성한다.

Portable core는 Agent Skills Specification을 따르고, Rulesync의 `targets`와 target blocks를 Superset extension으로 사용한다.

## Package

```text
.rulesync/skills/<name>/
├─ SKILL.md
├─ references/   # optional
├─ scripts/      # optional
└─ assets/       # optional
```

## Schema

```yaml
---
name: <kebab-case>
description: <string>
targets: ["*"]

disable-model-invocation: <boolean>
user-invocable: <boolean>

agentsskills:
  license: <string>
  compatibility: <string>
  metadata:
    <key>: <string>
  allowed-tools: <string-or-list>

copilot:
  license: <string>
  allowed-tools: <string-or-list>
  argument-hint: <string>
  user-invocable: <boolean>
  disable-model-invocation: <boolean>
  context: <fork>

codexcli:
  interface:
    display_name: <string>
    short_description: <string>
    default_prompt: <string>
  policy:
    allow_implicit_invocation: <boolean>
  dependencies:
    tools: <list>

# 기타 target-specific block 허용
<target>: <mapping>
---

<skill instructions>
```

## Core Fields

| Field | Requirement | Constraint |
| --- | --- | --- |
| `name` | **Required** | Agent Skills 규격: 1–64자, lowercase/digit/hyphen, directory name과 일치 |
| `description` | **Required** | 1–1024자. capability + activation condition |
| `targets` | **Required** | `"*"` 또는 Rulesync target 목록 |
| `disable-model-invocation` | Optional | 지원 target의 shared invocation default |
| `user-invocable` | Optional | 지원 target의 shared user-invocation default |
| `agentsskills` | Optional | portable Agent Skills optional fields |
| `<target>` | Optional | target-native extension/override |
| body | **Required** | runtime instructions |

## Agent Skills Core

`agentsskills` block은 portable optional fields의 canonical home이다.

| Field | Constraint |
| --- | --- |
| `license` | license name 또는 bundled license reference |
| `compatibility` | 1–500자 string |
| `metadata` | string → string mapping |
| `allowed-tools` | Agent Skills 출력에서는 space-separated scalar로 정규화됨 |

`name`과 `description`은 항상 top-level canonical field다. Target block에서 별도 authority로 재정의하지 않는다.

## Repository Constraints

1. Capability identity와 activation은 `name` + `description`에 완결한다.
1. Portable하게 표현 가능한 metadata는 `agentsskills`에 먼저 둔다.
1. Target-specific capability만 `<target>` block에 둔다.
1. `user-invocable` / `disable-model-invocation`은 여러 target에 동일한 의미라면 top-level shared default를 사용한다.
1. Runtime에 필요한 supporting file은 package 안에 보존한다. Flat target으로 투영할 수 없으면 내용을 버리지 말고 unsupported profile로 판정한다.
1. `.docs/` 같은 maintainer-only 자료는 runtime package Superset에 넣지 않는다.

## Minimal

```yaml
---
name: pr-review
description: Review a pull request for correctness and regressions. Use when asked to review PR changes.
targets: ["*"]
---

# PR Review

Inspect the requested change and report evidence-backed findings.
```

## Extended

```yaml
---
name: pr-review
description: Review a pull request for correctness and regressions. Use when asked to review PR changes.
targets: ["agentsskills", "copilot", "codexcli"]
user-invocable: true

agentsskills:
  license: MIT
  compatibility: Requires git
  metadata:
    version: "1.0.0"
  allowed-tools: "shell"

copilot:
  argument-hint: "[pr-number]"

codexcli:
  policy:
    allow_implicit_invocation: true
---

# PR Review

Inspect the requested change and report evidence-backed findings.
```

## Projection Contract

- Agent Skills-compatible target에는 portable core를 우선 보존한다.
- Target-specific field는 해당 target projection에만 반영한다.
- Generated Skill이 portable 규격을 위반하는 경우 생성 성공을 호환성 성공으로 취급하지 않는다.
- Target이 canonical Agent Skills package를 직접 읽을 수 있으면 별도 sibling projection을 만들지 않는다.

## Validation

```bash
rulesync generate --dry-run --features skills --targets <targets>
rulesync generate --check --features skills --targets <targets>
skills-ref validate <generated-skill-directory>
```

## References

- [Rulesync File Formats — skills](https://rulesync.dyoshikawa.com/reference/file-formats.html#rulesync-skills-skill-md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Skill Target Profiles](agent-assets-skills-target-profiles.md)
