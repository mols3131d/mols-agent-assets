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
{% for item in author %}  - {{ item }}
{% endfor %}```
{% endif %}
