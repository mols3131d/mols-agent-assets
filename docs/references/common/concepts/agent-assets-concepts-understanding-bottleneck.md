---
title: Understanding Bottleneck
description: AI가 산출물을 만드는 속도보다 인간이 시스템을 이해하는 속도가 느려질 때 생기는 유지보수 병목과 자산 설계 함의
---

# Understanding Bottleneck

AI가 코드와 문서를 빠르게 생성할수록 병목은 생성 자체보다 **사람이 시스템의 구조와 판단 근거를 따라가는 능력**으로 이동할 수 있습니다.

이 저장소에서 중요한 문제는 산출물의 양이 아니라, 인간 maintainer가 다음을 할 수 있는가입니다.

- 무엇이 authoritative한지 찾습니다.
- 왜 이 경계와 규칙이 존재하는지 이해합니다.
- 변경이 어떤 책임에 영향을 주는지 판단합니다.
- AI가 만든 결과를 검토하고 방향을 수정합니다.

## Cognitive Debt

```text
빠른 생성
→ 이해하지 못한 자산과 abstraction 누적
→ authority와 책임 경계가 불투명
→ 변경 판단과 리뷰 비용 증가
```

## Design Implications

문서를 많이 만드는 것으로 해결하지 않습니다.

- authoritative owner와 책임 경계를 명확히 하고 중복·불필요한 구조를 줄입니다. → [Design Principles](../principles/README.md)
- 사람이 빠르게 탐색할 수 있는 문서 구조를 사용합니다. → [Human-Readable Documents](../authoring/agent-assets-authoring-human-readable-documents.md)
- 중요한 rationale과 invariant는 재생성 가능한 작업 로그와 구분해 보존합니다.

## Boundary

Understanding Bottleneck은 더 많은 설명을 정당화하는 원칙이 아닙니다. **필요한 이해를 최소한의 authoritative structure로 유지해야 한다는 문제 정의**입니다.

## Source

- [Understanding is the New Bottleneck](https://wikidocs.net/blog/@jaehong/23176/)
