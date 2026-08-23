---
description: repository communication과 Agent Asset 역할별 언어 정책을 정의합니다.
---

# Language

이 repository의 언어는 **영역과 역할에 따라 정합니다**.

사람이 읽는 일반 서술과 협업 내용은 한국어를 기본으로 하고, 구조적 이름과 통용되는 기술 명칭은 영어를 유지합니다. 다만 이 repository가 생성·관리하는 대상 Agent Asset에는 repository의 한국어 기본값을 강제하지 않습니다.

더 좁은 영역에 별도 언어 규칙이 있으면 해당 규칙을 따릅니다.

## At a Glance

| 대상 | 언어 원칙 |
| --- | --- |
| 이 repository를 개발·운영하기 위한 문서와 협업 | 한국어 중심 |
| 이 repository와 관리 대상 Agent Asset을 직접 관리하는 작업용 Agent Asset | 한국어 중심 |
| 구조적이거나 기계적으로 해석되는 이름과 값 | 영어 |
| 이 repository가 생성·관리하는 대상 Agent Asset | 해당 source framework, target contract, intended audience와 asset-local convention |

## Korean-Centered Surfaces

다음 영역은 **한국어 중심**으로 작성합니다.

- **Documentation** — README, `docs/`와 그 밖의 사람이 읽는 repository 문서
- **Comments and Docstrings** — source와 configuration의 주석, 개발자용 docstring
- **Git** — 사람이 작성하는 commit subject와 body
- **GitHub** — 사람이 작성하는 PR, issue, discussion, review, comment와 release note
- **Agent Assets Used to Manage This Repository** — 이 repository와 **Agent Assets Managed by This Repository**를 생성·수정·검증·관리하기 위해 직접 사용하는 instruction, Skill, Rule, Command, Hook과 지원 자료

## Mixing Rules

한국어를 기본 서술 언어로 사용하되, 구조적 이름과 표준·기술 명칭은 필요한 영어 표기를 유지합니다.

- **일반 서술** — 설명, 안내와 근거는 한국어로 작성합니다.
- **구조적 이름과 값** — field name, heading, metadata key, identifier, key, option, enum처럼 구조적이거나 기계적으로 해석되는 이름과 값은 영어를 사용합니다.
- **서술형 metadata value** — `description`, `summary`, `notes`처럼 사람이 읽는 값은 일반 서술과 같은 언어 규칙을 적용합니다.
- **표준·기술 명칭** — standard, specification, product, tool, framework, API, protocol과 같은 명칭은 통용되는 영어 명칭을 사용합니다.
- **번역이 부자연스럽거나 부정확한 표현** — 한국어로 번역하거나 음역했을 때 매우 어색하거나 의미가 덜 정확해지는 영어 표현과 단어는 영어를 유지합니다.
- **자연스러운 한국어가 있는 일반 문장** — 불필요하게 영어로 바꾸지 않습니다.

## Agent Asset Roles

Agent Asset의 언어 규칙은 이 repository에서 맡는 역할에 따라 다릅니다.

| 역할 | 의미 | 언어 원칙 |
| --- | --- | --- |
| **Agent Assets Used to Manage This Repository** | 이 repository와 관리 대상 Agent Asset을 생성·수정·검증·관리하기 위해 직접 사용하는 도구성 자산 | 한국어 중심 |
| **Agent Assets Managed by This Repository** | 이 repository가 생성·관리하는 대상 Agent Asset | repository의 한국어 기본값을 강제하지 않음 |

**Agent Assets Managed by This Repository**와 그 source/package content는 source framework, target contract, intended audience와 asset-local convention을 따릅니다. 여기에는 Skill, Rule, Command, Hook, agent instruction, runtime resource, template, script, schema와 target-specific content가 포함됩니다.

## Boundary

- Branch, tag, label, field 같은 identifier와 metadata의 구조적 요소는 `Mixing Rules`를 따릅니다.
- Code, command, path, filename, literal value와 외부에서 정의된 exact name은 해당 source와 format의 표기를 따릅니다.
- 자동 생성된 메시지나 외부 source에서 보존해야 하는 text는 해당 source의 규칙을 따릅니다.
