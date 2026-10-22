# {{ title }}

> [!IMPORTANT]
> **{{ verdict }}** — {{ summary }}

- **Target** — {{ target }}
- **Revision** — `{{ revision }}`
- **Scope** — {{ scope }}

## Findings

{% if findings %}
{% for finding in findings %}

### {{ finding.id }} · {{ finding.severity }} — {{ finding.summary }}

- **Evidence** — {{ finding.evidence }}
- **Impact** — {{ finding.impact }}
{% if finding.action %}
- **Action** — {{ finding.action }}
{% endif %}

{% endfor %}
{% else %}
확인된 finding 없음.
{% endif %}

## Validation

{% if validation %}
{% for check in validation %}

### {{ check.result }} · {{ check.name }}

{{ check.evidence }}

{% endfor %}
{% else %}
검증 결과가 기록되지 않았습니다.
{% endif %}

{% if risks_and_limits %}

## Risks and Limits

{% for item in risks_and_limits %}

- {{ item }}
{% endfor %}
{% endif %}
