---
name: mols-documentation
description: >-
  README, 가이드, 정책, 계획, 보고서, 설명 문서 등 사람이 읽고 유지보수하는 문서를
  새로 작성하거나 구조, 내용, 가독성을 개선할 때 사용한다. 문서의 목적, 독자,
  정보 구조, 탐색성, 신뢰성, ownership 또는 유지보수성이 주된 문제일 때 선택한다.
  단순 Markdown formatting이나 lint, engineering dashboard, source-code comment나
  docstring, 이메일·메시지·소셜 문구 또는 문체만 윤문하는 작업에는 사용하지 않는다.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
---

# Mols Documentation

사람이 읽고 유지보수하는 문서를 새로 작성하거나 개선한다.

# Contract

- 문서는 독자가 필요한 정보를 `찾고`, `이해하고`, `판단하고`, `행동`할 수 있게 해야 한다.
- 범위와 순서는 독자가 실제로 묻는 질문과 수행해야 하는 행동에서 정한다.
- 사람과 LLM 모두에게 불필요한 탐색·추론·검증·실행 비용을 줄이되, 인간 독자의 이해 가능성을 희생하지 않는다.
- 가장 좁은 책임을 가진 문서를 선호한다. 파일이나 디렉터리가 존재한다는 이유만으로 문서를 만들지 않는다.
- 하나의 의미에는 하나의 canonical owner를 둔다. 다른 문서는 링크나 짧은 맥락만 제공한다.
- 사실, 결정, 근거, 불확실성과 현재 상태를 구분해 독자가 신뢰 수준을 판단할 수 있게 한다.
- 기존 문서를 편집할 때는 사실, 결정, 순서, 관계, 식별자, 인용, 불확실성과 필요한 project voice를 보존한다. 보존 자체가 주된 제약이면 `technical-document-fidelity`를 함께 적용한다.
- 명시적인 사용자 지시와 project template, terminology, style, policy가 이 Skill의 기본값보다 우선한다.
- 확인되지 않은 사실, 수치, 관계나 결론을 만들지 않는다.
- agent-facing human-readable 문서에도 표현과 구조 원칙만 적용한다. behavior contract, activation, authority, runtime semantics는 해당 Agent Asset owner가 소유한다.

# References

조건에 맞는 reference만 추가로 읽는다.

- Markdown surface를 작성하거나 편집하면 [Markdown](references/markdown.md)을 읽는다.
- README, 디렉터리·문서 번들 진입점, 온보딩 첫 화면처럼 독자의 첫 탐색과 다음 행동을 안내하는 entrypoint 문서를 다루면 [Entrypoint](references/entrypoint.md)를 읽는다.

# Workflow

1. 독자와 문서의 목적, 읽은 뒤 기대되는 판단이나 행동을 정한다.
1. 기존 문서라면 보존해야 할 사실, 결정, 관계, 식별자, 링크, 불확실성과 voice를 먼저 확인한다.
1. 문서가 소유해야 할 의미와 다른 canonical owner로 넘길 내용을 구분한다.
1. 독자의 질문 순서에 맞게 섹션을 배치하고 중요한 내용을 먼저 둔다.
1. 가능한 한 직접적인 prose를 쓰고, 목록·표·코드·시각 요소는 실제 탐색이나 비교 비용을 줄일 때만 사용한다.
1. surface나 문서 역할에 특화된 규칙이 필요하면 해당 reference만 읽는다.
1. 중복 설명, 상투적 서론, 수동 동기화 부담, 불필요한 navigation과 boilerplate를 줄인다.
1. 독자가 핵심을 찾고 다음 행동을 결정할 수 있는지, 사실과 ownership이 신뢰 가능한지, 유지보수 부담이 과하지 않은지 다시 확인한다.

# Information Architecture

- 문서 구조는 source 구조가 아니라 독자의 질문 구조를 따른다.
- 핵심 결론, 상태, 결정이나 첫 행동은 가능한 한 앞에 둔다.
- 한 섹션은 하나의 질문이나 책임을 중심으로 구성한다.
- 세부사항이 다른 canonical 문서에 있으면 복제하지 말고 필요한 맥락과 링크만 제공한다.
- 장기적으로 함께 변하지 않는 내용을 억지로 한 문서에 묶지 않는다.

# Trust and Ownership

- 현재 사실과 과거 결정, 계획, 제안, 예시를 혼동하지 않는다.
- 불확실하거나 검증되지 않은 내용은 그 상태를 드러낸다.
- 유지보수 책임이 다른 내용은 해당 owner로 연결한다.
- 자동 생성되거나 다른 source에서 파생되는 정보는 손으로 복제하지 않는다.

# Navigation and Maintenance

- 독자가 다음에 읽거나 해야 할 것이 있을 때만 navigation을 추가한다.
- 파일 목록, 목차, 상태 표나 링크 모음은 실제 탐색 비용을 줄일 때만 둔다.
- 자주 바뀌는 정보를 여러 곳에 복제하지 않는다.
- 문서 구조가 실제 repository, product, process 구조와 어긋나면 문서만으로 가리지 말고 ownership 문제를 드러낸다.

# Writing

- 자연스러운 문단을 우선하고 한 문장을 억지로 여러 줄로 쪼개지 않는다.
- 핵심 의미를 먼저 말하고 배경은 필요한 만큼만 뒤에 둔다.
- 추상적인 품질 표현보다 독자가 확인하거나 수행할 수 있는 구체적인 설명을 쓴다.
- 같은 개념에는 같은 용어를 사용한다.
- 의미를 더하지 않는 수식어, 반복, 메타 설명을 줄인다.

# Editing

- 구조 개선을 이유로 의미를 바꾸지 않는다.
- 오래된 문구를 최신 사실처럼 재해석하지 않는다.
- 중복을 제거할 때는 canonical owner를 분명히 남긴다.
- 문서의 기존 voice가 의미 전달이나 project consistency에 필요하면 보존한다.
- 더 짧게 만드는 것보다 독자가 더 적은 비용으로 올바르게 이해하고 행동할 수 있는지를 우선한다.

# Boundary

- deterministic Markdown formatting, lint, frontmatter, link, heading, index 검증은 `mols-markdown-maintenance`가 소유한다.
- engineering dashboard는 `mols-markdown-dashboard`가 소유한다.
- source-code comment와 docstring은 `mols-clarify-code`가 소유한다.
- 기존 기술 문서의 의미·식별자·코드·URL 보존이 주된 제약이면 `technical-document-fidelity`를 함께 적용한다.
- 도메인 전용 diagram, chart, template semantics는 해당 전문 Skill이나 project owner를 따른다.
