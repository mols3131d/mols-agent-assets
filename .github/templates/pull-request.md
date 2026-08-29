## Summary

<!--
왜 필요한 변경이며 merge 후 무엇이 달라지는지 먼저 설명한다.
구현 상세는 Changes에 둔다.
-->

{{ summary }}

## Changes

<!-- 파일 목록을 반복하기보다 검토자가 확인해야 할 동작, 계약과 구조의 변화를 적는다. -->

{% for change in changes %}
- {{ change }}
{% endfor %}

## Validation

<!--
직접 확인한 check와 근거만 적는다.
중요한 미수행 검증은 숨기지 말고 ⚪ Not Verified로 남긴다.
상태: ✅ Pass / ❌ Fail / ⚪ Not Verified
-->

{% for check in validation %}
- {{ check.status }} — `{{ check.name }}`: {{ check.evidence }}
{% endfor %}

{% if review_focus %}
## Review Focus

<!-- 특히 확인할 결정, trade-off나 위험만 적는다. Review 범위를 제한하지 않는다. -->

{% for item in review_focus %}
- {{ item }}
{% endfor %}
{% endif %}

{% if risks %}
## Risks

<!--
`risk.importance`는 `🔴 Critical` / `🟠 High` / `🟡 Medium` / `🔵 Low` 중 하나를 그대로 사용한다.
현재 변경에서 실제로 고려해야 할 risk만 적고 finding이나 Validation을 반복하지 않는다.
-->

{% for risk in risks %}
- {{ risk.importance }} — {{ risk.description }}
{% endfor %}
{% endif %}

{% if boundaries %}
## Boundaries

{% for boundary in boundaries %}
- {{ boundary }}
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
