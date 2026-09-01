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
  - agentsskills
agentsskills:
  metadata:
    version: "4.0.0"
---

# Documentation

좋은 문서는 독자가 필요한 정보를 **찾고, 이해하고, 판단하고, 행동**하게 한다. 이 Skill은 표현 형식보다 독자, 목적, 정보 구조, 신뢰성과 유지보수 비용을 먼저 다룬다.

## Contract

- 작성자가 설명하고 싶은 순서보다 독자가 풀어야 할 질문, 내려야 할 판단과 해야 할 행동을 기준으로 문서의 역할과 범위를 정한다.
- 독자는 필요한 내용을 적은 부담으로 찾고 이해할 수 있어야 하며, 중요한 의미를 특정 표현 방식이나 도구에만 의존하게 만들지 않는다. LLM이나 AI Agent도 독자라면 맥락·탐색·추론·검증·실행 비용을 줄이되 사람을 위한 문서 품질을 희생하지 않는다.
- 문서마다 주된 책임을 분명히 하고 그 책임을 맡을 수 있는 가장 좁은 범위에 둔다. 파일이나 디렉터리가 있다는 이유만으로 문서를 만들지 않는다.
- 하나의 범위에서 같은 의미를 설명하는 canonical owner는 하나로 유지한다. 다른 문서는 필요한 안내, 링크와 짧은 맥락만 제공하고 같은 규칙을 다시 정의하지 않는다.
- 사실, 결정, 근거, 불확실성과 현재 상태를 구분한다. 오래된 상태나 추측을 현재의 사실이나 지침처럼 표현하지 않는다.
- 기존 문서를 고칠 때는 사실, 결정, 절차·우선순위·연대처럼 의미를 갖는 순서, 관계, 식별자, citation, quotation, 필요한 불확실성과 프로젝트 고유의 voice를 보존한다. 기술 문서의 보존 제약이 주된 요구면 `technical-document-fidelity`를 함께 적용한다.
- 사용자와 프로젝트의 명시적 template, terminology, style, 형식과 문서 정책이 있으면 이 Skill의 기본값보다 우선한다.
- 원문이나 근거에 없는 사실, 수치, 관계, 확정적 판단을 새로 만들지 않는다.
- 사람이 읽는 agent-facing 문서에도 적용할 수 있지만 human-readable presentation과 문서 구조만 다룬다. 행동 계약, activation, authority와 runtime semantics는 해당 자산의 owner가 소유한다.

## References

결과를 실제로 바꾸는 경우에만 필요한 reference를 읽는다.

| Need | Reference |
| --- | --- |
| Markdown heading, list, table, code, link, metadata, callout, footnote와 Markdown 기반 visual 선택 | [Markdown](references/markdown.md) |
| README, 디렉터리·문서 묶음의 진입점, 온보딩 첫 화면 등 entrypoint 문서 작성·개선 | [Entrypoint](references/entrypoint.md) |

Reference를 읽지 않아도 독자, 목적, 정보 구조, 신뢰성, ownership과 내용 판단은 이 본문을 따른다.

## Workflow

1. 독자, 문서의 목적, 독자가 읽은 뒤 알아야 하거나 판단하고 행동해야 하는 것을 식별한다.
1. 기존 문서라면 보존해야 할 사실, 결정, 계약, 절차·우선순위·연대처럼 의미를 갖는 순서, 관계, 식별자, citation, quotation, 근거와 voice를 먼저 구분한다.
1. 문서의 주된 책임과 canonical boundary를 정하고, 이미 더 적절한 owner가 있는 내용은 복제하지 않고 연결한다.
1. 독자의 주요 질문과 사용 순서를 기준으로 section과 정보 순서를 설계한다.
1. 가장 중요한 내용부터 직접적이고 구체적인 prose로 작성하고 필요한 근거, 예시와 세부 내용을 점진적으로 확장한다.
1. 정보 구조에 맞는 표현을 선택하고, surface나 문서 유형에 특화된 규칙이 결과를 바꾸는 경우에만 해당 reference를 적용한다.
1. 중복, boilerplate, 불필요한 section, navigation과 장식을 제거한다.
1. 문서가 찾기 쉽고 다음 정보나 행동으로 자연스럽게 이어지는지, 현재 상태를 신뢰할 수 있는지, 이후 수정 비용이 불필요하게 커지지 않는지 검토한다.

## Information Architecture

- 제목과 도입부는 문서가 무엇을 위한 것인지 빠르게 알려야 한다.
- 중요한 결론, 조건, 현재 상태와 다음 판단에 필요한 내용을 먼저 둔다. 절차서, tutorial, reference처럼 실행 순서나 검색성이 더 중요한 문서는 그 목적에 맞는 구조를 우선한다.
- section은 작성 순서가 아니라 독자의 질문, 판단, 작업 단계 또는 검색 단위로 나눈다.
- heading은 내용을 예측할 수 있을 만큼 구체적으로 작성한다. 비슷한 의미의 heading을 연속해서 쪼개지 않는다.
- 핵심에서 세부로 내려가는 progressive disclosure를 사용하되 중요한 제약이나 예외를 독자가 놓칠 위치에 숨기지 않는다.
- 반복해서 비교하는 속성은 묶고, 서로 다른 추상화 수준의 내용을 같은 목록이나 표에 억지로 넣지 않는다.
- 독립적인 의미가 없는 한 줄짜리 section을 연속해서 만들지 않는다.

## Trust and Ownership

- 현재 상태를 설명한다면 freshness를 확인할 수 있는 근거를 유지한다. 확인하지 못한 내용은 추측으로 채우지 않는다.
- 사실, 결정, 해석과 불확실성이 섞여 독자가 같은 수준의 확실성으로 읽지 않게 한다.
- 쉽게 다시 생성하거나 source에서 계산할 수 있는 목록과 파생 정보는 사람이 유지하는 canonical 지식으로 복제하지 않는다.
- maintainer를 위한 문서는 의도, 중요한 제약, 쉽게 알 수 없는 결정과 복구에 필요한 맥락을 보존하되 실행 가능한 원본이나 계약의 복사본이 되지 않게 한다.

## Navigation and Maintenance

- 독자가 문서를 발견하고 다른 후보와 구분해 선택할 수 있게 제목, 설명, 링크와 배치를 설계한다.
- 읽은 뒤 필요한 다음 정보나 행동이 있으면 자연스럽게 연결한다. 중요한 지식을 우연히 발견해야만 알 수 있게 숨기지 않는다.
- index, table of contents, navigation list 같은 탐색 장치는 실제 탐색 비용을 낮출 때만 추가한다.
- 사람이 선택 판단을 위해 관리하는 navigation과 도구가 다시 만들 수 있는 inventory를 구분하고 같은 정보를 반복하지 않는다.
- 문서를 추가하거나 구조를 나눌 때는 작성 비용뿐 아니라 이후 갱신, 이동, 이름 변경과 stale 상태를 관리할 비용도 고려한다.

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

- deterministic Markdown formatting, lint, frontmatter schema, link와 index mechanics → `mols-markdown-maintenance`
- engineering progress와 evidence를 집계하는 Markdown dashboard → `mols-markdown-dashboard`
- source file 내부의 comments, docstrings와 declaration documentation → `mols-clarify-code`
- 기술 문서 변환에서 protected content 보존 제약 → `technical-document-fidelity`
- 문서가 사용하는 domain-specific diagram, chart, template 또는 형식의 의미는 해당 전문 owner가 있으면 그 owner가 소유한다.
