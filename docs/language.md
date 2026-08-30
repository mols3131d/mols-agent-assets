---
description: README·docs·comments·Git/GitHub communication과 Agent Asset에서 한국어와 영어를 어떻게 사용할지 판단할 때 적용하는 repository 언어 정책입니다.
---

# Language

이 repository에서는 사람이 읽는 문서·협업 내용과 repository 관리에 직접 사용하는 Agent Asset을 **한국어 중심**으로 작성합니다. 반면 이 repository가 생성·관리하는 대상 Agent Asset에는 한국어 기본값을 강제하지 않습니다.

한국어 중심은 모든 표현을 한국어로 바꾼다는 뜻이 아닙니다. 일반 서술은 한국어로 작성하고, 구조적 이름과 통용되는 기술 명칭은 필요한 영어 표기를 유지합니다. 더 좁은 영역에 별도 언어 규칙이 있으면 그 규칙을 우선합니다.

## Scope

| 영역 | 적용 대상 | 기본 규칙 |
| --- | --- | --- |
| **Documentation** | README, `docs/`와 그 밖의 사람이 읽는 repository 문서 | 한국어 중심 |
| **Comments and Docstrings** | source와 configuration의 주석, 개발자용 docstring | 한국어 중심 |
| **Git** | 사람이 작성하는 commit subject와 body | 한국어 중심 |
| **GitHub** | 사람이 작성하는 PR, issue, discussion, review, comment와 release note | 한국어 중심 |
| **Agent Assets Used to Manage This Repository** | 이 repository와 **Agent Assets Managed by This Repository**를 생성·수정·검증·관리하기 위해 직접 사용하는 instruction, Skill, Rule, Command, Hook과 지원 자료 | 한국어 중심 |
| **Agent Asset Trigger Frontmatter** | Agent Asset의 선택·활성화를 결정하는 trigger 역할의 frontmatter value | 영어 |
| **Agent Assets Managed by This Repository** | 이 repository가 생성·관리하는 대상 Agent Asset과 그 source/package content | repository의 한국어 기본값을 강제하지 않음 |

**Agent Assets Managed by This Repository**의 Skill, Rule, Command, Hook, agent instruction, runtime resource, template, script, schema와 target-specific content는 source framework, target contract, intended audience와 asset-local convention을 따릅니다.

## Mixing Rules

다음 규칙은 한국어 중심 영역에 적용합니다.

| 종류 | 규칙 |
| --- | --- |
| **일반 서술** | 설명, 안내와 근거는 한국어로 작성합니다. 자연스러운 한국어가 있는 일반 문장을 불필요하게 영어로 바꾸지 않습니다. |
| **Heading** | Markdown heading은 `H1`~`H3`까지 영어로 작성하고, `H4` 이하부터 한국어로 작성합니다. |
| **구조적 이름과 값** | field name, metadata key, identifier, key, option, enum처럼 구조적이거나 기계적으로 해석되는 이름과 값은 영어를 사용합니다. |
| **서술형 metadata value** | `description`, `summary`, `notes`처럼 사람이 읽는 값은 일반 서술과 같은 언어 규칙을 적용합니다. 단, Agent Asset의 선택·활성화를 결정하는 trigger 역할의 frontmatter value는 `Scope`에 따라 영어로 작성합니다. |
| **표준·기술 명칭** | standard, specification, product, tool, framework, API, protocol과 같은 명칭은 통용되는 영어 명칭을 사용합니다. |
| **번역이 부자연스럽거나 부정확한 표현** | 한국어로 번역하거나 음역했을 때 매우 어색하거나 의미가 덜 정확해지는 영어 표현과 단어는 영어를 유지합니다. |

## Boundary

- Branch, tag, label, field 같은 identifier와 metadata의 구조적 요소는 `Mixing Rules`를 따릅니다.
- Code, command, path, filename, literal value와 외부에서 정의된 exact name은 해당 source와 format의 표기를 따릅니다.
- 자동 생성된 메시지나 외부 source에서 보존해야 하는 text는 해당 source의 규칙을 따릅니다.
