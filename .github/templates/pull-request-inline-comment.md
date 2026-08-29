<!--
GitHub UI가 path와 line을 이미 보여주므로 본문에서 위치를 반복하지 않는다.
한 comment에는 가능한 한 하나의 구체적 논점만 다룬다.
Importance가 필요하면 PR Review와 같은 Critical / High / Medium / Low 의미를 사용한다.
Evidence와 Impact는 필요한 근거를 보충한다. Required Change는 finding을 해결하기 위해 필요한 결과, Suggestion은 optional한 대안이나 구현 예시에만 사용하며 같은 내용을 둘에 반복하지 않는다.
-->

{{ message }}

{% if importance %}
**Importance:** {{ importance }}
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
