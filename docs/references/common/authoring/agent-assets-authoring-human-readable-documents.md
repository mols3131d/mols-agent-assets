---
title: Human-Readable Documents
description: 사람이 에이전트 자산과 관련 문서를 빠르게 탐색하고 판단할 수 있도록 Markdown 구조를 작성하는 원칙
---

# Human-Readable Documents

사람용 문서는 모든 내용을 설명하는 것이 아니라 **독자가 필요한 판단과 근거를 빠르게 찾게 하는 것**이 목표다.

## Rules

- 제목과 description만으로 문서의 책임을 식별할 수 있게 한다.
- 첫 단락에서 목적, 핵심 결론 또는 문서가 소유하는 범위를 제시한다.
- heading은 내용의 논리적 계층을 표현할 때만 추가한다.
- 한 section은 하나의 질문이나 책임을 중심으로 구성한다.
- 표는 같은 차원을 비교할 때 사용하고, 단순 나열은 list를 사용한다.
- 같은 개념에는 같은 용어를 사용한다.
- 예시는 규칙을 보완할 때만 두고 규칙 전체를 반복하지 않는다.
- 독자가 다른 문서로 이동해야 할 때만 명시적인 link를 둔다.

## Default Shape

고정 template은 요구하지 않는다. 대부분의 reference는 다음 정도면 충분하다.

```markdown
---
title: ...
description: ...
---

# Title

문서의 목적 또는 핵심 결론.

## Main responsibility

필요한 규칙, 근거, 판단 기준.

## Boundary

이 문서가 소유하지 않는 것과 다음 authoritative reference.
```

문서 성격상 다른 구조가 더 명확하면 그대로 사용한다.

## Review Test

- 첫 화면에서 이 문서를 읽어야 하는 이유를 알 수 있는가?
- 원하는 규칙이나 결론을 heading만 훑어도 찾을 수 있는가?
- 문서 구조가 내용보다 더 복잡하지 않은가?
- 다른 authoritative document의 내용을 불필요하게 복제하지 않는가?

구조를 위해 빈 section, 의미 없는 요약, 상투적인 탐색 제안을 추가하지 않는다.

인간의 이해가 유지보수 병목이 되는 배경은 [Understanding Bottleneck](../concepts/agent-assets-concepts-understanding-bottleneck.md)을 참고한다.
