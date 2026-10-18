# {{ subject }} — 다관점 리뷰

## 결론

{{ conclusion }}

## 대상과 기준

- **대상:** {{ target }}
- **기준 상태:** {{ basis }}
- **검토 범위와 질문:** {{ scope }}
- **관점 검토 방식:** {{ review_method }}

## 관점별 결과

{% for perspective in perspectives %}
### {{ perspective.name }} — {{ perspective.question }}

- **관찰과 판단:** {{ perspective.assessment }}
- **근거:** {{ perspective.evidence }}
- **확인하지 못한 부분:** {{ perspective.limitations }}

{% endfor %}

## 종합 판단

{{ reconciliation }}

## 통합 발견 사항

{% if findings %}
{% for finding in findings %}
### {{ finding.title }}

- **문제와 영향:** {{ finding.impact }}
- **근거:** {{ finding.evidence }}
{% if finding.action %}
- **권고 조치:** {{ finding.action }}
{% endif %}

{% endfor %}
{% else %}
검토 범위에서 확인된 문제는 발견되지 않았습니다.
{% endif %}

## 검증과 한계

- **직접 확인한 사항:** {{ verification }}
- **남은 불확실성과 검토 제약:** {{ limitations }}

{% if next_actions %}
## 후속 조치

{% for action in next_actions %}
- {{ action }}
{% endfor %}
{% endif %}
