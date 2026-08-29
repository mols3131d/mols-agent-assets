{{ message }}

{% if evidence %}
**Evidence**

{% for item in evidence %}
- {{ item }}
{% endfor %}
{% endif %}

{% if impact %}
**Impact:** {{ impact }}
{% endif %}

{% if required_change %}
**Required Change:** {{ required_change }}
{% endif %}

{% if suggestion %}
**Suggestion:** {{ suggestion }}
{% endif %}

{% if author %}
```yaml
author:
{% for item in author %}  - {{ item }}
{% endfor %}```
{% endif %}
