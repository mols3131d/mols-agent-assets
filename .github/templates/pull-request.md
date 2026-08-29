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
`check.status`는 `✅ Pass` / `❌ Fail` / `⚪ Not Verified` 중 하나를 그대로 사용한다.
상태의 의미와 정렬 기준은 `docs/development/github.md`를 따른다.
-->

{% for check in validation %}
- {{ check.status }} — `{{ check.name }}`: {{ check.evidence }}
{% endfor %}

{% if risks %}
## Risks

<!--
`risk.importance`는 `🔴 Critical` / `🟠 High` / `🟡 Medium` / `🔵 Low` 중 하나를 그대로 사용한다.
Importance의 의미와 정렬 기준은 `docs/development/github.md`를 따른다.
현재 변경에서 실제로 고려해야 할 risk만 적고 finding이나 Validation을 반복하지 않는다.
-->

{% for risk in risks %}
- {{ risk.importance }} — {{ risk.description }}
{% endfor %}
{% endif %}

{% if review_focus %}
## Review Focus

<!-- 앞의 변경, 검증과 risk를 바탕으로 특히 확인할 결정이나 trade-off를 적는다. Review 범위를 제한하지 않는다. -->

{% for item in review_focus %}
- {{ item }}
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
