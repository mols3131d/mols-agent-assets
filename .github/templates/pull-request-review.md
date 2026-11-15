## Summary

<!-- 검토 결론과 결정적 근거부터 적습니다. GitHub Review decision은 반복하지 않습니다.
Finding이 없으면 검토 범위에서 확인된 문제가 없었다는 사실을 Summary에 명시합니다. -->

{{ summary }}

{% if scope %}
## Scope

<!-- 일부 범위만 검토했거나 검토 기준이 달랐을 때만 작성합니다. -->
{% for item in scope %}
- {{ item }}
{% endfor %}
{% endif %}

{% if findings or has_inline_findings %}
## Findings

<!-- 확인된 문제만 기록합니다. 기본은 굵은 finding 제목을 사용하고,
Finding이 길어 구분이 어려울 때에만 H3 제목으로 바꿀 수 있습니다.
Inline finding을 본문에 중복하지 않습니다. -->
{% if findings %}
{% for finding in findings %}
**{{ finding.importance }} · F{{ loop.index }} — {{ finding.title }}**

**Impact:** {{ finding.impact }}

{% if finding.required_changes %}
**Required Change**

{% for change in finding.required_changes %}
- {{ change }}
{% endfor %}
{% endif %}

{% if finding.evidence %}
**Evidence**

{% for item in finding.evidence %}
- {{ item }}
{% endfor %}
{% endif %}

{% if finding.locations %}
**Location**

{% for location in finding.locations %}
- {{ location }}
{% endfor %}
{% endif %}

{% if finding.uncertainty %}
**Uncertainty:** {{ finding.uncertainty }}
{% endif %}

{% endfor %}
{% else %}
See inline review comments for findings.
{% endif %}
{% endif %}

{% if validation %}
## Validation

<!-- 실제 실행·확인한 검사와 중요한 미검증만 표시합니다.
check.status: ✅ Pass / ❌ Fail / ⚪ Not Verified.
중요도·정렬은 docs/development/github.md를 따릅니다. -->
{% for check in validation %}
- {{ check.status }} — `{{ check.name }}`: {{ check.evidence }}
{% endfor %}
{% endif %}

{% if remaining_risks %}
## Remaining Risks

{% for risk in remaining_risks %}
- {{ risk }}
{% endfor %}
{% endif %}

<!-- Agent가 작성한 최종 Review에는 author가 필요합니다.
해당 diff를 검토한 경우 base/head revision도 기록합니다.
본문 끝에 하나의 fenced yaml 메타데이터 블록만 남깁니다. -->
{% if author or revision %}
```yaml
{% if author %}
author:
{% for item in author %}
  - {{ item }}
{% endfor %}
{% endif %}
{% if revision %}
revision:
  base: {{ revision.base }}
  head: {{ revision.head }}
{% endif %}
```
{% endif %}
