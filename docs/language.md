---
description: README·docs·comments·Git/GitHub communication과 Agent Asset에서 한국어와 영어를 어떻게 사용할지 판단할 때 적용하는 repository 언어 정책입니다.
---

# Language

- 이 저장소의 기본 언어는 한국어입니다. 한국어가 자연스러우면 한국어를 사용합니다. 
- 보조 언어는 영어입니다. 한국어가 부자연스러우면 영어가 자연스러운지 판단합니다.
  - 영어가 자연스러우면 영어를 사용합니다.
  - 영어도 부자연스러우면 기본값인 한국어를 사용합니다.
  - standard, specification, product, tool, framework, API, protocol과 같은 표준·기술 명칭은 통용되는 영어 명칭을 사용합니다.
  - 한국어로 번역하거나 음역했을 때 매우 어색하거나 의미가 덜 정확해지는 영어 표현과 단어는 영어를 유지합니다.
- 더 구체적인 `Scope` 규칙이 있으면 해당 규칙을 우선합니다.

## Scope

영역과 경우마다 아래 규칙을 적용합니다. 더 구체적인 `Scope`가 일반 규칙보다 우선합니다.

| Scope | Applies To | Rule |
| --- | --- | --- |
| **General Prose** | 설명, 안내와 근거 같은 일반 서술 | Default |
| **Markdown Heading** | Markdown heading | `H1`~`H3`은 영어, `H4` 이하는 한국어 |
| **Structural Names and Values** | field name, metadata key, identifier, key, option, enum처럼 구조적이거나 기계적으로 해석되는 이름과 값 | 영어 |
| **Descriptive Metadata Values** | `description`, `summary`, `notes`처럼 사람이 읽는 metadata value | 해당 `Scope`의 일반 서술 규칙을 따름 |
| **Agent Assets Used to Manage This Repository** | 이 repository와 **Agent Assets Managed by This Repository**를 생성·수정·검증·관리하기 위해 직접 사용하는 instruction, Skill, Rule, Command, Hook과 지원 자료 | 한국어 중심 |
| **Agent Asset Trigger Frontmatter** | Agent Asset의 선택·활성화를 결정하는 frontmatter의 서술형 trigger value | 영어 |
| **Agent Assets Managed by This Repository** | 이 repository가 생성·관리하는 대상 Agent Asset과 그 source/package content | repository의 한국어 기본값을 강제하지 않고 source framework, target contract, intended audience와 asset-local convention을 따름 |

## Boundary

- Branch, tag, label, field 같은 identifier와 metadata의 구조적 요소는 `Scope`를 따릅니다.
- Code, command, path, filename, literal value와 외부에서 정의된 exact name은 해당 source와 format의 표기를 따릅니다.
- 자동 생성된 메시지나 외부 source에서 보존해야 하는 text는 해당 source의 규칙을 따릅니다.
