## Summary

<!--
왜 필요한 변경이며, merge 후 무엇이 달라지는가?
핵심 결과를 먼저 쓰고 구현 상세는 Changes에 둔다.
-->

{{ summary }}

## Changes

<!--
검토자가 diff에서 확인해야 할 최종 변화를 적는다.
파일 목록보다 동작, 계약과 구조의 변화에 집중한다.
-->

{% for change in changes %}
- {{ change }}
{% endfor %}

## Validation

<!--
직접 확인한 check와 근거를 적는다.
중요한 미수행 검증은 숨기지 말고 ⚪ Not Verified로 남긴다.
상태: ✅ Pass / ❌ Fail / ⚪ Not Verified
-->

{% for check in validation %}
- {{ check.status }} — `{{ check.name }}`: {{ check.evidence }}
{% endfor %}

{% if boundaries %}
## Boundaries

{% for boundary in boundaries %}
- {{ boundary }}
{% endfor %}
{% endif %}

{% if review_focus %}
## Review Focus

<!--
특히 확인할 결정, trade-off나 위험만 강조한다.
이 section은 review 범위를 제한하지 않는다.
-->

{% for item in review_focus %}
- {{ item }}
{% endfor %}
{% endif %}

{% if risks %}
## Risks

{% for risk in risks %}
- {{ risk }}
{% endfor %}
{% endif %}

{% if references %}
## References

{% for reference in references %}
- {{ reference }}
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
