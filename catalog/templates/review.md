# {{ subject }} — 리뷰

## 결론

{{ conclusion }}

## 대상과 기준

- **대상:** {{ target }}
- **기준 상태:** {{ basis }}
- **검토 범위와 질문:** {{ scope }}

## 발견 사항

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
- **미검증 사항과 제약:** {{ limitations }}

{% if next_actions %}
## 후속 조치

{% for action in next_actions %}
- {{ action }}
{% endfor %}
{% endif %}
