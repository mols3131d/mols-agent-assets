---
description: README·docs·comments·Git/GitHub communication과 Agent Asset에서 한국어와 영어를 어떻게 사용할지 판단할 때 적용하는 repository 언어 정책입니다.
---

# Language

- 이 저장소의 기본 언어는 한국어입니다.
- 한국어 표현이 어색하면 자연스러운 영어를 사용합니다.
  - 번역하면 어색하거나 뜻이 흐려지는 표현은 영어를 유지합니다.
  - 한국에서 널리 쓰이는 기술 용어나 고유 명칭은 영어를 그대로 사용합니다.
  - 영어도 어색하면 기본값인 한국어를 사용합니다.
- 더 구체적인 `Scope`가 있으면 해당 규칙을 우선합니다.

## Scope

영역별 언어는 아래와 같습니다.

| Scope | Description | Language |
| --- | --- | --- |
| **General Prose** | 설명, 안내, 근거 등 일반 서술 | Default |
| **Markdown Headings H1–H3** | `H1`~`H3` heading | 영어 |
| **Markdown Headings H4–H6** | `H4`~`H6` heading | Default |
| **Structural Names and Values** | field name, metadata key, identifier 등 구조적이거나 기계적으로 해석되는 이름과 값 | 영어 |
| **Descriptive Metadata Values** | `description`, `summary`, `notes` 등 사람이 읽는 metadata value | Default |
| **Agent Assets Used to Manage This Repository** | 이 repository와 관리 대상 Agent Asset을 생성·수정·검증하는 데 사용하는 Agent Asset과 지원 자료 | Default |
| **Agent Asset Trigger Frontmatter** | Agent Asset의 선택·활성화를 결정하는 frontmatter의 서술형 trigger value | 영어 |

## Non-Scope

Non-Scope는 해당 대상의 언어와 표기 규칙을 따릅니다.

| Non-Scope | Description |
| --- | --- |
| **Agent Assets Managed by This Repository** | 이 repository가 생성·관리하는 Agent Asset과 source/package content |
| **Framework, Tool, and Technology Conventions** | framework, tool, technology의 언어·표기 규칙이 적용되는 content |
| **Exact and Literal Values** | code, command, path, filename, literal value, 외부에서 정의된 exact name |
| **Generated or Preserved Text** | 자동 생성된 message와 외부 source에서 보존해야 하는 text |
