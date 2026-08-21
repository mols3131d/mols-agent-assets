---
title: Agent Asset Naming Convention
description: flat namespace에서 관리 편의와 이름 충돌 방지를 위한 최소 naming convention
---

# Agent Asset Naming Convention

이 convention은 **폴더 계층을 쓰기 어렵거나 flat namespace에서 충돌이 생길 때** 사용합니다. 이름을 metadata schema로 사용하지 않습니다.

```text
[<source>-][<family>-]<name>[-<extension>]
```

`name`만 필수입니다. 나머지는 실제 관리나 collision avoidance에 필요할 때만 추가합니다.

| Segment | 의미 | 예시 |
| --- | --- | --- |
| `source` | 서로 다른 출처·범위 구분 | `project-pivot`, `user`, `mols` |
| `family` | 함께 관리하는 자산군 | `liner`, `caveman` |
| `name` | 핵심 기능·역할 | `tag`, `review`, `research` |
| `extension` | 같은 핵심 자산의 명확한 특수화 | `runtime`, `batch`, `github` |

## Rules

- 관리와 충돌 방지에 충분한 가장 짧은 이름을 사용합니다.
- `source`, `family`, `extension`은 실제 구분이 필요할 때만 추가합니다.
- `v2`, `new`, `final`, `advanced` 같은 version·상태·막연한 품질을 이름에 넣지 않습니다.
- 이름을 역파싱해 provenance, scope, owner를 복원하지 않습니다. 기계가 필요한 정보는 source framework나 target contract의 metadata를 사용합니다.
- `SKILL.md`, `AGENTS.md`처럼 framework가 강제하는 filename과 target 고유 identifier contract가 우선합니다.
- 외부 Skill은 이 convention에 맞추기 위해 임의 rename하지 않습니다.

예: `review`, `liner-tag`, `mols-liner-tag`, `liner-tag-runtime`.
