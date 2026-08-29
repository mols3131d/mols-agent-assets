<!--
첫 문장에서 comment의 목적과 현재 결론을 바로 전달한다.
`status`는 workflow 상태를 명확히 전달할 때만 사용하며 `🔴 Blocked` / `🟡 Waiting` / `🟢 Unblocked` 중 하나를 그대로 사용한다.
상태의 의미는 `docs/development/github.md`를 따른다.
Next Actions는 실제 후속 행동이 있을 때만 남기고, Evidence는 판단 근거가 필요할 때만 보충한다.
-->

{% if status %}
**{{ status }}**

{% endif %}
{{ message }}

{% if next_actions %}
## Next Actions

{% for action in next_actions %}
- [ ] {{ action }}
{% endfor %}
{% endif %}

{% if evidence %}
## Evidence

{% for item in evidence %}
- {{ item }}
{% endfor %}
{% endif %}

<!-- Agent가 최종 PR conversation text를 실질적으로 작성하거나 재작성했다면 `author`는 필수입니다. -->
{% if author %}
```yaml
author:
{% for item in author %}
  - {{ item }}
{% endfor %}
```
{% endif %}
