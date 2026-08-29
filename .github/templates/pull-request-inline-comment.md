<!--
작성 지침:
- GitHub UI가 path와 line을 이미 보여주므로 본문에서 중복하지 않는다.
- 한 comment에는 가능한 한 하나의 구체적 문제만 다룬다.
- severity, 문제와 영향은 확인된 코드·문서 동작에 근거한다.
- 제안은 필요할 때만 남긴다.
- GitHub에 게시할 때 이 comment와 미치환 template syntax를 남기지 않는다.
-->

```yaml
severity: "{{ severity }}"
{% if category %}category: "{{ category }}"{% endif %}
```

{{ finding }}

**영향:** {{ impact }}

{% if suggestion %}
**제안:** {{ suggestion }}
{% endif %}
