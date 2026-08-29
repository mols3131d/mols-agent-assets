<!--
GitHub UI가 path와 line을 보여주므로 위치를 반복하지 않는다.
한 comment에는 가능한 한 하나의 구체적 논점만 다룬다.
Importance는 PR Review의 Critical / High / Medium / Low 의미를 따른다.
Evidence와 Impact는 필요한 근거를 보충한다.
Required Change는 필요한 결과를, Suggestion은 optional 대안이나 구현 예시를 적으며 같은 내용을 반복하지 않는다.
-->

{{ message }}

{% if importance %}
**⚖️ Importance:** {{ importance }}
{% endif %}

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
