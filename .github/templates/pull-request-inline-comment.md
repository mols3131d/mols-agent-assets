<!--
작성 지침:
- GitHub UI가 path와 line을 이미 보여주므로 본문에서 중복하지 않는다.
- 한 comment에는 가능한 한 하나의 구체적 논점만 다룬다.
- type은 finding, question, suggestion처럼 comment의 역할을 실제 내용에 맞게 적는다.
- severity는 문제의 심각도 판단이 필요한 경우에만 남긴다.
- GitHub에 게시할 때 이 comment와 미치환 template syntax를 남기지 않는다.
-->

```yaml
type: "{{ type }}"
{% if severity %}severity: "{{ severity }}"{% endif %}
```

{{ message }}

{% if rationale %}
**근거:** {{ rationale }}
{% endif %}

{% if suggestion %}
**제안:** {{ suggestion }}
{% endif %}
