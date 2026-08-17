# Chatbot Runtime Skills

`skills-chatbot-runtime/`은 단일 Markdown만으로는 충분하지 않은 hosted chatbot capability를 둡니다.

## Placement

`skills-chatbot-runtime/`은 배포 capability가 다음 중 하나라도 해당할 때 사용합니다.

- flat 단일 skill 파일이 **4,000 tokens 이상**이라 여러 Markdown 파일로 분리해야 합니다.
- Markdown 한 파일만으로 배포 capability의 instruction surface를 완결할 수 없습니다.
- 실행에 `references/`, `assets/`, `scripts/`, images 같은 bundled resources가 필요합니다.
- host-specific tool schema, integration resource, progressive loading, script/runtime package처럼 **단일 Markdown 밖의 runtime surface**가 capability에 필요합니다.

`SKILL.md`는 activation boundary와 공통 계약을 유지하고, 상세 context는 필요한 경우에만 bundled file이나 runtime source에서 로드하는 방식을 우선합니다.

단일 Markdown 파일로 충분하고 4,000 tokens 미만이며 별도 runtime surface가 필요하지 않다면 `../skills-chatbot/`의 flat variant가 더 단순한 기본 선택입니다. Skill이 host가 이미 제공하는 tool이나 connector 사용을 지시한다는 사실만으로 runtime placement를 강제하지 않습니다.

사용자의 로컬/원격 workspace, filesystem, shell 같은 workspace authority가 필요하면 `../skills/` profile도 검토합니다.

## Runtime Resource Rule

Bundled resource는 capability에 실제로 필요할 때만 둡니다.

- `references/`: 조건부 상세 지식
- `assets/`: templates, examples, images 같은 실행/출력 resource
- `scripts/`: deterministic helper나 validation
- host-specific integration/configuration resource

단순한 문서 분할 자체가 목적이 되어서는 안 됩니다. flat file로 더 명확하고 독립적으로 완결되면 flat profile을 우선합니다.

Maintainer-only 파일이 존재한다는 이유만으로 runtime placement를 강제하지 않습니다. tests/evals/development docs를 배포 surface에서 분리할 수 있다면 target profile 판단에서는 제외합니다.

## Naming

주책임이 **상황별 context 로딩**이면 `load-context-<topic>` 이름을 사용합니다. 이 naming은 repository-local convention이며 Agent Skills 표준 요구사항이 아닙니다.

- context-only Skill은 context discovery, selection, scoping, loading과 적용 경계까지만 소유합니다.
- context를 사용한 실제 구현, 작성, 검증, 리뷰, mutation과 최종 output은 downstream capability가 소유합니다.
- 실제 workflow 수행, artifact 생성, validation, transformation이 주책임이면 `load-context-`를 사용하지 않습니다.

Personal context overlay가 필요한 경우 flat profile의 `load-context-<topic>-<owner>` convention을 사용하고, base loader를 대체하지 않습니다.
