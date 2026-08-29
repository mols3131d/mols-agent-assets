## Summary

<!--
문제나 필요를 한눈에 이해할 수 있게 설명한다.
구현 방법보다 원하는 변화와 기대 결과를 먼저 쓴다.
Agent에게 독립 작업을 위임한다면 중요한 완료 조건과 경계를 명확히 하되 구현 절차는 과도하게 지정하지 않는다.
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
