# {{ title }}

> [!IMPORTANT]
> **{{ verdict }}** — {{ summary }}

- **Target** — {{ target }}
- **Revision** — {{ revision }}
- **Scope** — {{ scope }}

## Findings

{% if findings %}
| ID | Severity | Finding | Action |
| --- | --- | --- | --- |
{% for finding in findings %}
| {{ finding.id }} | {{ finding.severity }} | {{ finding.summary }} | {{ finding.action }} |
{% endfor %}
{% else %}
확인된 finding 없음.
{% endif %}

{% if details %}
## Details

{% for detail in details %}
### {{ detail.id }} · {{ detail.title }}

{% if detail.locations %}
#### Locations

{% for location in detail.locations %}
- {{ location }}
{% endfor %}
{% endif %}

#### Evidence

{{ detail.evidence }}

#### Impact

{{ detail.impact }}

{% if detail.action %}
#### Action

{{ detail.action }}
{% endif %}

{% endfor %}
{% endif %}

## Validation

{% if validation %}
| Result | Check | Evidence |
| --- | --- | --- |
{% for check in validation %}
| {{ check.result }} | {{ check.name }} | {{ check.evidence }} |
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
