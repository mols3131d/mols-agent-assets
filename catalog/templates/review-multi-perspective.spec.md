---
description: 다관점 리뷰의 관점별 근거, 후보 채택·제외·미해결 판단과 통합 Finding을 Markdown으로 기록할 때 사용합니다.
---

# Multi-perspective Review Template Spec

[Multi-perspective Review](review-multi-perspective.md)는 **서로 다른 검토 질문을 근거로 종합한 결과**를 전달합니다. 공통 판정, Finding·Details·Validation 작성 기준은 [Review Spec](review.spec.md)을 따르며 여기서는 추가된 의미만 정의합니다.

## Perspectives

- `perspectives`는 **실제로 수행한 서로 다른 관점 2개 이상**을 기록합니다. 관점의 이름·수·검토자 구성은 고정하지 않습니다.
- 각 행은 `name`(관점), `reviewer_method`(실제 검토 주체·수행 방법과 컨텍스트 공유 여부), `focus`(검토한 질문·범위), `assessment`와 `evidence`(관찰·판단과 확인 가능한 근거)를 담습니다.
- 여러 관점을 한 실행 주체가 순차로 검토했다면 독립 검토라고 주장하지 않습니다. 관점 이름만 바꾼 반복 의견으로 관점 수를 채우지 않습니다.

## Candidate Decisions

- 후보는 같은 원인이나 주장을 기준으로 중복 제거하고 `C1`, `C2`… ID로 식별합니다.
- `candidate.perspectives`는 제기한 관점, `candidate.claim`은 검토할 주장, `candidate.rationale`은 근거·반증·판단 이유입니다.
- `candidate.decision`은 `Accept`(근거가 성립해 최종 Finding으로 반영), `Drop`(불성립·비관련·중복 등으로 제외), `Open`(판정을 바꿀 수 있으나 근거가 부족함)을 구분합니다. 다수결이나 reviewer 동의는 근거가 아닙니다.
- `Accept`는 반드시 확정된 `F` ID에 연결하고, `Drop`과 `Open`은 Finding을 참조하지 않습니다. `Open`의 결정 조건·남은 검증은 `Risks and Limits`에 남깁니다.
- 별도 후보가 없으면 표를 비워두지 않고 없음을 명시합니다. 리뷰를 위해 가짜 후보를 만들지 않습니다.

## Rendering and Boundary

최종 `Findings`는 수용한 후보 중 확인된 내용만 중복 없이 표시합니다. `Perspectives`는 관점별 입력을, `Candidate Decisions`는 채택·제외·미해결의 판단 근거를 소유합니다. 같은 설명을 반복하지 않고 ID·링크로 연결합니다.

이 템플릿은 특정 다관점 실행 workflow, 독립성 보장 또는 최종 승인 권한을 소유하지 않습니다. 관점별 주장과 후보를 증거로 평가하며, 해결되지 않은 실질적 이견을 임의로 결론에 흡수하지 않습니다.
