---
description: 반복해서 작성하는 일반 리뷰와 다관점 리뷰 Markdown 결과물의 양식과 작성 스펙을 선택할 때 사용합니다.
---

# Markdown Templates

검토 결과를 일관되게 **기록하고 전달**하기 위한 재사용 가능한 Markdown 양식입니다. 템플릿은 결과물의 표현 구조를, 같은 이름의 `.spec.md`는 항목의 의미와 작성·생략 조건을 정의합니다.

| 목적 | 양식 | 스펙 |
| --- | --- | --- |
| 하나의 검토를 결론·근거·후속 조치 중심으로 정리 | [Review](review.md) | [Review Spec](review.spec.md) |
| 서로 다른 검토 관점을 비교·조정해 하나의 판단으로 정리 | [Multi-perspective Review](multi-perspective-review.md) | [Multi-perspective Review Spec](multi-perspective-review.spec.md) |

## 사용

1. 목적에 맞는 템플릿과 스펙을 함께 선택합니다.
1. 확인된 정보로 변수를 치환하고 반복 블록을 실제 항목 수만큼 작성합니다.
1. 조건에 맞지 않는 블록과 작성용 표기를 제거해 일반 Markdown으로 완성합니다.

`{{ value }}`, `{% if ... %}`, `{% for ... %}`는 구조를 표시하는 Jinja2-style 표기일 뿐, 특정 렌더러나 실행 환경을 요구하지 않습니다. 실제 검토 방법, 검증, 승인 또는 완료 절차를 대신하지 않습니다. GitHub PR Review 전용 본문 형식은 [GitHub Authoring Templates](../../.github/templates/README.md)가 별도로 소유합니다.
