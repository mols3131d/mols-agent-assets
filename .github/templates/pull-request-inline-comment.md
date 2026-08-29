```yaml
type: "{{ type }}"
{% if importance %}
importance: "{{ importance }}"
{% endif %}
```

<!--
GitHub UI가 path와 line을 이미 보여주므로 본문에서 위치를 반복하지 않는다.
한 comment에는 가능한 한 하나의 구체적 논점만 다룬다.
Evidence, Impact, Required Change, Suggestion은 실제 내용에 맞는 것만 남긴다.
-->

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
{% for item in author %}
  - {{ item }}
{% endfor %}
```
{% endif %}
