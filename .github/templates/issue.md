## Summary

<!--
무엇이 문제이거나 필요한가? 원하는 변화는 무엇인가?
구현 방법보다 문제와 기대 결과를 먼저 설명한다.
Agent에게 독립 작업을 위임하는 Issue라면 중요한 완료 조건과 넘지 말아야 할 경계를 충분히 명확히 하되 구현 절차를 과도하게 지정하지 않는다.
-->

{{ summary }}

{% if context %}
## Context

{{ context }}
{% endif %}

## Desired Outcome

{{ desired_outcome }}

{% if boundaries %}
## Boundaries

{% for boundary in boundaries %}
- {{ boundary }}
{% endfor %}
{% endif %}

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

{% if author %}
```yaml
author:
{% for item in author %}
  - {{ item }}
{% endfor %}
```
{% endif %}
