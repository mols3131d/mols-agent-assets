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

## Family Documentation

같은 family의 Skill이 durable maintainer 지식을 공유하면 `docs/skills/<family>/`을 공동 owner로 사용할 수 있습니다.

- Family 문서 이름은 관리 편의를 위한 owner label이며 runtime metadata가 아닙니다.
- Family membership은 문서의 `README.md`에 사람이 읽을 수 있게 명시하고 이름을 역파싱하는 별도 registry나 schema를 만들지 않습니다.
- Family 문서는 discoverable Skill을 대체하지 않습니다. 서로 다른 trigger와 책임은 계속 독립 Skill로 유지합니다.
- 하나의 Skill에만 적용되는 maintainer 지식은 `docs/skills/<skill-name>/`에 남길 수 있습니다.
