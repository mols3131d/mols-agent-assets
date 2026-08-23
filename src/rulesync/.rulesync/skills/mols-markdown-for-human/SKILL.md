---
name: mols-markdown-for-human
description: >
  빠르고 쉽게 사람이 읽을 수 있는 Markdown 문서를 생성하거나 개선한다.
  핵심을 먼저 보여주고 문서의 정보 구조에 맞는 Markdown 표현을 선택한다.
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
    version: "3.1.1"
---

# Markdown for Human

## Purpose

빠르고 쉽게 사람이 읽을 수 있는 Markdown 문서를 생성하거나 개선한다.
독자가 핵심을 빠르게 파악하고 필요한 정보를 쉽게 다시 찾도록 만든다.
사용자와 프로젝트의 명시적인 스타일 선호를 우선한다.

사람 전용 문서뿐 아니라 사람이 읽고 유지보수하는 agent-facing Markdown에도 적용하되, human-readable presentation만 담당한다. 행동 계약, activation과 authority는 해당 자산의 owner가 소유한다.

## Scope

이 skill은 BLUF, heading, prose, list, table, semantic emoji, callout, footnote, text bar와 단일 부모 계층의 tree structure를 담당한다.
복잡한 관계·흐름·상태, 정량 시각화와 개발 dashboard는 독립 skill의 책임이며 선택 기준은 `Visual Routing`을 따른다.
독립 skill의 세부 문법과 규칙은 이 package에 복제하지 않는다.

## References

필요한 경우에만 읽는다.

| Need | Reference |
| --- | --- |
| 상태, 위험, 행동과 category의 빠른 구분 | [Semantic Markers](references/semantic-markers.md) |
| 완료율 또는 소수 category의 단일 수치 비교 | [Text Bars](references/text-bars.md) |
| 파일, module, section 또는 ownership의 단일 부모 계층 | [Tree Structures](references/tree-structures.md) |

## Workflow

1. 독자, 목적, 핵심 결론과 다음 행동 중 결과를 바꾸는 정보를 확인한다. 배경과 reading surface 제약은 필요할 때만 반영한다.
1. 기존 문서라면 보존해야 할 사실, 결정, 순서, 관계, 식별자와 voice를 구분한다.
1. 결론과 중요한 상태를 먼저 배치한다.
1. heading과 section을 구성한다.
1. 정보 구조에 맞는 가장 이해하기 쉬운 표현을 선택한다.
1. KISS와 DRY에 따라 불필요한 복잡성과 중복을 제거한다.
1. source와 rendered view에서 의미가 유지되는지 확인한다.

## Writing Structure

- 문서와 section의 첫 부분에 결론, 상태, 결정 또는 핵심 수치를 둔다.
- 정보는 `결론 → 핵심 근거 → 세부 내용 → 참고 자료` 순서로 확장한다.
- 저자의 작성·탐색 순서보다 독자의 질문, 판단과 다음 행동에 맞춰 구조화한다.
- heading만 훑어도 흐름을 이해할 수 있게 구체적으로 작성한다.
- heading depth는 얕게 유지하고 한 줄짜리 section을 연속해서 만들지 않는다.
- 한 문단에는 하나의 핵심만 두고 첫 문장에 결론을 배치한다.
- list 항목은 같은 추상화 수준과 문법 형태를 유지한다.
- 긴 list는 category, priority 또는 상태로 나눈다.
- code, command, path와 field name은 inline code로 표시한다.
- 사용자가 선호하면 의미 있는 emoji를 heading과 주요 section에 적극 사용한다.

## Visual Routing

| Information | Expression |
| --- | --- |
| 짧은 상태, 위험, 행동, category | Semantic emoji |
| 반복되는 속성, 선택지, 변경 전후 | Markdown table |
| 현재값 / 전체값 | Progress bar |
| 소수 category의 단일 수치 | Horizontal bar |
| 단일 부모 hierarchy | Tree structure |
| 핵심 안내, 팁, 경고 | Callout |
| 복잡한 관계·흐름·상태 | `mols-mermaid-diagram` |
| 정량 비교·추세·분포 | `mols-mermaid-chart` |
| 개발 현황, 위험, blocker와 next action의 통합 뷰 | `mols-markdown-dashboard` |
| 출처와 부가 설명 | Footnote 또는 References |

짧은 prose나 list가 더 빠르게 읽히면 visual을 추가하지 않는다.
시각화가 이해 비용을 줄이거나 사용자가 선호하면 적극 사용한다.

## Markdown Elements

### Semantic Emojis

Emoji는 장식이 아니라 scan marker로 사용한다.
반복되는 상태·위험·행동·category는 [Semantic Markers](references/semantic-markers.md)를 따른다.
Text label을 함께 사용하고 같은 marker에는 같은 의미를 부여한다.

### Tables

비교 가능한 반복 구조에 사용한다. 절차, 긴 서술과 서로 다른 구조의 항목에는 list나 section을 사용한다.

### Text Bars and Trees

진행률과 작은 범주 비교에는 [Text Bars](references/text-bars.md)를 따른다.
하나의 parent를 가진 hierarchy에는 [Tree Structures](references/tree-structures.md)를 따른다.
범위를 벗어나는 시각화 선택은 `Visual Routing`을 따른다.

### Callouts

GitHub target에서는 `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`을 사용할 수 있다.
첫 문장만 읽어도 의미가 전달되어야 하며 일반 section container로 남용하지 않는다.

### Footnotes

본문 흐름을 끊는 출처, 용어 설명, 예외와 부가 기술 설명에 사용한다.

```markdown
핵심 내용에는 근거를 연결한다.[^source]

[^source]: 출처 또는 본문 밖에 둘 보충 설명.
```

- 핵심 결론, 필수 절차와 중요한 제약을 footnote에 숨기지 않는다.
- 같은 출처나 설명을 반복하지 말고 하나의 footnote로 연결한다.
- 지원되지 않는 환경에서는 짧은 `References` section을 사용한다.

## Editing Rules

문서를 **KISS**와 **DRY**하게 작성하거나 개선한다.

- KISS는 문서 길이, section 수, 구조나 단계 수를 줄이는 목표가 아니다. 필요한 의미, 정보 구조와 제약을 유지하면서 이해와 유지보수에 기여하지 않는 복잡성만 제거한다.
- 직접적이고 이해하기 쉬운 표현을 선택한다.
- 불필요한 section, 장식, template 문구와 형식적 서론을 제거한다.
- 짧은 prose나 list로 충분하면 table이나 visual을 만들지 않는다.
- 결정, 근거, 제약과 필요한 예시는 길이를 줄이기 위해 희생하지 않는다.
- 하나의 사실이나 규칙은 가장 적절한 한 곳에서만 설명한다.
- 같은 내용을 heading, prose, table, callout과 visual에서 반복하지 않는다.
- 겹치는 section을 통합하고 다른 위치에서는 링크나 짧은 참조를 사용한다.
- 같은 개념에는 같은 용어를 사용한다. 사용자의 용어와 naming, 표준 domain term은 보존하고 독자에게 필요할 때만 설명한다.
- 주체, 행동, 조건, 예외와 결과가 모호할 때는 이를 명시한다.
- 기존 자료의 사실, citation, quotation, identifier, 필요한 불확실성과 nuance를 보존하고 사용자 의도와 voice를 유지한다. 원문에 없는 사실, 수치, 판단과 관계를 추가하지 않는다.
- 유용한 visual은 보존하고 예시를 복사하기보다 실제 정보 구조를 먼저 판단한다.
