---
title: Skill Canonical Superset
description: 여러 Skill runtime에 투영할 repository-local canonical Skill authoring spec
---

# Skill Canonical Superset

Skill Superset은 **Agent Skills package**를 portable core로 사용하고, target-specific metadata만 namespaced extension으로 추가한다.

## Package

```text
<skill-name>/
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
license: <string>
compatibility: <string>
metadata:
  <key>: <string>
allowed-tools: <string>

targets: [<target>]

copilot:
  <copilot-only fields>

antigravity:
  <antigravity-only fields>

chatgpt:
  <chatgpt-only fields>
---

<skill instructions>
```

## Fields

| Field | Requirement | Contract |
| --- | --- | --- |
| `name` | Required | Agent Skills-compatible Skill identity. |
| `description` | Required | capability와 activation condition을 함께 설명한다. |
| `license` | Optional | Portable Skill license. |
| `compatibility` | Optional | 환경/runtime requirement. |
| `metadata` | Optional | Portable string metadata. |
| `allowed-tools` | Optional | Portable tool allowance가 의미 있을 때 사용. |
| `targets` | Optional | 명시하면 지원 target을 제한한다. |
| `<target>` | Optional | 해당 runtime에서만 필요한 discovery/invocation/packaging metadata. |
| body | Required | 실제 reusable capability instructions. |

`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`는 portable core다. Target block에서 같은 의미를 다시 정의하지 않는다.

## Target Extensions

```yaml
copilot:
  argument-hint: "[pr-number]"
  user-invocable: true

chatgpt:
  install-surface: personal-skill
```

Target extension은 portable Agent Skills field로 표현할 수 없는 정보만 둔다.

## Body Contract

Body는 다음을 포함할 수 있다.

- capability contract
- 실행 절차와 decision rule
- guardrail
- output semantics
- 필요한 resource loading instruction

Target별 runtime 차이가 행동 자체를 바꾸면 target block만으로 숨기지 말고 body 또는 target-specific projection에서 그 차이를 명시한다.

## Resources

- `references/` — runtime에서 필요할 때만 로드하는 지식.
- `scripts/` — capability 수행에 필요한 executable helper.
- `assets/` — template, fixture 등 runtime asset.

Maintainer-only docs, evals, recovery notes는 runtime Superset package와 분리한다.

## Minimal Example

```yaml
---
name: pr-review
description: Review pull request changes for correctness and regressions. Use when asked to review a PR.
---

# PR Review

Inspect the requested change and report evidence-backed findings.
```

## Projection Requirements

- Portable Agent Skills semantics를 우선 보존한다.
- Target-native metadata는 해당 target projection에만 반영한다.
- Flat target이 required resource를 담을 수 없으면 내용을 삭제하지 말고 incompatible projection으로 처리한다.

## References

- [Agent Skills Specification](https://agentskills.io/specification)
- [Skill Target Profiles](agent-assets-skills-target-profiles.md)
