<!--
작성 지침:
- `{{ ... }}`를 실제 PR과 검증 결과에서 확인한 값으로 치환한다.
- 적용되지 않는 `{% ... %}` block과 빈 section은 제거한다.
- GitHub에 게시할 때 이 comment와 미치환 template syntax를 남기지 않는다.
- summary는 diff를 다시 나열하지 말고 변경의 목적과 결과를 먼저 설명한다.
-->

```yaml
type: "{{ type | default('change') }}"
scope: "{{ scope }}"
base: "{{ base_branch }}"
head: "{{ head_branch }}"
related: "{{ related | default('none') }}"
risk: "{{ risk | default('low') }}"
```

# 요약

{{ summary }}

## 변경

{% for change in changes %}
- {{ change }}
{% endfor %}

## 검증

{% for check in checks %}
- `{{ check.name }}` — {{ check.result }}
{% endfor %}

{% if checks_not_run %}
**미실행:** {{ checks_not_run }}
{% endif %}

{% if impact %}
## 영향

{{ impact }}
{% endif %}

{% if breaking_change %}
> [!WARNING]
> **Breaking change:** {{ breaking_change }}
{% endif %}

{% if review_points %}
## 리뷰 포인트

{% for point in review_points %}
- {{ point }}
{% endfor %}
{% endif %}
