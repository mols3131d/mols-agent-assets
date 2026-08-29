## Summary

<!--
왜 이 변경이 필요한가? 병합 후 무엇이 달라지는가?
핵심부터 설명하고 구현 상세는 Changes에 둔다.
-->

{{ summary }}

## Changes

<!--
검토자가 diff에서 확인해야 할 최종 변화는 무엇인가?
파일 목록을 다시 쓰기보다 동작, 계약, 구조의 변화에 집중한다.
-->

{% for change in changes %}
- {{ change }}
{% endfor %}

## Validation

<!--
실제로 무엇을 확인했고 결과는 어땠는가?
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

{% for item in review_focus %}
- {{ item }}
{% endfor %}
{% endif %}

{% if risks %}
## Risks

{% for risk in risks %}
- ⚠️ {{ risk }}
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
