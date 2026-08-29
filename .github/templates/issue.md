## Summary

<!--
무엇이 문제이거나 필요한가? 원하는 변화는 무엇인가?
구현 방법보다 문제와 기대 결과를 먼저 설명한다.
-->

{{ summary }}

{% if context %}
## Context

{{ context }}
{% endif %}

## Desired Outcome

{{ desired_outcome }}

{% if acceptance_criteria %}
## Acceptance Criteria

{% for criterion in acceptance_criteria %}
- [ ] {{ criterion }}
{% endfor %}
{% endif %}

{% if reproduction %}
## Reproduction

{% for step in reproduction.steps %}
1. {{ step }}
{% endfor %}

- **Actual:** {{ reproduction.actual }}
- **Expected:** {{ reproduction.expected }}
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
