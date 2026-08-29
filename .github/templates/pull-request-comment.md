<!--
첫 문장에서 comment의 목적과 현재 결론을 바로 전달한다.
`status`는 workflow 상태를 명확히 전달할 때만 사용하며 `🔴 Blocked` / `🟡 Waiting` / `🟢 Ready` 중 하나를 그대로 사용한다.
Evidence와 Next Actions는 판단이나 후속 작업에 실제로 필요할 때만 남긴다.
-->

{% if status %}
**{{ status }}**

{% endif %}
{{ message }}

{% if evidence %}
## Evidence

{% for item in evidence %}
- {{ item }}
{% endfor %}
{% endif %}

{% if next_actions %}
## Next Actions

{% for action in next_actions %}
- [ ] {{ action }}
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
