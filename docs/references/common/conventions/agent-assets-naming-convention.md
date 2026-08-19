---
title: Agent Asset Naming Convention
description: flat namespace에서 관리 편의와 이름 충돌 방지를 위한 최소 naming convention
---

# Agent Asset Naming Convention

이 컨벤션은 **폴더 계층을 쓰기 어렵거나 flat namespace에서 이름 충돌이 생기는 경우**를 위한 관리 규칙입니다. 이름을 metadata schema로 사용하지 않습니다.

## Pattern

```text
[<source>-][<family>-]<name>[-<extension>]
```

`name`만 필수입니다. 나머지는 실제 관리나 collision avoidance에 도움이 될 때만 추가합니다.

| Segment | 책임 | 예시 |
| --- | --- | --- |
| `source` | 서로 다른 출처·범위를 구분 | `project-pivot`, `user`, `mols` |
| `family` | 함께 관리하는 자산군을 묶음 | `liner`, `caveman` |
| `name` | 핵심 기능이나 역할 | `tag`, `review`, `research` |
| `extension` | 같은 핵심 자산의 명확한 특수화 | `runtime`, `batch`, `github` |

각 segment 자체가 `kebab-case`일 수 있으므로 이름을 역파싱해 provenance, scope, owner를 복원하지 않습니다. 기계가 그런 정보가 필요하면 source framework나 target contract의 metadata를 사용합니다.

## Rules

- **관리와 충돌 방지에 충분한 가장 짧은 이름**을 사용합니다.
- `source`, `family`, `extension`은 실제 구분이 필요할 때만 추가합니다.
- `v2`, `new`, `final`, `advanced`처럼 version·상태·막연한 품질을 이름에 넣지 않습니다.
- `SKILL.md`, `AGENTS.md`처럼 framework가 강제하는 filename은 이 규칙으로 바꾸지 않습니다.
- Target이 자체 identifier/file naming contract를 가지면 그 contract가 우선합니다.
- 외부 Skill은 이 컨벤션에 맞추기 위해 임의로 rename하지 않고 upstream naming을 우선합니다.

## Examples

```text
review
user-review
project-pivot-reliability-review
liner-tag
mols-liner-tag
liner-tag-runtime
```

## Decision Test

새 이름을 정할 때 다음만 확인합니다.

1. Flat namespace에서 찾고 묶기 쉬운가?
1. 현재 범위의 이름 충돌을 충분히 줄이는가?
1. 선택 segment가 실제로 필요한가?
1. Metadata를 이름에 과도하게 인코딩하지 않았는가?
1. Upstream/framework naming contract를 침범하지 않는가?

## References

- [Rulesync](https://github.com/dyoshikawa/rulesync)
- [Agent Skills Specification](https://agentskills.io/specification)
