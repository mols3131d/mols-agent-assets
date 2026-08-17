---
title: Understanding Bottleneck
description: AI가 산출물을 만드는 속도보다 인간이 시스템을 이해하는 속도가 느려질 때 생기는 유지보수 병목과 자산 설계 함의
---

# Understanding Bottleneck

AI가 코드와 문서를 빠르게 생성할수록 병목은 생성 자체보다 **사람이 시스템의 구조와 판단 근거를 따라가는 능력**으로 이동할 수 있다.

이 저장소에서 중요한 문제는 산출물의 양이 아니라, 인간 maintainer가 다음을 할 수 있는가다.

- 무엇이 authoritative한지 찾는다.
- 왜 이 경계와 규칙이 존재하는지 이해한다.
- 변경이 어떤 책임에 영향을 주는지 판단한다.
- AI가 만든 결과를 검토하고 방향을 수정한다.

## Cognitive Debt

작동하는 자산이 늘어도 의미와 ownership을 이해하지 못하면 cognitive debt가 쌓인다.

```text
빠른 생성
→ 이해하지 못한 자산과 abstraction 누적
→ authority와 책임 경계가 불투명
→ 변경 판단과 리뷰 비용 증가
```

## Design Implications

이 문제를 해결하기 위해 문서를 많이 만드는 것은 답이 아니다.

- authoritative owner를 명확히 한다. → [DRY](../principles/agent-assets-principles-dry.md)
- 책임 경계를 작고 cohesive하게 유지한다. → [SRP](../principles/agent-assets-principles-srp.md)
- 행동과 구조에 기여하지 않는 설명을 줄인다. → [KISS](../principles/agent-assets-principles-kiss.md)
- 사람이 빠르게 탐색할 수 있는 문서 구조를 사용한다. → [Human-Readable Documents](../authoring/agent-assets-authoring-human-readable-documents.md)
- 중요한 rationale과 invariant는 재생성 가능한 작업 로그와 구분해 보존한다.

## Boundary

Understanding Bottleneck은 더 많은 설명을 정당화하는 원칙이 아니다. **필요한 이해를 최소한의 authoritative structure로 유지해야 한다는 문제 정의**다.

## Source

- [Understanding is the New Bottleneck](https://wikidocs.net/blog/@jaehong/23176/)
