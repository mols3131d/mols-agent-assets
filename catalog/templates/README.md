---
description: 일반 리뷰와 다관점 리뷰의 범용 Markdown 양식과 개별 작성 스펙을 선택할 때 사용합니다.
---

# Markdown Templates

리뷰 결과를 **빠르게 판단하고 근거를 추적**할 수 있도록 하는 범용 Markdown 작성 양식입니다. 템플릿은 출력 구조를, 옆의 `.spec.md`는 필드 의미와 작성·생략 조건을 정의합니다.

- **일반 리뷰:** [Review](review.md) · [Spec](review.spec.md). 한 검토의 결론·Finding·검증을 기록합니다.
- **다관점 리뷰:** [Multi-perspective Review](review-multi-perspective.md) · [Spec](review-multi-perspective.spec.md). 서로 다른 관점의 후보를 비교·판정한 결과를 기록합니다.

가로:세로 3:4 화면에서 읽기 쉽도록 항목을 세로로 배치합니다. Finding마다 근거·영향·조치를 함께 두고, 긴 설명을 다열 표에 넣지 않습니다.

양식과 스펙을 함께 선택하고 실제 값으로 치환한 뒤, 사용하지 않는 선택 섹션과 템플릿 표기를 제거합니다. `{{ ... }}`, `{% if ... %}`, `{% for ... %}`는 작성용 표기이며 Jinja2 실행을 요구하지 않습니다.

구조는 HMDA Data Reliability의 [Review](https://github.com/mols3131d/hmda-data-reliability/blob/34519fec148dd2ab38ddf0cc0157c3d3ed9f7247/inbox/_templates/review.md)와 [Multi-perspective Review](https://github.com/mols3131d/hmda-data-reliability/blob/34519fec148dd2ab38ddf0cc0157c3d3ed9f7247/inbox/_templates/review-multi-perspective.md)를 참고했습니다. 참고 저장소 고유의 verdict, severity, frontmatter·Inbox 정책은 가져오지 않습니다. GitHub PR Review 본문은 [전용 템플릿](../../.github/templates/pull-request-review.md)을 사용합니다.
