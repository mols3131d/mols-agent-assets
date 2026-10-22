---
description: PR 245의 3:4 세로 구성과 Finding·관점·후보 판단 표시를 확인하는 가상 리뷰 예시입니다.
---

# 리뷰 템플릿 검토 예시

> [!IMPORTANT]
> **수정 필요 (가상 예시)** — 아래는 표시 구조를 확인하기 위한 가상 리뷰입니다. 실제 검토·실행 결과가 아닙니다. 긴 근거와 조치를 세로로 읽는 상황을 가정합니다.

- **Target** — [가상 템플릿](https://example.com/repository/blob/0123456789012345678901234567890123456789/templates/review.md)
- **Revision** — `0123456789012345678901234567890123456789`
- **Scope** — 일반·다관점 양식의 근거 추적성, 후보 판단과 좁은 화면에서의 읽기 흐름

## Findings

### F1 · High (예시 분류) — Finding의 근거가 누락될 수 있음

- **Evidence** — [가상 spec의 근거 규칙](https://example.com/repository/blob/0123456789012345678901234567890123456789/templates/review.spec.md#L16-L24)은 상세를 선택 사항으로 두며, 요약에도 근거 위치를 요구하지 않습니다. 근거 없이 문제를 확정할 수 있는 구조라는 가정입니다.
- **Impact** — 요약만 읽는 독자가 관찰 사실과 추정을 구분하기 어렵습니다. 다른 검토자가 같은 위치에서 주장을 재확인할 수 없어, 수정 여부를 결정할 때 추가 탐색이 필요합니다.
- **Action** — 각 Finding 안에 근거 링크·확인한 사실과 영향을 함께 배치합니다. 같은 설명을 별도 요약과 상세에 반복하지 않습니다.

## Perspectives

### 근거 추적성

- **Reviewer / Method** — 단일 검토자가 순차로 살펴본다는 가정. 같은 문서와 맥락을 공유하며 독립 검토를 뜻하지 않습니다.
- **Focus** — 독자가 Finding을 뒷받침하는 원문과 판단 이유를 직접 확인할 수 있는가?
- **Assessment** — 근거를 각 항목 안에 모으는 구성이 필요하다는 가상 판단입니다. 관련 문제와 조치는 F1을 참조합니다.
- **Evidence** — [가상 spec](https://example.com/repository/blob/0123456789012345678901234567890123456789/templates/review.spec.md#L16)

### 표시 구조

- **Reviewer / Method** — 같은 검토자가 별도 질문으로 재검토한다는 가정.
- **Focus** — 긴 한국어 설명과 링크를 좁은 화면에서 위에서 아래로 따라 읽을 수 있는가?
- **Assessment** — 가로 표에 여러 설명을 동시에 배치하면 확인 순서가 분산될 수 있습니다. 사용 환경별 실제 렌더링 확인이 필요하다는 가정입니다.
- **Evidence** — [가상 읽기 환경](https://example.com/review/portrait-reading-environment)

## Candidate Decisions

### C1 · Accept

Finding의 근거가 빠질 수 있다는 후보.

- **Perspectives** — 근거 추적성
- **Rationale** — 가상 규칙에서 누락 경로를 확인했다는 가정으로 F1에 통합합니다.
- **Finding** — F1

### C2 · Drop

별도 요약표를 반드시 유지해야 한다는 후보.

- **Perspectives** — 표시 구조
- **Rationale** — 이 가상 예시에서는 요약표가 필수라는 요구가 없으므로 제외합니다.
- **Finding** — —

### C3 · Open

모든 renderer에서 동일하게 표시된다는 후보.

- **Perspectives** — 표시 구조
- **Rationale** — 환경별 검증이 없으므로 미해결로 남깁니다. 확인 조건은 Risks and Limits를 참조합니다.
- **Finding** — —

## Validation

### ⚪ Not Verified · 렌더링 실행

가상 리뷰에서는 실행하지 않았다는 상태를 표시한 예시입니다. 실제 실행 근거를 뜻하지 않습니다.

## Risks and Limits

- C3: 사용하는 renderer와 해상도에서 긴 설명·링크를 넣어 확인한 후 판단합니다. 예시는 모든 환경에서의 표시를 보장하지 않습니다.
