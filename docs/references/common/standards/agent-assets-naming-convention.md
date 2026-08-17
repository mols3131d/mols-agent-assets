---
title: Agent Asset Naming Convention
description: 파일시스템 탐색과 이름 충돌 방지를 위한 범용 Agent Asset 이름 접두사 컨벤션
---

# Agent Asset Naming Convention

이 문서는 Rule, Skill, Prompt, Agent처럼 이름을 직접 정할 수 있는 Agent Asset에 적용하는 **파일시스템 중심 naming convention**을 정의한다.

목적은 taxonomy를 이름에 인코딩하는 것이 아니라 다음 두 가지다.

- 파일시스템에서 관련 자산을 찾고 묶어 보기 쉽게 한다.
- 서로 다른 범위에서 들어온 자산의 이름 충돌을 줄인다.

플랫폼이 강제하는 파일명이나 identifier 규격이 이 컨벤션보다 우선한다.

## Pattern

```text
[<source>-][<family>-]<name>[-<extension>]
```

`name`만 필수다. 나머지는 실제 구분에 도움이 될 때만 추가한다.

| Segment | Responsibility | Examples |
| --- | --- | --- |
| `source` | 자산의 출처·소유 범위를 구분하는 선택적 namespace | `project-pivot`, `prj`, `user`, `mols` |
| `family` | 함께 설계·운영되는 자산군의 공통 이름 | `liner`, `caveman` |
| `name` | 자산의 핵심 기능이나 역할 | `tag`, `review`, `research` |
| `extension` | 같은 핵심 자산의 명확한 특수화 | `runtime`, `batch`, `github` |

이 pattern은 사람이 읽기 위한 의미 구조다. 각 segment 자체가 kebab-case일 수 있으므로 문자열을 역파싱하는 schema로 사용하지 않는다. 기계가 provenance나 scope를 알아야 한다면 별도 metadata를 사용한다.

## Source

`source`는 canonical provenance metadata가 아니라 **filesystem namespace hint**다.

필요에 따라 다음처럼 사용할 수 있다.

- 구체적인 프로젝트 이름: `project-pivot-*`
- 현재 프로젝트를 뜻하는 상대 표기: `prj-*`
- 사용자 범위: `user-*`
- 제작자나 조직: `mols-*`, `acme-*`

`prj`, `user` 같은 상대 표기는 그 scope가 이미 알려진 저장 위치에서 유용하다. 여러 프로젝트의 자산을 같은 namespace에 모으면 구체적인 프로젝트명이나 제작자 식별자를 선호한다.

## Family and Extension

`family`는 여러 자산이 하나의 제품군이나 설계 계열로 관리될 때만 둔다.

```text
liner-tag
liner-filename
liner-custom-tags
```

`extension`은 같은 핵심 자산의 동작이나 대상이 실제로 달라지는 특수화에 사용한다.

```text
liner-tag-runtime
liner-tag-batch
```

`v2`, `new`, `final`, `advanced`처럼 lifecycle이나 막연한 품질을 표현하는 suffix는 피한다. 버전과 상태는 이름이 아니라 version control이나 metadata가 소유한다.

## Minimal Naming Rule

**가장 짧은 충돌 없는 이름을 사용한다.**

구분이 필요할 때만 왼쪽에는 namespace를, 오른쪽에는 specialization을 추가한다.

```text
tag
→ liner-tag
→ mols-liner-tag
```

이름에 domain, scope, owner, type, version을 모두 넣어 작은 metadata schema처럼 만들지 않는다.

## Host Boundary

이 컨벤션은 host가 자유롭게 정하도록 허용한 **logical asset name**에 적용한다.

- `SKILL.md`, `AGENTS.md`처럼 platform이 강제하는 고정 파일명은 rename하지 않는다.
- `.agent.md`, `.prompt.md`처럼 host가 의미를 부여하는 suffix가 있다면 suffix 바깥의 logical name에 적용한다.
- Agent Skills에 적용할 때 최종 Skill 이름과 디렉터리는 Agent Skills specification의 naming contract를 만족해야 한다.
- target harness가 더 엄격한 규칙을 가지면 해당 공식 규격을 따른다.

## External Skills

외부 Skill은 이 컨벤션을 맞추기 위해 임의로 rename하지 않고 **upstream naming을 우선한다**.

Agent Skills에서는 `name`이 디렉터리명과 결합된 identifier이므로 rename은 단순한 filesystem 정리가 아니라 upstream 자산 자체의 변경이 될 수 있다. 이름 충돌이 실제로 발생하면 target harness의 namespace, placement, precedence 또는 qualified invocation 같은 충돌 해결 수단을 먼저 사용한다.

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

구체적인 segment 경계는 문맥에 따라 달라질 수 있다. 이름만 보고 모든 metadata를 복원할 수 있어야 한다는 요구는 두지 않는다.

## Review Test

새 이름을 정할 때 다음만 확인한다.

1. `name`만으로 충분히 구분되는가?
1. `source` 또는 `family`가 탐색이나 collision avoidance에 실제로 도움이 되는가?
1. `extension`이 독립된 specialization을 나타내는가?
1. host의 naming contract를 침범하지 않는가?
1. 외부 Skill의 upstream 이름을 불필요하게 바꾸고 있지 않은가?

## Research Basis

- [Agent Skills Specification](https://agentskills.io/specification) — Skill `name`은 디렉터리명과 일치하는 제한된 identifier다.
- [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) — 중복 Skill 이름은 name-based precedence의 대상이 될 수 있다.
- [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — 일관되고 구체적인 Skill naming을 권장한다.
