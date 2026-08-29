<!--
작성 지침:
- `{{ ... }}`를 확인된 값으로 치환한다.
- 적용되지 않는 `{% ... %}` block과 빈 section은 제거한다.
- GitHub에 게시할 때 이 comment와 미치환 template syntax를 남기지 않는다.
- 구현 방법보다 문제, 원하는 결과와 완료 조건을 먼저 명확히 한다.
-->

```yaml
type: "{{ type | default('task') }}"
scope: "{{ scope }}"
priority: "{{ priority | default('normal') }}"
related: "{{ related | default('none') }}"
```

# 요약

{{ summary }}

## 배경

{{ context }}

## 원하는 결과

{{ desired_outcome }}

## 완료 조건

{% for criterion in acceptance_criteria %}
- [ ] {{ criterion }}
{% endfor %}

{% if reproduction %}
## 재현

{% for step in reproduction.steps %}
1. {{ step }}
{% endfor %}

**현재 결과:** {{ reproduction.actual }}

**기대 결과:** {{ reproduction.expected }}
{% endif %}

{% if references %}
## 참고

{% for reference in references %}
- {{ reference }}
{% endfor %}
{% endif %}
