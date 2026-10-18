---
description: 일반 리뷰를 Markdown으로 작성할 때 결론, 검토 기준, 발견 사항, 상세 근거와 검증 결과의 작성 계약을 확인합니다.
---

# Review Template Spec

[Review](review.md)은 코드, 문서, 설계, 운영 등 **하나의 검토 대상에 대한 근거 중심 결과**를 전달하는 범용 Markdown 양식입니다. 해당 작업의 리뷰 방법이나 승인 정책은 이 템플릿이 결정하지 않습니다.

## Fields

| Field | Contract |
| --- | --- |
| `title` | 검토 결과를 식별할 제목 |
| `verdict`, `summary` | 검토 범위에 한정한 판정과 1~3문장의 핵심 근거·필요 조치. 적용되는 정책의 판정 용어 사용 |
| `target`, `revision`, `scope` | 실제로 본 대상 링크·식별자, 기준 revision/version/baseline, 검토한 범위 |
| `findings` | 확정된 문제·실질적 관찰만 기입. 각 행은 `F1`… ID, 적용되는 severity, 짧은 finding, 필요한 action |
| `details` | 요약만으로 판단하기 어려운 finding만 확장. 같은 ID로 Locations, Evidence, Impact, 필요하면 Action 기록 |
| `validation` | 수행한 check와 결과·근거; 확인이 필요하지만 미수행한 check도 그 상태와 이유를 명시 |
| `risks_and_limits` | 남은 위험, 확인할 수 없었던 부분, 재검토 조건. 이미 기록한 finding이나 validation을 중복하지 않음 |

## Rendering

- 결론 callout은 한 번만 작성합니다. Finding이 없으면 `Findings`는 유지하고 "확인된 finding 없음."이라고 씁니다.
- `Details`와 `Risks and Limits`는 필요할 때만 남깁니다. Detail의 `id`는 Finding 표의 ID와 일치해야 합니다.
- `Severity`와 `verdict`는 대상 프로젝트의 기준을 따릅니다. 기준이 없으면 임의 등급·승인을 만들어내지 말고 분류가 없음을 명시합니다. 필요 없는 Action은 표에서 `—`로 표기합니다.
- Validation에는 `✅ Pass` / `❌ Fail` / `⚪ Not Verified`처럼 결과를 구분하는 표기를 권장합니다. 미실행·접근 불가인 경우 통과로 표시하지 않습니다.
- `{{ value }}`는 확인한 값으로, `{% for ... %}`는 실제 행 수만큼, `{% if ... %}`는 조건에 맞는 section만 렌더링하는 작성용 표기입니다. 최종 문서에는 미치환 표기를 남기지 않습니다.
- 파일·테스트·요구사항처럼 실제 판단을 뒷받침하는 위치는 직접 탐색 가능한 링크로 남깁니다. 검토하지 않은 범위를 전체 검토로 표현하지 않습니다.

## Boundaries

이 양식은 결과의 표시 구조일 뿐 리뷰 수행 절차·심각도 기준·승인·merge 권한을 소유하지 않습니다. 대상 환경이 요구하는 frontmatter는 결과물을 작성할 때 그 환경의 계약에 따라 추가합니다. GitHub PR Review의 전용 본문 형식은 [GitHub Templates](../../.github/templates/pull-request-review.md)가 소유합니다.
