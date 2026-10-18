---
description: 다관점 리뷰 결과를 Markdown으로 기록할 때 관점별 근거, 실제 독립성, 이견 조정과 통합 발견 사항을 어떻게 구분할지 확인합니다.
---

# Multi-perspective Review Template Spec

[Multi-perspective review template](multi-perspective-review.md)은 **서로 다른 질문이나 실패 조건으로 검토한 결과를 근거에 따라 종합**하는 형식입니다. 관점의 수, 이름, 담당 agent나 순서는 고정하지 않습니다.

## 작성 계약

- **결론과 범위:** `subject`, `conclusion`, `target`, `basis`, `scope`는 일반 [Review Spec](review.spec.md)과 같은 의미입니다. `conclusion`은 최종 판단을 먼저 말하고, 확인 범위를 넘어선 확신을 표현하지 않습니다.
- **검토 방식:** `review_method`에는 실제 사용한 방식(예: 분리된 검토자, 한 실행 주체의 순차적 관점 검토)을 적습니다. 검토 맥락이나 판단이 공유됐다면 독립 검토라고 주장하지 않습니다.
- **관점별 결과:** `perspectives`의 각 항목은 서로 다른 판단 질문(`question`)을 가져야 합니다. `name`은 관점을 식별하고, `assessment`는 그 관점의 관찰·판단, `evidence`는 직접 확인 가능한 근거, `limitations`는 해당 관점이 확인하지 못한 범위를 담습니다. 같은 지적을 관점 이름만 바꿔 반복하지 않습니다.
- **종합 판단:** `reconciliation`은 관점들 사이의 중복·일치·충돌을 **근거와 반증에 따라** 해소하거나 남겨둔 이유를 설명합니다. 다수결, reviewer 수, 동의 자체는 문제의 진위를 증명하지 않습니다. `conclusion`을 길게 되풀이하지 않습니다.
- **통합 발견 사항:** `findings`에는 교차 검토 후 근거가 성립한 문제만 중복 없이 정리합니다. 각 항목의 `title`, `impact`, `evidence`, 선택적인 `action`은 일반 리뷰와 같은 의미입니다. 배제한 후보를 발견 사항으로 되살리거나 미해결 가설을 확정하지 않습니다.
- **검증·한계·조치:** `verification`은 실제 확인한 사항만, `limitations`는 판단에 영향을 줄 수 있는 미검증 사항·미해결 이견·관점 누락을, `next_actions`는 필요한 후속 행동을 적습니다. 아직 수행하지 않은 검증이나 조치를 완료로 표현하지 않습니다.

## 조건과 출력

| 항목 | 조건 |
| --- | --- |
| `subject`, `conclusion`, `target`, `basis`, `scope`, `review_method` | 항상 작성 |
| `perspectives` | 실제 수행한 서로 다른 관점 2개 이상 작성. 수행하지 않은 관점을 채우지 않음 |
| `reconciliation` | 항상 작성. 합의·충돌·미해결이 없더라도 검토 근거가 어떻게 통합됐는지 설명 |
| `findings` | 0개 이상. 없으면 템플릿의 발견 없음 문구 사용 |
| `findings[].action`, `next_actions` | 실제 필요한 경우에만 유지 |
| `verification`, `limitations` | 항상 작성. 수행하지 않은 검증·남아 있는 한계도 명시 |

최종 결과에서는 모든 템플릿 표기와 비어 있는 선택 항목을 제거합니다. 미해결 이견이 중요한 경우 어느 판단을 바꿀 수 있는지와 추가로 필요한 근거를 `limitations` 또는 `next_actions`에 남깁니다.

## 경계

다관점은 **출력에 드러내는 검토 관점과 종합 근거의 구조**이지 특정 agent 구성이나 실행 workflow가 아닙니다. 실제 독립 실행, 검토 방법, 조치 여부와 완료 판정은 해당 작업을 운영하는 주체가 결정합니다. 이 형식은 일반 리뷰를 확장하지만 GitHub PR Review의 provenance, decision과 surface 규칙을 대체하지 않습니다.
