## Summary

<!--
문제나 필요와 원하는 변화를 먼저 설명한다.
구현 방법보다 왜 필요한지와 무엇이 달라져야 하는지에 집중한다.
Agent에게 독립 작업을 위임한다면 완료 조건과 경계를 분명히 하되 구현 절차는 과도하게 지정하지 않는다.
-->

{{ summary }}

## Desired Outcome

<!-- 완료되었을 때 기대하는 결과를 구체적으로 적는다. -->

{{ desired_outcome }}

{% if acceptance_criteria %}
## Acceptance Criteria

{% for criterion in acceptance_criteria %}
- [ ] {{ criterion }}
{% endfor %}
{% endif %}

{% if boundaries %}
## Boundaries

<!-- 포함·제외 범위나 넘지 말아야 할 제약만 적는다. -->

{% for boundary in boundaries %}
- {{ boundary }}
{% endfor %}
{% endif %}

{% if context %}
## Context

<!-- 판단에 필요한 배경만 남기고 Summary를 반복하지 않는다. -->

{{ context }}
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
