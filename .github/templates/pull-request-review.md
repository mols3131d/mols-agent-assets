<!--
작성 지침:
- verdict는 실제 review action과 일치시킨다: APPROVE, COMMENT, REQUEST_CHANGES.
- findings는 diff와 repository policy로 확인한 구체적 문제만 적는다.
- 발견 사항이 없으면 빈 findings section을 만들지 말고 결론에서 명확히 말한다.
- GitHub에 게시할 때 이 comment와 미치환 template syntax를 남기지 않는다.
-->

```yaml
verdict: "{{ verdict }}"
reviewed_commit: "{{ reviewed_commit }}"
scope: "{{ scope | default('entire PR') }}"
```

# 결론

{{ conclusion }}

{% if findings %}
## Findings

{% for finding in findings %}
### {{ finding.title }}

- **위치:** `{{ finding.location }}`
- **문제:** {{ finding.problem }}
- **영향:** {{ finding.impact }}
{% if finding.suggestion %}
- **제안:** {{ finding.suggestion }}
{% endif %}

{% endfor %}
{% endif %}

{% if verification %}
## 확인한 근거

{% for item in verification %}
- {{ item }}
{% endfor %}
{% endif %}
