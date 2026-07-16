# 스킬 프론트매터 (Skill Frontmatter)

에이전트 스킬의 프론트매터 사양입니다.

## Fields (필드 목록)

### `name`

- **형식 (Format)**: 소문자 케밥 케이스(kebab-case)를 사용하며, 스킬 폴더 이름과 완전히 일치시킵니다.
- **길이 (Length)**: 최대 64자 이하.

### `description`

- **내용 (Content)**: 스킬의 전체적인 기능(Capability), 활성화 상황(Activation Contexts), 및 명시적 제외 사항(Exclusions)을 명확하게 작성합니다.
- **길이 (Length)**: 최대 1024자 이하.

## Rules (규칙)

- 타겟 에이전트 클라이언트가 추가 요구사항을 가지지 않는 한, 오직 `name`과 `description` 필드만 작성하십시오.
