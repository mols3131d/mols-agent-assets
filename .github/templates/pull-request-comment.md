<!--
작성 지침:
- comment의 목적을 첫 문장에서 바로 전달한다.
- status는 실제 상태를 짧게 표현하고, GitHub object의 공식 state를 대신하지 않는다.
- 근거와 다음 작업은 필요할 때만 남긴다.
- GitHub에 게시할 때 이 comment와 미치환 template syntax를 남기지 않는다.
-->

```yaml
purpose: "{{ purpose | default('update') }}"
status: "{{ status | default('info') }}"
related: "{{ related | default('none') }}"
```

{{ message }}

{% if evidence %}
## 근거

{% for item in evidence %}
- {{ item }}
{% endfor %}
{% endif %}

{% if next_actions %}
## 다음 작업

{% for action in next_actions %}
- [ ] {{ action }}
{% endfor %}
{% endif %}
