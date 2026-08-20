# Template / Schema / Metadata-Driven Assets

자산의 구조를 정의하는 template, schema 또는 metadata에 작성 지침과 제약을 가능한 한 가까이 두어 **더 유연하고 효율적으로 자산을 생성·검증·관리**하는 패턴입니다.

## Purpose

구조 정의와 작성 규칙을 분리된 여러 문서에 반복하기보다 실제 자산 구조를 정의하는 owner 가까이에 배치해 KISS, DRY, SRP를 높입니다.

## Core

- Template은 섹션 구조, 필수 항목, 기본 형태와 작성 의도를 표현할 수 있습니다.
- Schema는 필드 의미, 타입, 제약, 허용값과 validation contract를 표현할 수 있습니다.
- Metadata는 자산의 분류, 선택 기준, 속성과 작성에 필요한 구조화된 정보를 담을 수 있습니다.
- 같은 구조 정보를 여러 곳에 반복하기보다 가장 자연스러운 structural owner에 가깝게 둡니다.

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
- metadata 기반 생성·검증·routing
- template/schema 변경을 감지하는 validation automation

자동화는 패턴의 확장 수단이며 필수 조건은 아닙니다.

## Considerations

- 구조와 가까운 지침일수록 생성자와 validator가 같은 contract를 재사용하기 쉽습니다.
- 너무 많은 prose나 장기 rationale을 schema/metadata에 넣으면 구조 정의 책임이 흐려질 수 있습니다.
- tool이나 format의 표현력이 부족하면 별도 maintainer documentation을 함께 사용할 수 있습니다.
- 단순한 자산에는 template 하나만으로 충분할 수 있고, 복잡한 자산에서는 schema와 metadata를 함께 사용하는 편이 나을 수 있습니다.

## Boundary

이 패턴은 **자산 구조를 정의하고 그 구조를 작성·검증하는 데 직접 필요한 지침과 metadata**를 소유합니다.

자산의 장기 비전, 본질, project-wide policy처럼 구조 정의와 직접 관계없는 내용까지 template/schema/metadata에 넣는 것을 요구하지 않습니다. 또한 특정 schema 언어, metadata 형식, generator 또는 validation tool을 강제하지 않습니다.
