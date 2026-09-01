---
name: mols-documentation
description: >-
  사람이 읽고 유지보수하는 문서를 작성, 재작성하거나 개선한다. README, 가이드,
  정책, 계획, 보고서, 설명 문서 등에서 독자와 목적에 맞게 정보 구조, 명확성,
  가독성, 탐색성과 유지보수성을 개선할 때 사용한다. 기존 문서는 사실, 결정,
  식별자, 제약과 필요한 voice를 보존한다. Markdown 등 표현 surface에 특화된
  규칙은 필요한 reference만 로드한다. deterministic Markdown formatting이나
  validation은 mols-markdown-maintenance, engineering dashboard는
  mols-markdown-dashboard, source-code comments와 docstrings는 mols-clarify-code를
  사용한다.
targets:
  - claudecode
  - codexcli
  - copilot
  - copilotcli
  - antigravity-ide
  - antigravity-cli
  - agentsskills
agentsskills:
  metadata:
    version: "4.0.0"
---

# Documentation

사람이 빠르게 이해하고 다시 찾고 오래 유지할 수 있는 문서를 만든다. 문서의 표현 형식보다 독자, 목적과 정보 구조를 먼저 결정한다.

## Contract

- 독자에게 필요한 판단, 행동과 이해를 기준으로 문서의 역할과 범위를 정한다.
- 기존 문서를 고칠 때는 사실, 결정, 순서, 관계, 식별자, citation, 필요한 불확실성과 프로젝트 고유의 voice를 보존한다.
- 작성자의 탐색 과정보다 독자의 질문과 사용 순서에 맞게 정보를 배치한다.
- 문서 초반에는 목적, 범위와 현재 상태 또는 핵심 결론처럼 독자가 먼저 알아야 할 정보를 보여준다. 절차서, tutorial, reference처럼 순서나 검색성이 더 중요한 문서는 그 목적에 맞는 구조를 우선한다.
- heading, paragraph, list, table, example과 visual은 정보 구조를 더 잘 드러낼 때만 사용한다. 특정 표현 형식의 문법이나 세부 규칙은 해당 reference가 소유한다.
- KISS는 필요한 의미를 줄이는 것이 아니라 이해와 유지보수에 기여하지 않는 복잡성을 제거하는 것이다. DRY는 같은 사실이나 규칙의 설명 owner를 하나로 유지하는 것이다.
- 프로젝트의 명시적 template, style, terminology와 문서 정책이 있으면 이 Skill의 기본값보다 우선한다.
- 원문이나 근거에 없는 사실, 수치, 관계, 확정적 판단을 새로 만들지 않는다.
- 사람이 읽는 agent-facing 문서에도 적용할 수 있지만 human-readable presentation만 다룬다. 행동 계약, activation, authority와 runtime semantics는 해당 자산의 owner가 소유한다.

## References

필요한 표현 surface만 읽는다.

| Need | Reference |
| --- | --- |
| Markdown heading, list, table, code, link, callout, footnote와 Markdown 기반 visual 선택 | [Markdown](references/markdown.md) |

Reference를 읽지 않아도 문서의 독자, 목적, 정보 구조와 내용 판단은 이 본문을 따른다.

## Workflow

1. 독자, 문서의 목적, 독자가 이 문서를 읽은 뒤 알아야 하거나 해야 하는 것을 식별한다.
1. 기존 문서라면 보존해야 할 사실, 결정, 계약, 순서, 관계, 식별자와 voice를 먼저 구분한다.
1. 독자의 주요 질문과 사용 순서를 기준으로 section과 정보 순서를 설계한다.
1. 가장 중요한 내용부터 직접적이고 구체적인 prose로 작성하고 필요한 근거, 예시와 세부 내용을 점진적으로 확장한다.
1. 정보 구조에 맞는 표현을 선택하고, surface-specific 규칙이 결과를 바꾸는 경우에만 해당 reference를 적용한다.
1. 중복, boilerplate, 불필요한 section과 장식을 제거한다.
1. 제목과 heading만 훑어도 문서의 역할과 흐름을 파악할 수 있는지, 필요한 정보를 쉽게 다시 찾을 수 있는지, 보존해야 할 의미가 유지되는지 검토한다.

## Information Architecture

- 제목과 도입부는 문서가 무엇을 위한 것인지 빠르게 알려야 한다.
- section은 작성 순서가 아니라 독자의 질문, 판단, 작업 단계 또는 검색 단위로 나눈다.
- heading은 내용이 무엇인지 예측할 수 있을 만큼 구체적으로 작성한다. 비슷한 의미의 heading을 연속해서 쪼개지 않는다.
- 문서 유형에 맞는 기본 흐름을 선택한다. 결정·상태 문서는 결론 우선, 절차서는 실행 순서, reference는 검색과 비교, 설명 문서는 개념 관계와 이해 순서를 우선한다.
- 핵심에서 세부로 내려가는 progressive disclosure를 사용하되 중요한 제약이나 예외를 독자가 놓칠 위치에 숨기지 않는다.
- 반복해서 비교하는 속성은 묶고, 서로 다른 추상화 수준의 내용을 같은 목록이나 표에 억지로 넣지 않는다.
- 독립적인 의미가 없는 한 줄짜리 section을 연속해서 만들지 않는다.

## Writing

- 문단마다 하나의 중심 내용을 두고 중요한 문장은 가능한 한 앞쪽에 둔다.
- 주체, 행동, 조건, 예외와 결과가 모호하면 명시한다.
- 같은 개념에는 같은 용어를 사용한다. 사용자의 naming과 표준 domain term은 특별한 이유 없이 바꾸지 않는다.
- 독자에게 익숙하지 않을 가능성이 높은 용어는 처음 필요한 위치에서 짧게 설명한다.
- 예시는 규칙이나 추상적 설명만으로 오해하기 쉬울 때 사용한다. 예시가 본문 규칙을 대신하게 하지 않는다.
- 문서명, 자산명이나 주제를 가까운 문장마다 기계적으로 반복하지 않는다. 주어가 분명한 범위에서는 자연스러운 문장 흐름을 우선한다.
- 강조, 장식과 visual은 중요도를 실제로 구분하거나 이해 비용을 줄일 때만 사용한다.

## Editing

- 불필요한 서론, template 문구, 메타 설명과 중복된 요약을 제거한다.
- 같은 사실이나 규칙을 heading, prose, table, callout과 visual에서 반복하지 않는다. 다른 위치에서 다시 필요하면 짧게 연결한다.
- 겹치는 section은 하나의 owner로 통합하고 독립적인 독자 질문이 있을 때만 분리한다.
- 짧게 만드는 과정에서 결정, 근거, 제약, 예외와 필요한 예시를 잃지 않는다.
- 원문의 의미와 voice를 보존해야 하는 작업에서는 가독성 개선을 이유로 기술적 의미나 의도적인 nuance를 바꾸지 않는다.

## Boundary

- deterministic Markdown formatting, lint, frontmatter, link와 index mechanics → `mols-markdown-maintenance`
- engineering progress와 evidence를 집계하는 Markdown dashboard → `mols-markdown-dashboard`
- source file 내부의 comments, docstrings와 declaration documentation → `mols-clarify-code`
- 문서가 사용하는 domain-specific diagram, chart, template 또는 형식의 의미는 해당 전문 owner가 있으면 그 owner가 소유한다.
