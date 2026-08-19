---
title: Agent Asset Naming Convention
description: 폴더 계층을 쓰기 어려운 환경에서 관리 편의와 이름 충돌 방지를 위한 configuration asset naming convention
---

# Agent Asset Naming Convention

이 문서는 Rulesync feature 또는 다른 agent harness에서 logical name을 직접 정할 수 있는 configuration asset에 적용하는 **파일시스템 중심 naming convention**을 정의한다.

이 컨벤션의 최우선 목적은 두 가지다.

1. 폴더 계층을 사용할 수 없거나 사용하기 불편한 환경에서 이름만으로 관련 자산을 묶어 보고 관리하기 쉽게 한다.
1. 서로 다른 범위에서 들어온 자산의 이름 중복과 충돌을 줄인다.

**이름은 metadata를 기록하는 장소가 아니다.** 출처, scope, owner 같은 정보를 완전하게 표현하거나 복원하기 위한 schema가 아니며, 관리 편의와 collision avoidance에 필요한 최소한의 구분만 이름에 둔다.

Rulesync 또는 target platform이 강제하는 identifier/file naming contract가 이 컨벤션보다 우선한다.

## Pattern

```text
[<source>-][<family>-]<name>[-<extension>]
```

`name`만 필수다. 나머지는 실제 관리나 충돌 방지에 도움이 될 때만 추가한다.

| Segment | Responsibility | Examples |
| --- | --- | --- |
| `source` | 서로 다른 출처·소유 범위의 자산을 이름에서 구분하기 위한 선택적 prefix | `project-pivot`, `prj`, `user`, `mols` |
| `family` | 함께 관리하는 자산군을 파일시스템에서 묶어 보기 위한 공통 이름 | `liner`, `caveman` |
| `name` | 자산의 핵심 기능이나 역할 | `tag`, `review`, `research` |
| `extension` | 같은 핵심 자산의 명확한 특수화 | `runtime`, `batch`, `github` |

이 pattern은 사람이 파일시스템에서 자산을 관리하기 위한 naming convention이다. 각 segment 자체가 kebab-case일 수 있으므로 문자열을 역파싱하는 schema로 사용하지 않는다. 기계가 provenance, scope, owner 같은 정보를 알아야 한다면 이름이 아니라 source framework나 target contract가 제공하는 metadata를 사용한다.

## Source

`source`는 provenance metadata가 아니라 **이름 충돌을 줄이고 자산을 묶어 보기 위한 prefix**다.

필요에 따라 다음처럼 사용할 수 있다.

- 구체적인 프로젝트 이름: `project-pivot-*`
- 현재 프로젝트를 뜻하는 상대 표기: `prj-*`
- 사용자 범위: `user-*`
- 제작자나 조직: `mols-*`, `acme-*`

`source` 값은 고정 enum으로 만들지 않는다. 자산이 놓이는 범위에서 짧고 안정적으로 구분되는 이름을 사용한다.

`prj`, `user` 같은 상대 표기는 그 scope가 이미 알려진 저장 위치에서 유용하다. 여러 프로젝트의 자산을 같은 flat namespace에 모으면 구체적인 프로젝트명이나 제작자 식별자를 선호한다.

## Family and Extension

`family`는 여러 자산이 하나의 제품군이나 설계 계열로 관리될 때만 둔다.

```text
liner-tag
liner-filename
liner-custom-tags
```

이는 폴더로 다음처럼 묶을 수 없는 상황을 이름으로 보완하는 역할을 한다.

```text
liner/
├─ tag
├─ filename
└─ custom-tags
```

`extension`은 같은 핵심 자산의 동작이나 대상이 실제로 달라지는 특수화에 사용한다.

```text
liner-tag-runtime
liner-tag-batch
```

`v2`, `new`, `final`, `advanced`처럼 lifecycle이나 막연한 품질을 표현하는 suffix는 피한다. 버전과 상태는 이름이 아니라 version control이나 metadata가 소유한다.

## Minimal Naming Rule

**관리와 충돌 방지에 충분한 가장 짧은 이름을 사용한다.**

구분이 필요할 때만 왼쪽에는 `source`나 `family`를, 오른쪽에는 specialization을 추가한다.

```text
tag
→ liner-tag
→ mols-liner-tag
```

접두사와 접미사는 폴더 계층을 보완하고 이름 충돌을 피하기 위한 수단이다. domain, scope, owner, type, version 같은 metadata를 이름에 모두 넣어 작은 schema처럼 만들지 않는다.

## Host Boundary

이 컨벤션은 source framework나 target harness가 자유롭게 정하도록 허용한 **logical asset name**에만 적용한다.

- `SKILL.md`, `AGENTS.md`처럼 framework/target이 강제하는 고정 파일명은 rename하지 않는다.
- `.agent.md`, `.prompt.md`처럼 target이 의미를 부여하는 suffix가 있다면 suffix 바깥의 logical name에 적용한다.
- Rulesync-managed source는 current Rulesync naming/schema contract를 먼저 따른다.
- Agent Skills output에는 Agent Skills specification의 naming contract를 적용한다.
- target harness가 더 엄격한 규칙을 가지면 해당 공식 규격을 따른다.

## External Skills

외부 Skill은 이 컨벤션을 맞추기 위해 임의로 rename하지 않고 **upstream naming을 우선한다**.

Agent Skills에서는 `name`이 디렉터리명과 결합된 identifier이므로 rename은 단순한 filesystem 정리가 아니라 upstream 자산 자체의 변경이 될 수 있다. 이름 충돌이 실제로 발생하면 source framework나 target harness가 지원하는 namespace, placement, precedence 또는 qualified invocation 같은 충돌 해결 수단을 먼저 사용한다.

통합을 위해 rename이 불가피하다면 upstream provenance는 별도로 보존한다.

## Examples

```text
review
user-review
project-pivot-reliability-review
liner-tag
mols-liner-tag
liner-tag-runtime
```

## Review Test

새 이름을 정할 때 다음만 확인한다.

1. 폴더 계층 없이도 관련 자산을 찾고 묶어 보기 쉬운가?
1. 현재 namespace에서 이름 충돌 가능성을 충분히 줄이는가?
1. `source`, `family`, `extension`이 실제 관리 편의에 필요한가?
1. metadata를 이름에 과도하게 인코딩하고 있지 않은가?
1. source framework와 target naming contract를 침범하지 않는가?
1. 외부 Skill의 upstream 이름을 불필요하게 바꾸고 있지 않은가?

## Research Basis

- [Rulesync](https://github.com/dyoshikawa/rulesync) — canonical feature/source와 target projection의 naming boundary.
- [Agent Skills Specification](https://agentskills.io/specification) — Skill `name`은 디렉터리명과 일치하는 제한된 identifier다.
- [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) — 중복 Skill 이름은 name-based precedence의 대상이 될 수 있다.
- [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — 일관되고 구체적인 Skill naming을 권장한다.
