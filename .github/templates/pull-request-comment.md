<!--
첫 문장에서 comment의 목적과 현재 결론을 바로 전달한다.
Evidence와 Next Actions는 판단이나 후속 작업에 실제로 필요할 때만 남긴다.
-->

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
