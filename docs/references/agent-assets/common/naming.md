---
title: Agent Asset Naming Convention
description: flat namespace에서 관리 편의와 이름 충돌 방지를 위한 최소 naming convention
---

# Agent Asset Naming Convention

이 convention은 **폴더 계층을 쓰기 어렵거나 flat namespace에서 충돌이 생길 때** 사용합니다. 이름을 metadata schema로 사용하지 않습니다.

```text
[<source>-][<family>-][<domain>-][<subdomain>-]<name>[-<extension>]...
```

`name`만 필수입니다. 나머지는 실제 관리나 collision avoidance에 필요할 때만 추가합니다. `[-<extension>]...`은 extension이 없거나 하나 이상 반복될 수 있음을 뜻합니다.

| Segment | 의미 | 예시 |
| --- | --- | --- |
| `source` | 서로 다른 출처·범위 구분 | `project-pivot`, `user`, `mols` |
| `family` | 함께 관리하는 자산군 | `liner`, `caveman` |
| `domain` | 자산이 다루는 넓은 문제·지식 영역 | `data`, `markdown`, `agent` |
| `subdomain` | domain 안에서 실제 구분이 필요한 더 좁은 영역 | `reliability`, `dashboard`, `skill` |
| `name` | 핵심 기능·역할 | `tag`, `review`, `research` |
| `extension` | 같은 핵심 자산의 명확한 특수화. 필요하면 반복 가능 | `runtime`, `batch`, `github` |

## Rules

- 관리와 충돌 방지에 충분한 가장 짧은 이름을 사용합니다.
- `source`, `family`, `domain`, `subdomain`, `extension`은 실제 구분이 필요할 때만 추가합니다.
- `family`는 함께 관리되는 자산군을, `domain`과 `subdomain`은 자산이 다루는 문제·지식 영역을 나타냅니다. 같은 단어가 두 역할을 충분히 표현하면 중복해서 넣지 않습니다.
- `subdomain`은 domain만으로 구분이 부족할 때 사용합니다. 단순히 계층을 채우기 위해 추가하지 않습니다.
- `extension`은 같은 핵심 자산을 둘 이상의 독립적인 축으로 특수화해야 할 때 여러 개 사용할 수 있습니다. 필요하지 않은 extension을 계층처럼 누적하지 않습니다.
- `v2`, `new`, `final`, `advanced` 같은 version·상태·막연한 품질을 이름에 넣지 않습니다.
- 이름을 역파싱해 provenance, scope, owner, domain을 복원하지 않습니다. 기계가 필요한 정보는 source framework나 target contract의 metadata를 사용합니다.
- `SKILL.md`, `AGENTS.md`처럼 framework가 강제하는 filename과 target 고유 identifier contract가 우선합니다.
- 외부 Skill은 이 convention에 맞추기 위해 임의 rename하지 않습니다.

예: `review`, `liner-tag`, `data-reliability-review`, `mols-liner-music-metadata-tag-runtime-github`.
