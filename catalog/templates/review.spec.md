---
description: 일반 리뷰를 3:4 세로 화면에 맞게 작성할 때 항목별 근거·영향·조치와 검증 결과의 작성 계약을 확인합니다.
---

# Review Template Spec

[Review](review.md)은 코드, 문서, 설계, 운영 등 **하나의 검토 대상에 대한 근거 중심 결과**를 전달하는 범용 Markdown 양식입니다. 해당 작업의 리뷰 방법이나 승인 정책은 이 템플릿이 결정하지 않습니다.

## Fields

- `title`: 검토 결과를 식별할 제목.
- `verdict`, `summary`: 검토 범위에 한정한 판정과 1~3문장의 핵심 근거·필요 조치. 적용되는 정책의 판정 용어를 사용합니다.
- `target`, `revision`, `scope`: 실제로 본 대상 링크·식별자, 기준 revision/version/baseline, 검토한 범위. Revision은 인라인 코드로 표시합니다.
- `findings`: 확정된 문제·실질적 관찰만 기록합니다. 각 항목의 `id`는 안정적인 `F1`… 식별자, `severity`는 적용되는 분류, `summary`는 짧은 문제 설명입니다.
- `finding.evidence`: 확인한 사실과 직접 탐색 가능한 근거 링크·위치를 반드시 포함합니다. 근거가 부족한 후보는 확정 Finding에 넣지 않습니다.
- `finding.impact`: 어떤 조건에서 누구·무엇에 영향이 있는지 기록합니다. `finding.action`은 필요한 조치이며, 없으면 빈 값으로 두고 Action을 생략합니다.
- `validation`: 항목별 `name`(check), `result`(상태), `evidence`(결과와 근거)를 기록합니다. 중요하지만 미수행한 check도 그 상태와 이유를 명시합니다.
- `risks_and_limits`: 남은 위험, 확인할 수 없었던 부분, 재검토 조건. Finding이나 Validation을 중복하지 않습니다.

## Rendering

- 결론 callout은 한 번만 작성합니다. Finding이 없으면 `Findings`는 유지하고 "확인된 finding 없음."이라고 씁니다.
- 가로:세로 **3:4의 세로 화면**을 기본 읽기 환경으로 삼습니다. 결론 → Finding별 근거·영향·조치 → 검증 결과 순으로 세로로 읽게 구성합니다.
- Finding은 ID·severity·짧은 summary를 제목으로 두고 바로 아래에 Evidence·Impact·필요한 Action을 배치합니다. 별도 요약표나 `Details`에 같은 내용을 반복하지 않습니다. 기존 `details`의 근거·영향·조치는 해당 `finding`으로 합칩니다.
- 긴 설명을 다열 표에 넣지 않습니다. 문장과 목록은 자연스럽게 줄바꿈되도록 쓰고, 긴 URL·경로는 짧고 구체적인 링크 이름으로 표시합니다. Heading의 summary와 인라인 코드 식별자는 짧게 유지합니다.
- 구체적인 해상도·renderer는 사용 환경에 맞게 정합니다. 긴 설명·링크·revision을 포함한 예시를 3:4 화면에서 확인하고, 핵심 내용을 읽는 데 가로 스크롤이나 축소가 필요한지 점검합니다.
- `severity`와 `verdict`는 대상 프로젝트의 기준을 따릅니다. 기준이 없으면 임의 등급·승인을 만들어내지 말고 분류가 없음을 명시합니다.
- Validation에는 `✅ Pass` / `❌ Fail` / `⚪ Not Verified`처럼 결과를 구분하는 표기를 권장합니다. 미실행·접근 불가인 경우 통과로 표시하지 않습니다.
- `{{ value }}`는 확인한 값으로, `{% for ... %}`는 실제 행 수만큼, `{% if ... %}`는 조건에 맞는 section만 렌더링하는 작성용 표기입니다. 최종 문서에는 미치환 표기를 남기지 않습니다.
- `Risks and Limits`는 필요할 때만 남깁니다. 검토하지 않은 범위를 전체 검토로 표현하지 않습니다.

## Boundaries

이 양식은 결과의 표시 구조일 뿐 리뷰 수행 절차·심각도 기준·승인·merge 권한을 소유하지 않습니다. 대상 환경이 요구하는 frontmatter는 결과물을 작성할 때 그 환경의 계약에 따라 추가합니다. GitHub PR Review의 전용 본문 형식은 [GitHub Templates](../../.github/templates/pull-request-review.md)가 소유합니다.
