<!--
GitHub UI가 path와 line을 보여주므로 위치를 반복하지 않는다.
한 comment에는 가능한 한 하나의 구체적 finding만 다룬다.
`importance`는 `🔴 Critical` / `🟠 High` / `🟡 Medium` / `🔵 Low` 중 하나를 그대로 사용한다.
Impact와 Required Change를 먼저 두어 문제의 의미와 필요한 결과를 빠르게 판단하게 한다.
Evidence는 판단에 필요한 근거만 보충한다.
Suggestion은 optional 대안이나 구현 예시에만 사용하며 Required Change와 같은 내용을 반복하지 않는다.
-->

{% if importance %}
**{{ importance }}**

{% endif %}
{{ message }}

{% if impact %}
**Impact:** {{ impact }}
{% endif %}

{% if required_change %}
**Required Change:** {{ required_change }}
{% endif %}

{% if evidence %}
**Evidence**

{% for item in evidence %}
- {{ item }}
{% endfor %}
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
