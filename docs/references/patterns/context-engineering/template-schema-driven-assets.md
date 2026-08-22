---
description: Template, schema 또는 metadata를 structural owner로 사용해 생성·검증 가능한 자산 구조를 설계할 때 참고하는 reusable pattern입니다.
---

# Template / Schema / Metadata-Driven Assets

자산의 구조를 정의하는 template, schema 또는 metadata에 작성 지침과 제약을 가능한 한 가까이 두어 **더 유연하고 효율적으로 자산을 생성·검증·관리**하는 패턴입니다.

## Purpose

구조 정의와 작성 규칙을 분리된 여러 문서에 반복하기보다 실제 자산 구조를 정의하는 owner 가까이에 배치해 KISS, DRY, SRP를 높입니다.

## Core

- Template은 섹션 구조, 필수 항목, 기본 형태와 작성 의도를 표현할 수 있습니다.
- Schema는 필드 의미, 타입, 제약, 허용값과 validation contract를 표현할 수 있습니다.
- Metadata는 자산의 분류, 선택 기준, 속성과 작성에 필요한 구조화된 정보를 담을 수 있습니다.
- 같은 구조 정보를 여러 곳에 반복하기보다 가장 자연스러운 structural owner에 가깝게 둡니다.

## Template Contract

Template을 생성 contract로 사용할 때는 **고정 구조와 작성 가능한 영역의 경계**가 복원 가능해야 합니다.

- 고정 heading, policy text, frontmatter key처럼 template이 소유하는 구조는 consumer가 임의로 다시 설계하지 않습니다.
- Variable area는 placeholder, slot, block, field description 등 해당 format에 맞는 명시적 mechanism으로 구분합니다.
- 각 variable area의 의미, required/optional 여부와 omission rule은 template 자체 또는 가장 가까운 structural metadata에서 찾을 수 있어야 합니다.
- 다른 runtime이나 tool이 소유하는 reserved placeholder가 있다면 agent-owned writable area와 구분합니다.
- 생성자는 선언된 writable area만 채우고, 고정 구조나 reserved value를 변경해야 한다면 template 자체 변경으로 취급합니다.
- 한 문서 instance마다 달라지는 사실은 fixed content로 박아 넣지 않고 variable area나 별도 input owner가 소유하게 합니다.
- Variable area는 의미 있는 단위로 두고 sentence fragment 수준의 과분할을 피합니다.

Placeholder 문법이나 boundary marker는 pattern의 본질이 아닙니다. Repository와 tool은 이미 가진 template engine, schema language 또는 metadata convention을 사용할 수 있습니다.

## Generation and Validation

Template/schema/metadata를 실제 생성에 사용할 때는 같은 structural contract를 validation에도 재사용하는 편이 좋습니다.

일반적인 흐름은 다음과 같습니다.

1. 현재 작업에 적용할 structural owner를 선택합니다.
1. Fixed structure, writable area와 required/optional constraint를 해석합니다.
1. 근거 있는 입력만 writable area에 채웁니다.
1. Optional area는 contract가 허용할 때만 생략합니다.
1. Fixed structure와 reserved value가 보존됐는지 확인합니다.
1. Required value, unresolved placeholder, type 또는 schema violation을 검증합니다.

Template selection이 필요한 경우 exact user choice, explicit metadata binding, uniquely applicable template처럼 **더 강한 applicability evidence를 우선**하고 동등한 후보를 임의 선택하지 않습니다.

Generator와 validator가 같은 structural owner를 사용하면 별도 prose contract나 독립적인 shape parser를 중복 구현하는 비용을 줄일 수 있습니다. 다만 tool이 표현하지 못하는 semantic quality까지 구조 검증만으로 증명했다고 간주하지 않습니다.

## Typical Options

- Markdown template의 heading, placeholder, inline guidance
- YAML/JSON schema의 field description, constraint, enum
- Markdown frontmatter나 manifest의 metadata contract
- template/schema/metadata를 재사용하는 generator와 validator
- project에 맞는 custom schema나 metadata file

이 중 필요한 방식만 선택하거나 함께 사용할 수 있습니다.

## Extensions

규모와 도구 지원에 따라 다음처럼 확장할 수 있습니다.

- 공통 template과 specialized template의 조합
- schema composition이나 reusable definition
- metadata를 생성·검증 또는 다른 tooling에서 재사용
- template/schema 변경을 감지하는 validation automation

자동화는 패턴의 확장 수단이며 필수 조건은 아닙니다.

## Considerations

- 구조와 가까운 지침일수록 생성자와 validator가 같은 contract를 재사용하기 쉽습니다.
- 너무 많은 prose나 장기 rationale을 schema/metadata에 넣으면 구조 정의 책임이 흐려질 수 있습니다.
- tool이나 format의 표현력이 부족하면 별도 maintainer documentation을 함께 사용할 수 있습니다.
- 단순한 자산에는 template 하나만으로 충분할 수 있고, 복잡한 자산에서는 schema와 metadata를 함께 사용하는 편이 나을 수 있습니다.
- 사실상 같은 목적과 applicability를 가진 template을 여러 개 유지하면 selection ambiguity와 drift가 늘어날 수 있으므로 구분 가능한 책임이 있을 때만 분리합니다.
- Formatting, linting, hook, deployment처럼 structural contract 자체가 아닌 동작은 특별한 이유가 없으면 해당 tool/config owner가 소유하고 template에 중복하지 않습니다.
- Template 자체가 특정 repository path, placeholder syntax 또는 tool integration을 요구한다면 그것은 generic pattern이 아니라 해당 implementation owner가 소유할 수 있습니다.

## Boundary

이 패턴은 **자산 구조를 정의하고 그 구조를 작성·검증하는 데 직접 필요한 지침과 metadata**를 소유합니다.

자산의 장기 비전, 본질, project-wide policy처럼 구조 정의와 직접 관계없는 내용까지 template/schema/metadata에 넣는 것을 요구하지 않습니다. 또한 특정 schema 언어, metadata 형식, placeholder 문법, generator, validation tool 또는 template directory를 강제하지 않습니다.
