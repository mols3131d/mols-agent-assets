## Summary

<!--
전체적으로 어떻게 판단했는가? 가장 중요한 근거는 무엇인가?
결론부터 쓰고 필요한 경우 다음 조치를 덧붙인다. GitHub review decision은 본문에 반복하지 않는다.
-->

{{ summary }}

## Findings

<!--
확인된 문제만 finding으로 기록한다. 단순 선호나 근거 없는 가능성은 제외한다.
문제가 없으면 `✅ No findings`를 남긴다.
중요도: 🔴 Critical / 🟠 High / 🟡 Medium / 🔵 Low
-->

{% if findings %}
{% for finding in findings %}
### {{ finding.importance }} — F{{ loop.index }} · {{ finding.title }}

{% if finding.locations %}
- **Location**
{% for location in finding.locations %}
  - {{ location }}
{% endfor %}
{% endif %}
{% if finding.evidence %}
- **Evidence**
{% for item in finding.evidence %}
  - {{ item }}
{% endfor %}
{% endif %}
- **Impact:** {{ finding.impact }}
{% if finding.required_changes %}
- **Required Change**
{% for change in finding.required_changes %}
  - {{ change }}
{% endfor %}
{% endif %}
{% if finding.uncertainty %}
- **Uncertainty:** {{ finding.uncertainty }}
{% endif %}

{% endfor %}
{% else %}
✅ No findings
{% endif %}

## Validation

<!--
무엇을 직접 확인했고 어떤 근거가 있는가?
diff, contract, test, command 등 실제 확인 결과만 기록한다.
중요한 미확인 영역은 ⚪ Not Verified로 남긴다.
-->

{% for check in validation %}
- {{ check.status }} — `{{ check.name }}`: {{ check.evidence }}
{% endfor %}

{% if remaining_risks %}
## Remaining Risks

{% for risk in remaining_risks %}
- ⚠️ {{ risk }}
{% endfor %}
{% endif %}

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
